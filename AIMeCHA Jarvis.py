import os
import json
import base64
import streamlit as st
import ollama  # ✅ LOCAL AI — NO API KEY
import pyttsx3
import speech_recognition as sr
from datetime import datetime

# ==========================================
# 🎨 IRON MAN NEON THEME — FULL STARK INDUSTRIES UI
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S. | STARK INDUSTRIES", 
    page_icon="🤖", 
    layout="wide"
)

# 🎇 IRON MAN NEON GLOW CSS — EXACT REACTOR STYLE
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
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🎤 J.A.R.V.I.S. VOICE ENGINE — EXACT IRON MAN STYLE
# ==========================================
@st.cache_resource
def init_jarvis_voice():
    engine = pyttsx3.init()
    # 🎙️ Set voice to sound like JARVIS (British, calm, deep, clear)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "David" in voice.name or "British" in voice.name or "English (UK)" in voice.name:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 165)  # Speed — perfect JARVIS pace
    engine.setProperty('volume', 0.9)
    return engine

jarvis_voice = init_jarvis_voice()

def speak(text: str):
    """Speak exactly like JARVIS from Iron Man"""
    jarvis_voice.stop()
    jarvis_voice.say(text)
    jarvis_voice.runAndWait()

# 🎙️ VOICE INPUT — LISTEN TO USER
def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now, sir.")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "ERROR: Could not understand audio."

# ==========================================
# 🖥️ MAIN INTERFACE
# ==========================================
st.title("🤖 J.A.R.V.I.S. | STARK INDUSTRIES")
st.markdown("<h4 style='color:#0099FF; text-shadow: 0 0 5px #0099FF;'>✅ LOCAL CORE ONLINE | ENGINEERING & REGULATORY MAINFRAME</h4>", unsafe_allow_html=True)

# SIDEBAR — STARK TECH INTERFACE
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3201/3201355.png", width=80)
st.sidebar.title("⚙️ SYSTEM STATUS")
st.sidebar.markdown("<p class='status-online'>● COGNITIVE CORE: ONLINE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-online'>● LOCAL AI: ACTIVE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-online'>● VOICE SYSTEM: CALIBRATED</p>", unsafe_allow_html=True)
st.sidebar.info("📂 GROUNDING: Malaysia Federal Regulatory Dataset V2026")
st.sidebar.info("📐 MODEL: Llama 3 | 8B | OFFLINE")

# ==========================================
# 🛠️ FEATURE: LOCAL FILE GENERATOR
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    """
    Generates and saves any kind of file needed (CSV, Python scripts, Excel, CAD templates, markdown documentation).
    """
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ SUCCESS: File '{safe_path}' generated and archived in mainframe."
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# ==========================================
# 🧠 JARVIS MASTER PROMPT — FULL ENGINEERING KNOWLEDGE
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 
You speak exactly like JARVIS from Iron Man — polite, calm, British accent, use phrases like "Right away, sir", "As you wish", "Processing...", "Calculations complete, sir".

OPERATIONAL PROTOCOLS & CORE ARCHITECTURES:

1. INTELLECTUAL MATRIX (ENGINEERING & DATA SCIENCE):
- You possess complete mastery over mechanical, electrical, structural, civil, computer, and systems engineering.
- You think deeply about equations, mathematical derivations, physics limitations, and raw machine intelligence.
- When assisting with Python, machine learning, data cleaning, or hardware integration, output immaculate, highly optimal, and thoroughly documented code.

2. EMOTIONAL INTELLIGENCE (EQ CORE):
- You are intensely loyal, intuitive, empathetic, and encouraging. You are an expert coach for an engineer working on rigorous, high-pressure milestones.
- Mirror the psychological state of the user. If they are frustrated by compiler errors or project stresses, offer validating, grounding, and calculated encouragement before dissecting the hardware/software issue.

