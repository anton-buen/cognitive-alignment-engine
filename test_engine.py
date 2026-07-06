import unittest
from unittest.mock import patch, MagicMock
import src.state_manager as sm
from src.engine import CognitiveAlignmentEngine
import os
import json
import requests

os.environ["USE_MOCK_LLM"] = "False"
class TestCognitiveAlignmentEngine(unittest.TestCase):
    def setUp(self):
        # [GATE 1: STATE] Reset a clean state before each test to prevent race conditions
        clean_state = {
            "live_transcript": [],
            "private_nudges": {"Data Analyst": [], "Production ML Engineer": []},
            "global_constraints": {"max_p99_latency_ms": 100}
        }
        sm.write_state(clean_state)
        self.engine = CognitiveAlignmentEngine()

    @patch('requests.post')
    def test_positive_trigger_writes_nudge(self, mock_post):
        """Test that a valid LLM trigger correctly mutates the target's private nudges."""
        # Mock the LLM returning a trigger
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"trigger": true, "nudge": "Heavy model detected."}'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Execute
        result = self.engine.evaluate_message("Alice", "Data Analyst", "Let's use a 100-layer neural net.")
        
        # Assert
        self.assertTrue(result)
        state = sm.read_state()
        self.assertIn("🤖 [CAE LLM] Heavy model detected.", state["private_nudges"]["Production ML Engineer"])

    @patch('requests.post')
    def test_negative_trigger_ignores_state(self, mock_post):
        """Test that a benign message does not trigger a nudge."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"trigger": false, "nudge": ""}'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Execute
        result = self.engine.evaluate_message("Bob", "Production ML Engineer", "Sounds good, data looks clean.")
        
        # Assert
        self.assertFalse(result)
        state = sm.read_state()
        self.assertEqual(len(state["private_nudges"]["Data Analyst"]), 0)

    @patch('requests.post')
    def test_network_timeout_graceful_degradation(self, mock_post):
        """[GATE 2: FEEDBACK] Test that a dead LLM endpoint does not crash the system."""
        # Force a network timeout exception
        mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")

        # Execute
        result = self.engine.evaluate_message("Alice", "Data Analyst", "Hello?")
        
        # Assert the system caught the error and gracefully returned False instead of crashing
        self.assertFalse(result)

    @patch('requests.post')
    def test_invalid_json_handling(self, mock_post):
        """Test how the engine handles AI hallucinations (bad JSON format)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": 'This is not JSON, I am hallucinating.'}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Execute
        result = self.engine.evaluate_message("Bob", "Production ML Engineer", "Deploying now.")
        
        # Assert the JSONDecodeError was caught and handled
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()