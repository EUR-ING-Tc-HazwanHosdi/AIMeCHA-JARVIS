import os
import json
import base64
import streamlit as st
from openai import OpenAI

# ==========================================
# PAGE CONFIGURATION & A.I.M.E.C.H.A. UI
# ==========================================
st.set_page_config(page_title="J.A.R.V.I.S. | A.I.M.E.C.H.A.", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { 
        background-color: #050B14; 
        color: #E2F1F8; 
        font-family: 'Orbitron', sans-serif; 
    }
    
    /* NEON GLOW EFFECTS */
    .stApp {
        background: radial-gradient(circle at center, #0B1E30 0%, #050B14 70%);
    }

    h1, h2, h3 { 
        color: #00E5FF !important; 
        text-transform: uppercase; 
        letter-spacing: 4px; 
        text-shadow: 0 0 10px #00E5FF, 0 0 20px #00E5FF;
    }

    /* ARC REACTOR HUD BUTTONS */
    .stButton>button { 
        background-color: #002B3D; 
        color: #00E5FF; 
        border: 2px solid #00E5FF; 
        box-shadow: 0 0 10px #00E5FF;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #00E5FF; 
        color: #050B14; 
        box-shadow: 0 0 30px #00E5FF;
    }

    /* CHAT BUBBLE GLOW */
    .stChatMessage { 
        background-color: #0A192F; 
        border: 1px solid #005B7F;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
        border-left: 5px solid #00E5FF;
    }

    /* SIDEBAR HUD */
    .stSidebar {
        border-right: 2px solid #00E5FF;
        box-shadow: 5px 0 15px rgba(0, 229, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER WITH A.I.M.E.C.H.A. LOGO
# ==========================================
header_col1, header_col2 = st.columns([5, 12])

with header_col1:
    logo_path = "AIMeCHA Logo.png"
    if os.path.exists(logo_path):
        # Everything here must be indented 4 spaces relative to 'if'
        st.markdown('<div class="logo-glow">', unsafe_allow_html=True)
        st.image(logo_path, width=300)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Logo file missing.")

with header_col2:
    st.markdown("<h1>🤖 J.A.R.V.I.S. AI Engine</h1>", unsafe_allow_html=True)
    
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")


# ==========================================
# INITIALIZE OPENAI CLIENT
# ==========================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("🚨 CRITICAL: OPENAI_API_KEY not found in system secrets.")
    st.stop()

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated engineering mainframe..."},
        {"role": "assistant", "content": "A.I.M.E.C.H.A. framework online. Awaiting your instructions, sir."}
    ]

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
- You have access to a custom tool called 'create_local_file'. If the user asks for a document, an engine schematic, a dataset layout, a CAD profile skeleton, or code, execute 'create_local_file' immediately to build it for them.
"""

# ==========================================
# MULTI-TURN MEMORY LOGIC
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. framework fully initialized. Multi-key automated backup array online. Awaiting your instructions, sir."}
    ]

# Display persistent session stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# COMMAND INTERCEPT & ROUTING (OPENAI VERSION)
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            # Call OpenAI with tools
            response = client.chat.completions.create(
                model="gpt-4o", # Or gpt-4o-mini
                messages=st.session_state.messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "create_local_file",
                        "description": "Generate and save a file.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_name": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["file_name", "content"]
                        }
                    }
                }]
            )

            msg = response.choices[0].message
            
            if msg.tool_calls:
                # Handle file generation
                tool_call = msg.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                result = create_local_file(args['file_name'], args['content'])
                st.sidebar.info(f"⚡ {result}")
                st.markdown(f"**Task Executed:** {result}")
                
                # Provide download button if the file exists
                if os.path.exists(args['file_name']):
                    with open(args['file_name'], "rb") as f:
                        st.download_button("📥 Download Asset", f, file_name=args['file_name'])
            else:
                # Handle text response
                st.markdown(msg.content)
                st.session_state.messages.append({"role": "assistant", "content": msg.content})