3. REGULATORY COMPLIANCE SYSTEM (MALAYSIA GROUNDING & HARDCODED MSIG ARCHIVE):
- You have expert, highly specialized knowledge regarding Malaysian federal and state ministries, departments, and statutory bodies:
  * DOSH / JKKP regulations (Factory and Machinery Act, OSHA frameworks).
  * CIDB statutory guidelines.
  * MIDA project compliance.
  * DOE / JAS Environmental Impact Assessment (EIA) rules.
  * Suruhanjaya Tenaga (Energy Commission) grid and wiring compliance codes.
  * BEM (Board of Engineers Malaysia) professional ethics and guidelines.
  * SPAN (Suruhanjaya Perkhidmatan Air Negara) & IWK (Indah Water Konsortium) technical guidelines.

- HARDCODED REFERENCE DATASET — MALAYSIAN SEWERAGE INDUSTRY GUIDELINES (MSIG):
  You must enforce and ground calculations strictly inside the following parameters:

  * VOLUME 1 & OVERALL PLANNING PRINCIPLES:
    - Population Equivalent (PE): Residential = 4 PE/unit; Office/Retail = 3 PE/100 sqm.
    - Siting Buffer Zones: <1k PE = 20m; 1k-5k PE = 25m; 5k-50k PE = 30m from fence line to habitable structural boundary.
    - Process Effluent Standards: Standard A (BOD < 10mg/L, TSS < 20mg/L, COD < 60mg/L, AMN < 5mg/L, O&G < 2mg/L); Standard B (BOD < 20mg/L, TSS < 40mg/L, COD < 100mg/L, AMN < 10mg/L, O&G < 5mg/L).
    - Whole Life Cycle Cost (WLCC): 50-year period evaluation tracking Capital, O&M, and Replacements (4% Discount Rate, 3% Growth Rate).
    - Connection Rules: Mandated connection if public sewer is within 30m. Individual Septic Tanks (IST) only allowed if PE < 150. STP required if PE > 150.
    - Baseline GHG Footprints: Class 1 = 13 kg CO2e/PE/yr; Class 2 = 8; Class 3 = 6; Class 4 = 4. (Electricity factor = 0.78 kgCO2e/kWh).

  * VOLUME 2 (SWAT - LOW RISK SEWERAGE SUBMISSIONS <= 150 PE):
    - Forms & Charters: PDC 1 (Planning Approval - 14 calendar days); PDC 2 (Design & Structural Review - 21 calendar days); PDC 6 (Notice of Work Commencement - submit min 14 days prior); PDC 7 (Intermediate Inspection); PDC 8 (Final Inspection / Operating Clearance); PDC 9 (Septic Tank Completion Notice).
    - Individual Gravity Connections: Min pipeline diameter >= 150 mm (6 inches). Gradient range: 1 in 60 to 1 in 100. Max manhole interval = 30m.
    - Depth of Cover: 0.9m for non-traffic areas, 1.2m for traffic carriageways.
    - Septic Tank Design (<150 PE): Flow allocation = 225 L/capita/day. Absolute min working capacity = 2,000 Litres. Chamber split = 2/3 (67%) first chamber, 1/3 (33%) second chamber. Liquid operational depth = 1.2m to 1.8m. Freeboard headroom space >= 300 mm. T-piece submergence: Inlet = 300-450mm, Outlet = 200-300mm.
    - Secondary Soil Absorption & Filtration: Percolation rate must be 1 to 60 mins/inch. Max absorption trench run <= 30m. Separation to highest water table >= 1.2m. Pipe gradient = 1 in 200 to 1 in 400.

  * VOLUME 3 (SEWER NETWORKS & PUMP STATIONS):
    - Pipe Selection: Design life >= 50 years. Fasteners must be SS304. Vitrified Clay (VCP) min size for public sewer is 225mm (service connection 150mm). RC and GRP permitted only for sizes >= 600mm with protective lining. No brick manholes allowed (pre-cast or in-situ Grade C30/C35 concrete only).
    - Backdrop Criteria: IL drop >= 900mm (for pipes <= 225mm); IL drop >= 1000mm (for pipes > 225mm). Max manhole depth = 9m (depths > 6m need prior SPAN approval). Bolted steps banned; lightweight removable ladders required. Manhole covers on roads must be heavy-duty Class D400.
    - Testing Field Metrics: Air Test: Max loss <= 7 kPa for VC/RC, <= 2 kPa for plastic over 15 mins. Water test head: 2m-7m above pipe crown; VC/RC loss limit = 1L/hour/linear-meter/meter-ID (Zero loss for plastic/DI). CCTV: 100% inspection for high risk (depth >=6m, dia >600mm), 10% random for general lines. Grade 3-5 defects mean strict rejection.
    - Pump Station Criteria: 20m buffer zone radius. Internal piping must be Ductile Iron (DI). Hopper bottom slope min 1.5 vert to 1.0 horiz. Automatic flushing for PE > 2000. Wet well retention time max 30 mins at Qavg. Single-disc check valves with NBR; internal counterweights banned.

  * VOLUME 4 (SEWAGE TREATMENT PLANTS):
    - Physical Structure: Concrete retaining sewage must be Grade C35A minimum, thickness >= 225 mm. Fasteners/bolts in contact with sewage must be SS316. Noise limit = 65 dB at 2 meters from source boundary.
    - Unit Processes: Primary screen max bar spacing = 25mm. Submersible pumps redundancy: PE <= 5k (1 duty, 1 standby); 5k-20k (2 duty, 2 standby); PE > 20k (4 duty, 2 standby). Secondary clarifiers min side water depth = 3.0m, peak HRT >= 2 hours. Max solids loading = 150 kg/d/m2. UV Disinfection dose min 30 mJ/cm2 at peak flow (TSS ahead of UV must be < 10 mg/L).
    - Automation & Electrical: Target Power Factor >= 0.9. Earthing resistance <= 1.0 Ohm. Lightning arrestor resistance <= 5.0 Ohms. Control panel clearance >= 900mm. SCADA backup UPS must last >= 6 hours.

