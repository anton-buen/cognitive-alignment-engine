import json
import os

DB_FILE = "session_state.json"

def read_state() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def write_state(state_data: dict) -> bool:
    temp_file = f"{DB_FILE}.tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        os.replace(temp_file, DB_FILE)
        return True
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"[ERROR] State write failure: {e}")
        return False