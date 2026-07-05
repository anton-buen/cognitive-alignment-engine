import streamlit as st
import src.state_manager as sm
from src.engine import CognitiveAlignmentEngine

# 1. UI Configuration
st.set_page_config(page_title="Project Naur", layout="wide", initial_sidebar_state="expanded")

def apply_adaptive_theme():
    """
    Bulletproof fluid theming. 
    Pins the disclaimer to the bottom viewport and elevates the chat input.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* 1. Define Strict Palette Variables */
        @media (prefers-color-scheme: light) {
            :root {
                --naur-bg: #FBF9F5;
                --naur-surface: #F2EFE9;
                --naur-text: #1E1D1B;
                --naur-border: #E2DCD2;
                --naur-muted: #68645E;
            }
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --naur-bg: #161616;
                --naur-surface: #262626;
                --naur-text: #f4f4f4;
                --naur-border: #393939;
                --naur-muted: #8d8d8d;
            }
        }

        /* 2. Bruteforce Backgrounds */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--naur-bg) !important;
            color: var(--naur-text) !important;
            font-family: 'IBM Plex Sans', sans-serif !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
            background-color: var(--naur-surface) !important;
        }

        /* 3. Typography Management */
        .playfair { font-family: 'Playfair Display', serif !important; color: var(--naur-text) !important; }
        h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif !important; color: var(--naur-text) !important; }
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * { color: var(--naur-text) !important; }

        /* 4. Chat Interface Overrides */
        [data-testid="stChatInput"] {
            background-color: var(--naur-bg) !important;
            padding-bottom: 3rem !important; 
        }
        [data-testid="stChatInput"] textarea {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.05rem !important;
            background-color: var(--naur-surface) !important;
            border: 1px solid var(--naur-border) !important;
            border-radius: 0px !important;
            color: var(--naur-text) !important;
            padding: 1rem !important;
        }
        [data-testid="stChatInput"] textarea:focus { border-color: var(--naur-text) !important; }
        
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            border-radius: 0px !important;
            padding: 1.5rem 0 !important;
            border-bottom: 1px solid var(--naur-border);
        }
        [data-testid="chatAvatarIcon-human"], [data-testid="chatAvatarIcon-user"] {
            background-color: var(--naur-surface) !important;
            color: var(--naur-text) !important;
            border: 1px solid var(--naur-border);
            border-radius: 0px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background-color: var(--naur-text) !important;
            color: var(--naur-bg) !important;
            border-radius: 0px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 5. Buttons */
        .stButton>button, .stDownloadButton>button {
            border-radius: 0px !important;
            font-family: 'IBM Plex Sans', sans-serif !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.8rem !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.2s ease !important;
            background-color: transparent !important;
            border: 1px solid var(--naur-border) !important;
            color: var(--naur-text) !important;
        }
        .stDownloadButton>button:hover, [data-testid="stSidebar"] .stButton>button:hover {
            border-color: var(--naur-text) !important;
        }

        /* 6. Output Cards */
        .tech-card {
            background-color: var(--naur-surface);
            border: 1px solid var(--naur-border);
            padding: 1.5rem;
            height: 100%;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem;
            line-height: 1.6;
            color: var(--naur-text);
            white-space: pre-wrap;
        }
        .card-title {
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
        }
        .card-fe { border-top: 3px solid #78a9ff !important; } 
        .card-be { border-top: 3px solid #42be65 !important; } 
        .card-ds { border-top: 3px solid #be95ff !important; } 

        hr { border-color: var(--naur-border) !important; margin: 2.5rem 0; }
        
        /* 7. Permanent Fixed Footer */
        [data-testid="stChatInput"] {
            padding-bottom: 2rem !important; 
        }
        
        [data-testid="stChatInput"]::after {
            content: "Project Naur helps catch technical blind spots before coding begins. AI can make mistakes, so always review these constraints with your team.";
            display: block;
            text-align: center;
            font-size: 0.75rem;
            color: var(--naur-muted);
            font-family: 'IBM Plex Sans', sans-serif;
            margin-top: 0.5rem;
            opacity: 0.8;
            pointer-events: none;
        }
    </style>
    """, unsafe_allow_html=True)

def generate_markdown_export(intent: str, assumptions: dict) -> str:
    return f"# Alignment Extraction\n**Intent:** {intent}\n\n### Technical Constraints\n- **Frontend:** {assumptions.get('FE', 'None detected.')}\n- **Backend:** {assumptions.get('BE', 'None detected.')}\n- **Data Science:** {assumptions.get('DS', 'None detected.')}\n"

# 2. Inject Theme
apply_adaptive_theme()

# 3. Engine 
try:
    if "engine" not in st.session_state:
        st.session_state.engine = CognitiveAlignmentEngine()
    engine = st.session_state.engine
except Exception as e:
    st.error(f"System Failure: {e}")
    st.stop()

# 4. Sidebar
with st.sidebar:
    st.markdown("<h2 class='playfair' style='margin-bottom: 0.5rem; font-size: 2rem;'>Project Naur</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; margin-bottom: 2rem; opacity: 0.8;'>Decompress feature intents to prevent integration failure.</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Session Admin</h3>", unsafe_allow_html=True)
    if st.button("Clear Ledger", use_container_width=True):
        state = sm.read_state()
        state["extractions"] = []
        sm.write_state(state)
        st.rerun()

# 5.Architecture Thread
st.markdown("<h2 class='playfair' style='margin-top: 0; font-size: 1.8rem;'>Architecture Thread</h2>", unsafe_allow_html=True)

state = sm.read_state()
thread = state.get("thread", [])

if not thread:
    st.markdown("<div style='opacity: 0.6; margin-top: 1rem;'>The thread is empty. Propose a feature below to begin alignment.</div>", unsafe_allow_html=True)
else:
    for index, msg in enumerate(thread):
        if msg["role"] == "human":
            with st.chat_message("human"):
                st.markdown(f"<div style='font-weight: 600; font-size: 1.05rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                assumptions = msg.get('assumptions', {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='tech-card card-fe'><div class='card-title' style='color: #78a9ff;'>Frontend Delta</div>{assumptions.get('FE', 'No constraints detected.')}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='tech-card card-be'><div class='card-title' style='color: #42be65;'>Backend Delta</div>{assumptions.get('BE', 'No constraints detected.')}</div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='tech-card card-ds'><div class='card-title' style='color: #be95ff;'>Data Science Delta</div>{assumptions.get('DS', 'No constraints detected.')}</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

# Padding
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# 6. Chat Input Layer
if user_intent := st.chat_input("Join the discussion... (e.g., '[Backend] We can't use WebSockets...')"):
    with st.chat_message("human"):
        st.markdown(f"<div style='font-weight: 600; font-size: 1.05rem;'>{user_intent}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant"):
        with st.spinner("Synthesizing constraints..."):
            success = engine.process_intent(user_intent)
        if success:
            st.rerun()
        else:
            st.error("System failure.")