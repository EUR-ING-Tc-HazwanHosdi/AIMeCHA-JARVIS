import os
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# PAGE CONFIGURATION & UI
# ==========================================
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050B14; color: #E2F1F8; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stChatMessage { background-color: #0A192F; border-radius: 6px; border-left: 3px solid #00E5FF; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. AI Engine")
st.sidebar.title("⚙️ System Status")

# ==========================================
# SINGLE-KEY INITIALIZATION
# ==========================================
if "GEMINI_API_KEY" not in st.secrets:
    st.sidebar.error("GEMINI_API_KEY missing from Secrets configuration.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
st.sidebar.success("Cognitive Core: ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")

# ==========================================
# TOOLSET: FILE GENERATOR
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' generated."
    except Exception as e:
        return f"ERROR: {str(e)}"

tools_list = [create_local_file]

# ==========================================
# COGNITIVE SYSTEM PROMPT
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., an expert engineering mainframe grounded in Malaysian regulatory standards (MSIG, DOSH, CIDB, BEM).
You possess total mastery over engineering disciplines and provide optimal, documented code. 
Always remain empathetic, professional, and witty.
If asked to generate a file, use the 'create_local_file' tool.
"""

# ==========================================
# SESSION MEMORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. framework online. Awaiting your instructions, sir."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# EXECUTION PIPELINE
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            try:
                client = genai.Client(api_key=api_key)
                config = types.GenerateContentConfig(
                    system_instruction=JARVIS_MASTER_PROMPT,
                    temperature=0.4,
                    tools=tools_list
                )
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[msg["content"] for msg in st.session_state.messages],
                    config=config
                )

                if response.function_calls:
                    for call in response.function_calls:
                        if call.name == "create_local_file":
                            res = create_local_file(call.args["file_name"], call.args["content"])
                            st.markdown(f"**{res}**")
                            st.session_state.messages.append({"role": "assistant", "content": res})
                else:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Mainframe Core Disruption: {str(e)}")
