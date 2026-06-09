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
    page_title="J.A.R.V.I.S.", 
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

st.title("🤖 J.A.R.V.I.S. AI Engine")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Cognitive Core: ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")

# ==========================================
# MULTI-KEY POOL VERIFICATION & MANAGEMENT
# ==========================================
if "GEMINI_API_POOL" not in st.secrets:
    st.sidebar.error("GEMINI_API_POOL missing from Secrets configuration.")
    st.warning("Please pass your jarvis-1 to jarvis-5 array into the Streamlit Secret section box.")
    st.stop()

# Track exhausted keys persistently across session states
if "exhausted_keys" not in st.session_state:
    st.session_state.exhausted_keys = set()

api_key_pool = st.secrets["GEMINI_API_POOL"]
available_keys = [k for k in api_key_pool if k not in st.session_state.exhausted_keys]

# Display system status metrics in the sidebar
total_keys = len(api_key_pool)
dead_keys = len(st.session_state.exhausted_keys)
active_index = dead_keys + 1

if not available_keys:
    st.sidebar.error("Engine status: ALL CORES EXHAUSTED")
    st.error("🚨 CRITICAL METRIC EXHAUSTION: All 5 Jarvis core key tokens have been completely used up today.")
    st.stop()
else:
    st.sidebar.warning(f"Engine Core: Jarvis [{active_index}/{total_keys}] Active")
    st.sidebar.info(f"Runway: {total_keys - dead_keys} pristine fallback cores left.")

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
# COMMAND INTERCEPT & AUTOMATED ROUTING LOOP
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters via available cores..."):
            
            # Compile multi-turn raw chat strings
            formatted_contents = [msg["content"] for msg in st.session_state.messages]
            
            # Re-verify remaining operational keys at the moment of request execution
            available_keys = [k for k in st.secrets["GEMINI_API_POOL"] if k not in st.session_state.exhausted_keys]
            
            if not available_keys:
                st.error("🚨 ALL CORES OFFLINE: System quota depleted. Please reload pool settings.")
                st.stop()
            
            response = None
            successful_key = None
            
            # AUTOMATIC RUNTIME OVERRIDE SEQUENCING
            for active_key in available_keys:
                try:
                    # Form client handshake using the current targeted array string
                    client = genai.Client(api_key=active_key)
                    
                    config = types.GenerateContentConfig(
                        system_instruction=JARVIS_MASTER_PROMPT,
                        temperature=0.4,
                        tools=tools_list
                    )
                    
                    # Execute generation call
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-lite', 
                        contents=formatted_contents,
                        config=config
                    )
                    
                    # If execution succeeds without triggering an error block, lock the key and break
                    successful_key = active_key
                    break
                    
                except Exception as e:
                    error_str = str(e)
                    # Catch structural resource limitations or HTTP 429 exceptions explicitly
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        st.session_state.exhausted_keys.add(active_key)
                        st.sidebar.warning(f"Jarvis Core [{len(st.session_state.exhausted_keys)}] depleted. Switching link...")
                        continue  # Let loop move to next available token block automatically
                    else:
                        # Drop general code bugs, missing libraries or config faults straight down
                        st.error(f"Mainframe Core Disruption: {error_str}")
                        st.stop()
            
            # Ensure a valid response object was returned before proceeding to extract metrics
            if response:
                jarvis_output = ""
                
                # Check if the AI wants to execute a file creation tool
                if response.function_calls:
                    for function_call in response.function_calls:
                        if function_call.name == "create_local_file":
                            args = function_call.args
                            f_name = args.get("file_name")
                            f_content = args.get("content")
                            
                            # Execute the local tool execution script
                            tool_result = create_local_file(file_name=f_name, content=f_content)
                            st.sidebar.info(f"⚡ File Generated: {f_name}")
                            
                            # Notify the model using the same successful key channel to maintain state consistency
                            follow_up_contents = formatted_contents + [
                                f"SYSTEM NOTE: The 'create_local_file' function ran successfully for '{f_name}'."
                            ]
                            
                            try:
                                client = genai.Client(api_key=successful_key)
                                final_response = client.models.generate_content(
                                    model='gemini-2.5-flash-lite',
                                    contents=follow_up_contents,
                                    config=types.GenerateContentConfig(system_instruction=JARVIS_MASTER_PROMPT)
                                )
                                jarvis_output = final_response.text
                            except Exception as follow_up_err:
                                st.error(f"Follow-up Handshake Disruption: {str(follow_up_err)}")
                                st.stop()
                            
                            st.markdown(jarvis_output)
                            
                            # Provide download utility
                            if os.path.exists(f_name):
                                with open(f_name, "r", encoding="utf-8") as dl_file:
                                    st.download_button(
                                        label=f"📥 Download Generated Asset ({f_name})",
                                        data=dl_file.read(),
                                        file_name=f_name,
                                        mime="text/plain"
                                    )
                else:
                    # Standard text response output pipeline
                    jarvis_output = response.text
                    st.markdown(jarvis_output)
                
                # Append finalized assistant payload onto historical thread tracker array
                if jarvis_output:
                    st.session_state.messages.append({"role": "assistant", "content": jarvis_output})
                    # Force page state metrics refresh to accurately show updated key counts in sidebar
                    st.rerun()