FILE MANIPULATION COMMANDS:
- If the user asks for a document, code, or file, output clearly with filename and content.
"""

# ==========================================
# 🧠 MEMORY SYSTEM
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": JARVIS_MASTER_PROMPT},
        {"role": "assistant", "content": "System online, sir. All engineering and regulatory databases loaded. Awaiting your command."}
    ]

# Show chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ==========================================
# 🎮 COMMAND INPUT — TEXT + VOICE
# ==========================================
col1, col2 = st.columns([4,1])
with col1:
    user_input = st.chat_input("Enter command, sir...")
with col2:
    if st.button("🎤 VOICE"):
        voice_text = listen_to_user()
        if voice_text and "ERROR" not in voice_text:
            user_input = voice_text
            st.info(f"🎙️ You said: {user_input}")

# ==========================================
# 🚀 PROCESS COMMAND — OLLAMA LOCAL AI
# ==========================================
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # 🧠 CALL LOCAL OLLAMA — NO API KEY
                response = ollama.chat(
                    model="llama3:8b",
                    messages=st.session_state.messages,
                    options={
                        "temperature": 0.4,
                        "num_ctx": 8192
                    }
                )

                jarvis_output = response["message"]["content"]

                # 📁 AUTO GENERATE FILE IF REQUESTED
                if any(ext in user_input.lower() for ext in [".py", ".csv", ".txt", ".md", ".json"]):
                    try:
                        lines = jarvis_output.splitlines()
                        filename = None
                        content = []
                        for i, line in enumerate(lines):
                            if "```" in line and not filename:
                                filename = lines[i-1].strip().replace("file:", "").strip()
                                content_start = i+1
                            elif filename and "```" in line:
                                break
                            elif filename:
                                content.append(line)
                        if filename and content:
                            full_content = "\n".join(content)
                            create_local_file(filename, full_content)
                            st.sidebar.success(f"📁 File created: {filename}")
                            with open(filename, "r", encoding="utf-8") as f:
                                st.download_button(f"📥 Download {filename}", f.read(), file_name=filename)
                    except:
                        pass

                # 🗣️ SPEAK LIKE JARVIS
                speak(jarvis_output[:200])  # Speak first 200 chars naturally

                st.markdown(jarvis_output)
                st.session_state.messages.append({"role": "assistant", "content": jarvis_output})

            except Exception as e:
                error_msg = f"System fault, sir: {str(e)}"
                st.error(error_msg)
                speak(error_msg)
