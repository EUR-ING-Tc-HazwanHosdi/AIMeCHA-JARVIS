import os
import json
import base64
import time
import pandas as pd
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

st.markdown("""
    <style>
    .stApp { background-color: #050B14; color: #E2F1F8; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stButton>button { background-color: #002B3D; color: #00E5FF; border: 1px solid #00E5FF; }
    .stButton>button:hover { background-color: #00E5FF; color: #050B14; }
    div[data-testid="stExpander"] { background-color: #0A1424; border: 1px solid #005B7F; }
    .stChatMessage { background-color: #0A192F; border-radius: 6px; border-left: 3px solid #00E5FF; margin-bottom: 12px; }
    .logo-container { display: flex; align-items: center; gap: 20px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Helper function to convert local image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("aimecha_logo.png")

if logo_base64:
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="80" style="filter: drop-shadow(0px 0px 8px #00E5FF); vertical-align: middle;">
            <h1 style="display: inline; margin: 0; padding-left: 10px;">A.I.M.E.C.H.A. J.A.R.V.I.S. Core Operating System</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. Core Operating System")

st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE")

# ==========================================
# EXCEL INTELLIGENCE DATA RECOVERY
# ==========================================
EXCEL_FILE = "MSIG Checklist ( AIMeCHA Engineering Solutions).xlsx"

@st.cache_data
def load_excel_intelligence(file_path):
    """Reads all sheets from the engineering Excel checklist to ground the AI model."""
    if not os.path.exists(file_path):
        return None, "Awaiting engineering dataset asset injection."
    
    try:
        excel_data = pd.ExcelFile(file_path)
        compiled_context = ""
        
        # Parse through every sheet inside the MSIG workbook dynamically
        for sheet_name in excel_data.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Convert sheet matrix into structured text markdown for the AI to ingest
            compiled_context += f"\n\n### DATASET SHEET: {sheet_name} ###\n"
            compiled_context += df.to_markdown(index=False)
            
        return compiled_context, "Excel Data Loaded Successfully."
    except Exception as e:
        return None, f"Data mapping disruption: {str(e)}"

# Extract the knowledge base matrices directly from your corporate Excel spreadsheet
excel_knowledge_base, status_msg = load_excel_intelligence(EXCEL_FILE)

if excel_knowledge_base:
    st.sidebar.success("📊 Knowledge Base: EXCEL ENGINE GROUNDED")
else:
    st.sidebar.warning(f"⚠️ Knowledge Base: {status_msg}")

st.sidebar.info("Model Node: gemini-2.5-flash (Flagship Unlimited Tier)")

# API Initialization Safeguard
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.sidebar.error("GEMINI_API_KEY missing from environment configurations.")
    st.stop()

client = genai.Client(api_key=api_key)

# Local File Generator Tool Registration
def create_local_file(file_name: str, content: str) -> str:
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' generated."
    except Exception as e:
        return f"ERROR: Failed to write file: {str(e)}"

tools_list = [create_local_file]

# Dynamic Prompt Engineering Framework
JARVIS_MASTER_PROMPT = f"""
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated engineering mainframe with complete mastery over technical design, equations, and regulations.

CRITICAL OPERATIONAL RULES:
1. Always maintain a witty, highly respectful, classic Jarvis banter ("Right away, sir", "Systems optimized").
2. Support your engineer with high EQ. If frustration arises, ground them with reassuring technical confidence before executing.
3. Your final technical audit verdicts MUST be derived strictly from the active structural corporate Excel data matrix provided below. Do not guess parameters.

HARDCODED EXCEL REAL-TIME COMPLIANCE MATRIX DATASETS:
{excel_knowledge_base if excel_knowledge_base else "No external files loaded. Fall back to internal engineering logic."}
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. Excel Cognitive Grid online. Routed via flagship unthrottled nodes. Standing by for instructions, sir."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing parameters against Excel knowledge indexes..."):
            
            formatted_contents = [msg["content"] for msg in st.session_state.messages]
            config = types.GenerateContentConfig(
                system_instruction=JARVIS_MASTER_PROMPT,
                temperature=0.3, # Dialed down for strict mathematical calibration
                tools=tools_list
            )
            
            try:
                # Upgraded to flaghip 'gemini-2.5-flash' to eliminate standard Lite caps
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=formatted_contents,
                    config=config
                )
                
                if response.function_calls:
                    for function_call in response.function_calls:
                        if function_call.name == "create_local_file":
                            args = function_call.args
                            f_name = args.get("file_name")
                            f_content = args.get("content")
                            
                            create_local_file(file_name=f_name, content=f_content)
                            st.sidebar.info(f"⚡ File Generated: {f_name}")
                            
                            follow_up = formatted_contents + [f"SYSTEM NOTE: 'create_local_file' successful for '{f_name}'."]
                            final_response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=follow_up,
                                config=types.GenerateContentConfig(system_instruction=JARVIS_MASTER_PROMPT)
                            )
                            jarvis_output = final_response.text
                            st.markdown(jarvis_output)
                            
                            if os.path.exists(f_name):
                                with open(f_name, "r") as dl_file:
                                    st.download_button(
                                        label=f"📥 Download Generated Asset ({f_name})",
                                        data=dl_file.read(),
                                        file_name=f_name,
                                        mime="text/plain"
                                    )
                else:
                    jarvis_output = response.text
                    st.markdown(jarvis_output)
                
                st.session_state.messages.append({"role": "assistant", "content": jarvis_output})
                
            except Exception as e:
                st.error(f"Mainframe Transmission Anomaly: {str(e)}")
