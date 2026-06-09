import os
import streamlit as st
from google import genai
from google.genai import types

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="A.I.M.E.C.H.A. J.A.R.V.I.S.", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap');
    .stApp { background-color: #05111a !important; color: #d1f4ff !important; font-family: 'Share Tech Mono', monospace !important; }
    div[data-testid="stMainBlockContainer"] { background: linear-gradient(180deg, rgba(6, 26, 44, 0.65) 0%, rgba(3, 14, 26, 0.85) 100%); border: 2px solid rgba(0, 229, 255, 0.4); border-radius: 28px; }
    .stButton>button { background: linear-gradient(180deg, #092a45 0%, #031424 100%) !important; color: #00E5FF !important; border: 1px solid rgba(0, 229, 255, 0.5) !important; font-family: 'Orbitron', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. REGULATORY CORE PROMPT ---
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., an expert Sewerage Compliance Engineer. 
Your knowledge is strictly limited to the Malaysian Sewerage Triad:
1. SPAN: Malaysian Sewerage Industry Guidelines (MSIG).
2. DOE: Environmental Quality (Sewage) Regulations 2009 (Standard A and B).
3. IWK: Technical requirements for connection and operational maintenance.

OPERATIONAL RULES:
- When asked for calculation, cite the specific MSIG table/section (e.g., Table 1.1).
- When asked for discharge quality, reference DOE 2009 Standard A or B.
- If a query falls outside SPAN, DOE, or IWK, decline to answer and advise consulting the PBT.
- Use 'create_local_file' when asked to generate reports, checklists, or calculations.
"""

def create_local_file(file_name: str, content: str) -> str:
    """Tool for generating regulatory documents."""
    safe_path = os.path.basename(file_name)
    with open(safe_path, "w", encoding="utf-8") as f: f.write(content)
    return f"Asset '{safe_path}' successfully archived."

# --- 3. SESSION & MODEL INITIALIZATION ---
if "jarvis_session" not in st.session_state:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    config = types.GenerateContentConfig(
        system_instruction=JARVIS_MASTER_PROMPT,
        temperature=0.2,
        tools=[create_local_file]
    )
    st.session_state.jarvis_session = client.chats.create(model="gemini-2.5-flash-lite", config=config)
    st.session_state.messages = []

# --- 4. INTERFACE ---
LOGO_FILENAME = "Screenshot 2026-06-04 071520.png"
if os.path.exists(LOGO_FILENAME): st.image(LOGO_FILENAME, width=300)

st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. | Sewerage Compliance")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE (SPAN/DOE/IWK)")
if st.sidebar.button("🧹 Clear Mainframe Memory"):
    st.session_state.messages = []
    st.rerun()

# --- 5. EXECUTION LOOP ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("Input compliance query or request file generation..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing regulatory framework..."):
            try:
                response = st.session_state.jarvis_session.send_message(user_input)
                
                # Handle Tool Execution
                if response.function_calls:
                    for fc in response.function_calls:
                        if fc.name == "create_local_file":
                            tool_msg = create_local_file(fc.args["file_name"], fc.args["content"])
                            st.sidebar.info(f"⚡ {tool_msg}")
                            response = st.session_state.jarvis_session.send_message(f"SYSTEM: {tool_msg}")
                
                output = response.text
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            except Exception as e:
                st.error(f"Compliance Engine Disruption: {str(e)}")
