import os
import json
import base64
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ==========================================
# PAGE CONFIGURATION & STARK INDUSTRIES UI
# ==========================================
st.set_page_config(
    page_title="A.I.M.E.C.H.A. J.A.R.V.I.S.", 
    page_icon="🤖", 
    layout="wide"
)

# Stark Industries Cyber-Neon HUD Styling
st.markdown("""
    <style>
    /* Global HUD Background - Deep Space Navy Gradient */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #0B1D2E 0%, #050B14 100%); 
        color: #E2F1F8; 
    }
    
    /* Futuristic Glassmorphism Panels */
    div.stChatMessage { 
        background: rgba(10, 25, 47, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }
    
    /* Neon Text Headers */
    h1, h2, h3 { 
        color: #00E5FF !important; 
        text-shadow: 0 0 12px rgba(0, 229, 255, 0.8);
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
    }
    
    /* Glowing Action Buttons */
    .stButton>button { 
        background-color: rgba(0, 43, 61, 0.4) !important; 
        color: #00E5FF !important; 
        border: 1px solid #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #00E5FF !important; 
        color: #050B14 !important; 
    }
    
    /* Input Field Pulse Effect */
    [data-testid="stChatInput"] {
        background: rgba(10, 25, 47, 0.8) !important;
        border: 1px solid #00E5FF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.15);
    }
    
    /* Sidebar HUD Customization */
    [data-testid="stSidebar"] {
        background: rgba(5, 11, 20, 0.9) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. Core Operating System")
st.sidebar.title("⚙️ System Status")

# ==========================================
# MULTI-KEY POOL VERIFICATION
# ==========================================
if "GEMINI_API_POOL" not in st.secrets:
    st.sidebar.error("CONFIG ERROR: GEMINI_API_POOL missing.")
    st.stop()

if "exhausted_keys" not in st.session_state:
    st.session_state.exhausted_keys = set()

api_key_pool = st.secrets["GEMINI_API_POOL"]
available_keys = [k for k in api_key_pool if k not in st.session_state.exhausted_keys]

if not available_keys:
    st.sidebar.error("Engine status: ALL CORES EXHAUSTED")
    st.error("🚨 CRITICAL METRIC EXHAUSTION: Pool depleted until next reset.")
    st.stop()
else:
    active_idx = len(st.session_state.exhausted_keys) + 1
    st.sidebar.warning(f"Engine Core: Jarvis [{active_idx}/{len(api_key_pool)}] Active")

# ==========================================
# TOOLS & COGNITIVE PROMPT
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    with open(os.path.basename(file_name), "w", encoding="utf-8") as f:
        f.write(content)
    return "SUCCESS: File archived."

tools_list = [create_local_file]
JARVIS_MASTER_PROMPT = "You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated engineering mainframe. [Include your MSIG/Engineering guidelines here...]"

# ==========================================
# COMMAND INTERCEPT LOOP
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Mainframe initialized. Awaiting directives, sir."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            formatted_contents = [msg["content"] for msg in st.session_state.messages]
            
            response = None
            successful_key = None
            
            # AUTOMATIC ROTATION LOOP
            for active_key in available_keys:
                try:
                    client = genai.Client(api_key=active_key)
                    config = types.GenerateContentConfig(system_instruction=JARVIS_MASTER_PROMPT, tools=tools_list)
                    response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=formatted_contents, config=config)
                    successful_key = active_key
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        st.session_state.exhausted_keys.add(active_key)
                        continue
                    else:
                        st.error(f"Core Disruption: {str(e)}")
                        st.stop()
            
            if response:
                if response.function_calls:
                    # Tool handling... (Insert tool logic from previous block here)
                    pass
                else:
                    jarvis_output = response.text
                    st.markdown(jarvis_output)
                    st.session_state.messages.append({"role": "assistant", "content": jarvis_output})
                    st.rerun()
