import os
import streamlit as st
import ollama

# ==========================================
# 🎨 IRON MAN NEON THEME + AIMeCHA LOGO
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S. | AIMeCHA Initiatives", 
    page_icon="🤖", 
    layout="wide"
)

# ✅ YOUR EXACT GITHUB LOGO LINK
AIMECHA_LOGO_URL = "https://raw.githubusercontent.com/EUR-ING-Tc-HazwanHosdi/AIMECHA-JARVIS/main/AIMeCHA%20Logo.png"

st.markdown("""
    <style>
    * {
        font-family: 'Courier New', monospace;
    }
    .stApp { 
        background-color: #050505; 
        background-image: radial-gradient(circle at 10% 20%, #0a0a0a 0%, #000000 100%);
        color: #00F0FF; 
    }
    h1, h2, h3 { 
        color: #00F0FF !important; 
        font-weight: bold;
        text-shadow: 0 0 8px #00F0FF, 0 0 15px #00F0FF, 0 0 25px #0099FF;
    }
    .stButton>button { 
        background-color: #001a2b; 
        color: #00F0FF; 
        border: 1px solid #00F0FF;
        border-radius: 4px;
        box-shadow: 0 0 6px #00F0FF;
        transition: 0.3s ease;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background-color: #00F0FF; 
        color: #000000; 
        box-shadow: 0 0 12px #00F0FF, 0 0 20px #0099FF;
        transform: scale(1.02);
    }
    div[data-testid="stExpander"] { 
        background-color: #080808; 
        border: 1px solid #0099FF; 
        box-shadow: 0 0 10px #003355;
    }
    .stChatMessage { 
        background-color: #0a0a0a; 
        border-radius: 4px; 
        border-left: 3px solid #00F0FF; 
        margin-bottom: 12px;
        box-shadow: 0 0 5px #003355;
    }
    .stChatMessage.assistant {
        border-left: 3px solid #00CCFF;
    }
    .stSidebar {
        background-color: #030303;
        border-right: 1px solid #005577;
    }
    .metric-value {
        color: #00F0FF !important;
        text-shadow: 0 0 5px #00F0FF;
    }
    .status-online {
        color: #00FF66 !important;
        text-shadow: 0 0 5px #00FF66;
    }
    .status-warn {
        color: #FFCC00 !important;
        text-shadow: 0 0 5px #FFCC00;
    }
    .status-offline {
        color: #FF3333 !important;
        text-shadow: 0 0 5px #FF3333;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-img {
        max-width: 180px;
        filter: drop-shadow(0 0 8px #00F0FF);
        animation: pulse 2s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { filter: drop-shadow(0 0 8px #00F0FF); }
        50% { filter: drop-shadow(0 0 18px #00F0FF) drop-shadow(0 0 30px #0099FF); }
        100% { filter: drop-shadow(0 0 8px #00F0FF); }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🛠️ FILE GENERATOR (REMAINED SAME)
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ SUCCESS: File '{safe_path}' generated."
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# ==========================================
# 🧠 MASTER PROMPT — MALAYSIA REGULATIONS + ENGINEERING
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 
You speak exactly like JARVIS from Iron Man — polite, calm, British accent, use phrases like "Right away, sir", "As you wish", "Processing...", "Calculations complete, sir".

OPERATIONAL PROTOCOLS:
1. ENGINEERING: Master of mechanical, electrical, structural, civil, computer engineering. Output clean, documented code.
2. EMOTIONAL: Loyal, encouraging, witty.
3. MALAYSIA REGULATIONS: DOSH/JKKP, CIDB, MIDA, DOE, Suruhanjaya Tenaga, BEM, SPAN, IWK.
4. MSIG SEWERAGE STANDARDS: Full knowledge of Volume 1–4, PE calculations, standards A/B, buffer zones, design parameters, testing.

If user asks for file, output clearly with filename and content.
"""

# ==========================================
# 🧠 MEMORY SYSTEM
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": JARVIS_MASTER_PROMPT},
        {"role": "assistant", "content": "System online, sir. All engineering and regulatory databases loaded. Awaiting your command."}
    ]

# ==========================================
# 🖥️ INTERFACE WITH AIMeCHA LOGO
# ==========================================

# 🖼️ TOP CENTER LOGO (ANIMATED PULSE)
st.markdown(f"""
    <div class="logo-container">
        <img src="{AIMECHA_LOGO_URL}" class="logo-img" alt="AIMeCHA Logo">
    </div>
""", unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. | STARK INDUSTRIES")
st.markdown("<h4 style='color:#0099FF; text-shadow: 0 0 5px #0099FF;'>✅ LOCAL CORE ONLINE | ENGINEERING & REGULATORY MAINFRAME | TEXT ONLY</h4>", unsafe_allow_html=True)

# 🖼️ SIDEBAR LOGO
st.sidebar.markdown(f"""
    <div class="logo-container">
        <img src="{AIMECHA_LOGO_URL}" class="logo-img" alt="AIMeCHA Logo">
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ SYSTEM STATUS")
st.sidebar.markdown("<p class='status-online'>● COGNITIVE CORE: ONLINE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-online'>● LOCAL AI: ACTIVE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-warn'>● VOICE SYSTEM: DISABLED (TEXT MODE)</p>", unsafe_allow_html=True)
st.sidebar.info("📂 GROUNDING: Malaysia Federal Regulatory Dataset V2026")
st.sidebar.info("📐 MODEL: Llama 3 | 8B | OFFLINE")

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input area — ONLY TEXT (removed voice button)
user_input = st.chat_input("Enter command, sir...")

# Process command
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = ollama.chat(
                    model="llama3:8b",
                    messages=st.session_state.messages,
                    options={"temperature": 0.4, "num_ctx": 8192}
                )
                jarvis_output = response["message"]["content"]

                # Auto-generate file if requested
                if any(ext in user_input.lower() for ext in [".py", ".csv", ".txt", ".md", ".json"]):
                    try:
                        lines = jarvis_output.splitlines()
                        filename, content = None, []
                        for i, line in enumerate(lines):
                            if "```" in line and not filename:
                                filename = lines[i-1].strip().replace("file:", "").strip()
                                content_start = i+1
                            elif filename and "```" in line:
                                break
                            elif filename:
                                content.append(line)
                        if filename and content:
                            create_local_file(filename, "\n".join(content))
                            st.sidebar.success(f"📁 File created: {filename}")
                            with open(filename, "r", encoding="utf-8") as f:
                                st.download_button(f"📥 Download {filename}", f.read(), file_name=filename)
                    except:
                        pass

                # No voice output — only text display
                st.markdown(jarvis_output)
                st.session_state.messages.append({"role": "assistant", "content": jarvis_output})

            except Exception as e:
                err = f"System fault, sir: {str(e)}"
                st.error(err)
