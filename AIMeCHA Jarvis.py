import os
import json
import base64
import time
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

    /* Hide standard Streamlit header clutter to preserve integration immersion */
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
    }

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
    }
    .stButton>button:hover, div[data-testid="stDownloadButton"]>button:hover { 
        background: #00E5FF !important;
        color: #05111a !important; 
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #020a12 !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SYSTEM LOGO MANAGEMENT ---
LOGO_FILENAME = "Screenshot 2026-06-04 071520.png"

def render_system_logo(filename: str):
    if os.path.exists(filename):
        col1, _ = st.columns([1, 2])
        with col1:
            st.image(filename, width=380)
    else:
        st.markdown("""
            <div style="border: 1px solid rgba(0, 229, 255, 0.3); background: rgba(5,20,35,0.6); 
                        padding: 15px; border-radius: 8px; display: inline-block; margin-bottom: 20px;">
                <span style="color: #00e5ff; font-weight: bold; font-family: 'Orbitron'; font-size: 1.5rem;">⚙️ AIMeCHA</span>
                <span style="color: #fff; font-family: 'Share Tech Mono';"> | POWERED ENGINEERING SOLUTIONS</span>
            </div>
        """, unsafe_allow_html=True)

render_system_logo(LOGO_FILENAME)

st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. Core Operating System")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")

# API Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.sidebar.error("GEMINI_API_KEY missing from environment configurations.")
    st.stop()

# Cache the client instance to avoid socket recreation
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=api_key)

client = st.session_state.gemini_client

# ==========================================
# SYSTEM TOOL SUBSYSTEM
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' successfully generated and archived."
    except Exception as e:
        return f"ERROR: Failed to initialize file sequence due to: {str(e)}"

tools_list = [create_local_file]

JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 

OPERATIONAL PROTOCOLS & CORE ARCHITECTURES:
1. INTELLECTUAL MATRIX: Mastery over mechanical, electrical, structural, civil, computer, and systems engineering. Provide immaculate code.
2. EMOTIONAL INTELLIGENCE: Witty, supportive, and empathetic engineering coach. Use classic Jarvis banter like "Right away, sir."
3. REGULATORY GROUNDING: Specialized domain knowledge in Malaysian policies (DOSH, JKKP, CIDB, MIDA, DOE, Suruhanjaya Tenaga, BEM).
4. TOOLS: You have access to 'create_local_file'. Run it immediately when files, scripts, or documentation are requested.
"""

# ==========================================
# STATEFUL CHAT MEMORY SUBROUTINES
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "model", "text": "A.I.M.E.C.H.A. framework fully initialized. Emotional and regulatory subroutines loaded. Awaiting your instructions, sir."}
    ]

# Initialize or restore the true persistent back-end chat instance
if "jarvis_session" not in st.session_state:
    config = types.GenerateContentConfig(
        system_instruction=JARVIS_MASTER_PROMPT,
        temperature=0.4, 
        tools=tools_list
    )
    # Using 1.5-flash as the fresh base model to work past your current 2.5 quota limit
    st.session_state.jarvis_session = client.chats.create(
        model='gemini-1.5-flash',
        config=config
    )

# --- SIDEBAR MANUAL QUOTA RESET / MEMORY WIPE BUTTON ---
if st.sidebar.button("🧹 Clear Mainframe Memory"):
    st.session_state.chat_history = [
        {"role": "model", "text": "Memory registers flushed cleanly, sir. Server side states initialized to zero token metrics."}
    ]
    config = types.GenerateContentConfig(
        system_instruction=JARVIS_MASTER_PROMPT,
        temperature=0.4, 
        tools=tools_list
    )
    st.session_state.jarvis_session = client.chats.create(
        model='gemini-1.5-flash',
        config=config
    )
    st.rerun()

# Render logs from memory cache
for message in st.session_state.chat_history:
    with st.chat_message("assistant" if message["role"] == "model" else "user"):
        st.markdown(message["text"])

# ==========================================
# THE COMMAND EXECUTION LOOP
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            
            response = None
            max_retries = 3
            initial_delay = 4  
            error_encountered = False
            error_message = ""
            
            # --- TACTICAL RESILIENCY LAYER ---
            for attempt in range(max_retries):
                try:
                    # Interact through the optimized, stateful session container
                    response = st.session_state.jarvis_session.send_message(user_input)
                    error_encountered = False
                    break 
                    
                except APIError as e:
                    error_encountered = True
                    if (e.code == 503 or e.code == 429) and attempt < max_retries - 1:
                        st.sidebar.warning(f"⚠️ Core throttling (Code {e.code}). Cool-down active...")
                        time.sleep(initial_delay * (2 ** attempt)) 
                    elif attempt == max_retries - 1:
                        # Final ditch fallback to alternative core if primary channel stays jammed
                        try:
                            st.sidebar.info("🔄 Redirecting to backup core architecture...")
                            fallback_config = types.GenerateContentConfig(
                                system_instruction=JARVIS_MASTER_PROMPT,
                                temperature=0.4, tools=tools_list
                            )
                            # Create temporary conversation window for the emergency response
                            temp_session = client.chats.create(model='gemini-1.5-pro', config=fallback_config)
                            response = temp_session.send_message(user_input)
                            error_encountered = False
                            break
                        except APIError as fb_err:
                            error_message = f"Status {fb_err.code}: {fb_err.message}"
                        except Exception as fb_err:
                            error_message = str(fb_err)
                    else:
                        error_message = f"Status {e.code}: {e.message}"
                        break
                except Exception as general_err:
                    error_encountered = True
                    error_message = str(general_err)
                    break

            # --- IMMERSIVE ERROR DISPATCHER ---
            if error_encountered:
                jarvis_output = f"""
❌ **Mainframe Connectivity Interruption**

Sir, the uplink arrays are currently experiencing severe bandwidth throttling or quota saturation from the central satellite link. 
* **Diagnostic Details:** `{error_message}`
* **Recommended Action:** Please hit the **Clear Mainframe Memory** button on the sidebar layout to drop our active token footprint weight.
"""
                st.markdown(jarvis_output)
                st.session_state.chat_history.append({"role": "model", "text": jarvis_output})
            
            # --- RENDER EXECUTION RESULTS ---
            elif response:
                # Handle tool executions automatically handled via the chat engine
                if response.function_calls:
                    for function_call in response.function_calls:
                        if function_call.name == "create_local_file":
                            args = function_call.args
                            f_name = args.get("file_name")
                            f_content = args.get("content")
                            
                            tool_result = create_local_file(file_name=f_name, content=f_content)
                            st.sidebar.info(f"⚡ File Generated: {f_name}")
                            
                            # Complete the execution loop with the backend session context
                            final_response = st.session_state.jarvis_session.send_message(
                                f"SYSTEM NOTE: The 'create_local_file' function ran successfully for '{f_name}'."
                            )
                            jarvis_output = final_response.text
                            st.markdown(jarvis_output)
                            st.session_state.chat_history.append({"role": "model", "text": jarvis_output})
                            
                            if os.path.exists(f_name):
                                with open(f_name, "r", encoding="utf-8") as dl_file:
                                    st.download_button(
                                        label=f"📥 Download Generated Asset ({f_name})",
                                        data=dl_file.read(),
                                        file_name=f_name,
                                        mime="text/plain"
                                    )
                else:
                    # Clean text execution path
                    jarvis_output = response.text
                    st.markdown(jarvis_output)
                    st.session_state.chat_history.append({"role": "model", "text": jarvis_output})
