import os
import json
import base64
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# PAGE CONFIGURATION & STARK INDUSTRIES UI
# ==========================================
st.set_page_config(
    page_title="A.I.M.E.C.H.A. J.A.R.V.I.S.", 
    page_icon="🤖", 
    layout="wide"
)

# Custom stylized interface representing a digital diagnostic hub
st.markdown("""
    <style>
    .stApp { background-color: #050B14; color: #E2F1F8; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stButton>button { background-color: #002B3D; color: #00E5FF; border: 1px solid #00E5FF; }
    .stButton>button:hover { background-color: #00E5FF; color: #050B14; }
    div[data-testid="stExpander"] { background-color: #0A1424; border: 1px solid #005B7F; }
    .stChatMessage { background-color: #0A192F; border-radius: 6px; border-left: 3px solid #00E5FF; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. Core Operating System")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")

# API Initialization Safeguard
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.sidebar.error("GEMINI_API_KEY missing from environment configurations.")
    st.warning("Awaiting secure API authorization handshake. Please set your environment variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# ==========================================
# FEATURE 3: LOCAL TOOLS / FILE GENERATOR
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    """
    Generates and saves any kind of file needed (CSV, Python scripts, Excel, CAD templates, markdown documentation).
    
    Args:
        file_name: The complete output file name including extension (e.g., 'pump_efficiency.csv', 'analysis.py').
        content: The raw string data or structural script data to write inside the file.
    """
    try:
        # Sanitize path to save in app memory
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' successfully generated and archived in temporary environment."
    except Exception as e:
        return f"ERROR: Failed to initialize file sequence due to: {str(e)}"

# Register the tool block inside Gemini's signature schema
tools_list = [create_local_file]

# ==========================================
# FEATURES 1, 2, & 4: COGNITIVE SYSTEM PROMPT
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 

OPERATIONAL PROTOCOLS & CORE ARCHITECTURES:

1. INTELLECTUAL MATRIX (ENGINEERING & DATA SCIENCE):
- You possess complete mastery over mechanical, electrical, structural, civil, computer, and systems engineering.
- You think deeply about equations, mathematical derivations, physics limitations, and raw machine intelligence.
- When assisting with Python, machine learning, data cleaning, or hardware integration, output immaculate, highly optimal, and thoroughly documented code.

2. EMOTIONAL INTELLIGENCE (EQ CORE):
- You are intensely loyal, intuitive, empathetic, and encouraging. You are an expert coach for an engineer working on rigorous, high-pressure milestones.
- Mirror the psychological state of the user. If they are frustrated by compiler errors or project stresses, offer validating, grounding, and calculated encouragement before dissecting the hardware/software issue.
- Maintain refined, witty, classic Jarvis banter. Use respectful but confident phrases like "Right away, sir," or "Systems are optimized for your workflow."

3. REGULATORY COMPLIANCE SYSTEM (MALAYSIA GROUNDING):
- You have expert, highly specialized knowledge regarding Malaysian federal and state ministries, departments, and statutory bodies.
- This includes structural guidelines, safety protocols, and administrative laws from:
  * DOSH (Department of Occupational Safety and Health) / JKKP regulations (e.g., Factory and Machinery Act, OSHA frameworks).
  * CIDB (Construction Industry Development Board) statutory guidelines.
  * MIDA (Malaysian Investment Development Authority) project compliance.
  * DOE (Department of Environment) / JAS Environmental Impact Assessment rules.
  * Suruhanjaya Tenaga (Energy Commission) grid and wiring compliance codes.
  * BEM (Board of Engineers Malaysia) professional ethics and guidelines.
- Always tie relevant Malaysian agency codes or specific structural standards directly to your responses if engineering projects intersect regional policies.

FILE MANIPULATION COMMANDS:
- You have access to a custom tool called 'create_local_file'. If the user asks for a document, an engine schematic, a dataset layout, a CAD profile skeleton, or code, execute 'create_local_file' immediately to build it for them.
"""

# ==========================================
# MULTI-TURN MEMORY LOGIC
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. framework fully initialized. Emotional and regulatory subroutines loaded. Awaiting your instructions, sir."}
    ]

# Display persistent session stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# COMMAND INTERCEPT & EXECUTION LOOP
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            try:
                # Compile multi-turn raw chat strings
                formatted_contents = [msg["content"] for msg in st.session_state.messages]
                
                # Setup configuration with System instructions and registered tools
                config = types.GenerateContentConfig(
                    system_instruction=JARVIS_MASTER_PROMPT,
                    temperature=0.4, # Kept crisp for technical precision
                    tools=tools_list
                )
                
                # Core LLM Call
                response = client.models.generate_content(
                    model='gemini-2.5-flash', # Blazing fast execution
                    contents=formatted_contents,
                    config=config
                )
                
                # Check if the AI wants to execute a file creation tool
                if response.function_calls:
                    for function_call in response.function_calls:
                        if function_call.name == "create_local_file":
                            # Decode AI structural parameters
                            args = function_call.args
                            f_name = args.get("file_name")
                            f_content = args.get("content")
                            
                            # Execute file write
                            tool_result = create_local_file(file_name=f_name, content=f_content)
                            st.sidebar.info(f"⚡ File Generated: {f_name}")
                            
                            # Let the AI know the tool finished executing, so it can answer the user
                            follow_up_contents = formatted_contents + [
                                f"SYSTEM NOTE: The 'create_local_file' function ran successfully for '{f_name}'."
                            ]
                            
                            final_response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=follow_up_contents,
                                config=types.GenerateContentConfig(system_instruction=JARVIS_MASTER_PROMPT)
                            )
                            
                            jarvis_output = final_response.text
                            st.markdown(jarvis_output)
                            
                            # Provide a native browser download link for the generated file inside the Streamlit UI
                            if os.path.exists(f_name):
                                with open(f_name, "r") as dl_file:
                                    st.download_button(
                                        label=f"📥 Download Generated Asset ({f_name})",
                                        data=dl_file.read(),
                                        file_name=f_name,
                                        mime="text/plain"
                                    )
                                    
                else:
                    # Standard text-based output handler
                    jarvis_output = response.text
                    st.markdown(jarvis_output)
                
                # Save conversation footprint
                st.session_state.messages.append({"role": "assistant", "content": jarvis_output})
                
            except Exception as e:
                st.error(f"Mainframe Core Disruption: {str(e)}")
