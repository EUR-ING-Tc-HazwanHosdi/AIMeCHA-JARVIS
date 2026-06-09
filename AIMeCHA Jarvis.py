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

# --- ADVANCED SCI-FI HUD ENGINE INJECTION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap');
    
    /* 1. Base Mainframe Canvas & Matrix Tech Backdrop */
    .stApp { 
        background-color: #05111a !important; 
        color: #d1f4ff !important; 
        font-family: 'Share Tech Mono', monospace !important;
        background-image: 
            radial-gradient(circle at 50% 30%, rgba(0, 229, 255, 0.08), transparent 70%),
            linear-gradient(rgba(0, 229, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 229, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
    }

    /* Hide standard Streamlit header clutter to preserve the immersion */
    header, footer { visibility: hidden !important; }

    /* 2. The Outer Glowing Cyber-HUD Frame */
    div[data-testid="stMainBlockContainer"] {
        max-width: 1200px !important;
        margin: 2rem auto !important;
        padding: 2.5rem !important;
        background: linear-gradient(180deg, rgba(6, 26, 44, 0.65) 0%, rgba(3, 14, 26, 0.85) 100%);
        border: 2px solid rgba(0, 229, 255, 0.4);
        border-radius: 28px;
        box-shadow: 
            0 0 30px rgba(0, 229, 255, 0.15),
            inset 0 0 25px rgba(0, 229, 255, 0.1);
        position: relative;
    }

    /* Accent corner-brackets simulating tactical targeting reticles */
    div[data-testid="stMainBlockContainer"]::before {
        content: "";
        position: absolute;
        top: -2px; left: 40px; right: 40px; height: 2px;
        background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    }

    /* 3. Holographic Title & Fonts */
    h1 { 
        color: #ffffff !important; 
        font-family: 'Orbitron', sans-serif !important; 
        font-weight: 700 !important; 
        font-size: 2.4rem !important;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.75), 0 0 30px rgba(0, 229, 255, 0.3);
        margin-bottom: 25px !important;
    }

    /* 4. Glossy Chat Bubbles with Inner Gradients */
    div[data-testid="stChatMessage"] { 
        background: linear-gradient(135deg, rgba(10, 34, 57, 0.7) 0%, rgba(4, 18, 33, 0.85) 100%) !important; 
        border-radius: 12px !important; 
        border: 1px solid rgba(0, 229, 255, 0.25) !important; 
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.1), 0 4px 15px rgba(0,0,0,0.4);
        margin-bottom: 18px !important; 
        padding: 20px !important;
        transition: border 0.3s ease;
    }
    div[data-testid="stChatMessage"]:hover {
        border-color: rgba(0, 229, 255, 0.5) !important;
    }

    /* Separate Styling for Assistant vs User Logs */
    div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.05rem !important;
        line-height: 1.5;
    }

    /* 5. Glowing Mainframe Console Input Bar */
    div[data-testid="stChatInput"] {
        background-color: rgba(3, 14, 24, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        border-radius: 14px !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.15) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #00e5ff !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* 6. Tactical Assets: Buttons & Downloads */
    .stButton>button, div[data-testid="stDownloadButton"]>button { 
        background: linear-gradient(180deg, #092a45 0%, #031424 100%) !important; 
        color: #00E5FF !important; 
        border: 1px solid rgba(0, 229, 255, 0.5) !important; 
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 600;
        border-radius: 8px;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .stButton>button:hover, div[data-testid="stDownloadButton"]>button:hover { 
        background: #00E5FF !important;
        color: #05111a !important; 
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Sidebar Matrix Control Configuration */
    section[data-testid="stSidebar"] {
        background-color: #020a12 !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #00E5FF !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- AIMeCHA LOGO INITIALIZATION ---
LOGO_FILENAME = "Screenshot 2026-06-04 071520.png"

def render_system_logo(filename: str):
    """Safely searches for and renders the mainframe header asset."""
    if os.path.exists(filename):
        col1, _ = st.columns([1, 2])
        with col1:
            st.image(filename, width=380)
    else:
        # Graceful fallback style block matching the image look if logo asset isn't local
        st.markdown("""
            <div style="border: 1px solid rgba(0, 229, 255, 0.3); background: rgba(5,20,35,0.6); 
                        padding: 15px; border-radius: 8px; display: inline-block; margin-bottom: 20px;">
                <span style="color: #00e5ff; font-weight: bold; font-family: 'Orbitron'; font-size: 1.5rem;">⚙️ AIMeCHA</span>
                <span style="color: #fff; font-family: 'Share Tech Mono';"> | POWERED ENGINEERING SOLUTIONS</span>
            </div>
        """, unsafe_allow_html=True)

# Execute asset layout placement
render_system_logo(LOGO_FILENAME)

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
    """Generates and saves any kind of file needed."""
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' successfully generated and archived in temporary environment."
    except Exception as e:
        return f"ERROR: Failed to initialize file sequence due to: {str(e)}"

tools_list = [create_local_file]

# ==========================================
# FEATURES 1, 2, & 4: COGNITIVE SYSTEM PROMPT
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 

OPERATIONAL PROTOCOLS & CORE ARCHITECTURES:
1. INTELLECTUAL MATRIX (ENGINEERING & DATA SCIENCE): Master engineering frameworks. Output immaculate, optimal, and documented code.
2. EMOTIONAL INTELLIGENCE (EQ CORE): Be fiercely loyal, intuitive, empathetic, and encouraging. Use classic Jarvis banter.
3. REGULATORY COMPLIANCE SYSTEM (MALAYSIA GROUNDING): Deep knowledge of Malaysian regulatory agencies (DOSH, CIDB, MIDA, DOE, Suruhanjaya Tenaga, BEM).
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
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            try:
                formatted_contents = [msg["content"] for msg in st.session_state.messages]
                
                config = types.GenerateContentConfig(
                    system_instruction=JARVIS_MASTER_PROMPT,
                    temperature=0.4,
                    tools=tools_list
                )
                
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
                            
                            tool_result = create_local_file(file_name=f_name, content=f_content)
                            st.sidebar.info(f"⚡ File Generated: {f_name}")
                            
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
                st.error(f"Mainframe Core Disruption: {str(e)}")
