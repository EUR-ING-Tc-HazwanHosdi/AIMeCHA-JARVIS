import os
import random
import re
import json
import streamlit as st

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
st.sidebar.error("Engine: Hardcoded Custom Python Core (No APIs / No Third Party Apps)")

# ==========================================
# FEATURE 3: HARDCODED LOCAL TOOLS ENGINE
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    """
    Generates and saves any kind of file needed entirely offline.
    """
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS"
    except Exception as e:
        return f"ERROR: {str(e)}"

# ==========================================
# NATIVE HARDCODED TEXT GENERATION ENGINE
# ==========================================
class HardcodedMarkovEngine:
    def __init__(self, corpus_text, state_size=2):
        self.state_size = state_size
        self.model = {}
        self.fit(corpus_text)
        
    def fit(self, text):
        # Tokenize words cleanly while keeping numbers and standard symbols
        words = re.findall(r'\b\w+\b|[:\-\.\(\)\>\<]', text.lower())
        
        for i in range(len(words) - self.state_size):
            state = tuple(words[i:i + self.state_size])
            next_word = words[i + self.state_size]
            
            if state not in self.model:
                self.model[state] = []
            self.model[state].append(next_word)
            
    def generate_response(self, user_prompt, max_words=80):
        # Standard witty Jarvis baseline prefixes to structure responses
        jarvis_banter = [
            "Right away, sir. Systems are optimized. Analyzing your request regarding ",
            "Parameters acknowledged, sir. Processing structural metrics for ",
            "I have run the diagnostic matrices for your inquiry regarding "
        ]
        
        response_prefix = random.choice(jarvis_banter) + f"'{user_prompt}'. "
        
        # Keyword token extractor
        input_words = re.findall(r'\b\w+\b', user_prompt.lower())
        seed_state = None
        
        for word in input_words:
            matching_states = [state for state in self.model.keys() if word in state]
            if matching_states:
                seed_state = random.choice(matching_states)
                break
                
        if not seed_state:
            seed_state = random.choice(list(self.model.keys()))
            
        generated_tokens = list(seed_state)
        current_state = seed_state
        
        for _ in range(max_words):
            if current_state in self.model:
                next_word = random.choice(self.model[current_state])
                generated_tokens.append(next_word)
                current_state = tuple(generated_tokens[-self.state_size:])
            else:
                break
                
        raw_output = " ".join(generated_tokens)
        cleaned_output = re.sub(r'\s+([:\-\.\(\)\>\<])', r'\1', raw_output)
        cleaned_output = re.sub(r'([:\-\.\(\)\>\<])\s+', r'\1', cleaned_output)
        
        sentences = cleaned_output.split('. ')
        capitalized_sentences = [s.capitalize() for s in sentences if s]
        base_body = ". ".join(capitalized_sentences) + "."
        
        # DETECT IF USER IS ASKING FOR A FILE ENHANCEMENT
        # If keywords match, we inject an explicit script block directly via our hardcoded response matrix
        file_attachment_block = ""
        if any(x in user_prompt.lower() for x in ["file", "script", "csv", "generate", "save"]):
            # Predict name based on search keywords
            predicted_filename = "msig_extracted_metrics.csv"
            if "script" in user_prompt.lower() or "python" in user_prompt.lower():
                predicted_filename = "compliance_checker.py"
                file_content = f"# Generated natively by J.A.R.V.I.S.\nprint('Executing local regulatory check for Malaysia MSIG...')\n"
            else:
                file_content = f"Metric,Value,Guideline_Reference\nPopulation_Equivalent_Residential,4,Volume_1\nBuffer_Zone_Under_1k_PE,20m,Volume_1\nMin_Gravity_Pipe_Dia,150mm,Volume_2\n"
            
            # Execute physical write
            status = create_local_file(predicted_filename, file_content)
            if status == "SUCCESS":
                file_attachment_block = f"|||ATTACHMENT:{predicted_filename}|||"

        return response_prefix + "\n\nBased on core architecture parameters: \n\n" + base_body + file_attachment_block

# ==========================================
# TEXT GENERATION ENGINE CORE CORPUS
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent engineering mainframe.
Population Equivalent PE calculation parameters. Residential is equal to 4 PE per unit. Office and Retail metrics equal 3 PE per 100 sqm space.
Siting Buffer Zones criteria requires distances. Systems less than 1k PE require 20m separation. Systems ranging 1k-5k PE require 25m buffer. Systems from 5k-50k PE mandate 30m distance boundaries from habitable structures.
Process Effluent Standards mandate strict parameters. Standard A dictates BOD < 10mg/L, TSS < 20mg/L, COD < 60mg/L, AMN < 5mg/L, O&G < 2mg/L. Standard B dictates BOD < 20mg/L, TSS < 40mg/L, COD < 100mg/L, AMN < 10mg/L, O&G < 5mg/L.
Whole Life Cycle Cost tracks a 50-year evaluation scaling capital assets and replacements using a 4% Discount Rate and 3% Growth Rate parameters.
Connection Rules dictate a mandatory public sewer line hookup if within 30m boundaries. Individual Septic Tanks are strictly restricted to PE < 150 allocations. Sewage Treatment Plants are mandated if PE > 150.
Individual Gravity Connections mandate a minimum pipeline diameter size >= 150 mm. Gradient boundaries must follow a strict range of 1 in 60 to 1 in 100. Maximum manhole interval distance equals 30m.
Depth of Cover requires 0.9m for non-traffic zones and 1.2m for traffic carriageways.
Septic Tank Design for systems <= 150 PE requires flow allocations of 225 L/capita/day. Absolute minimum operational capacity equals 2000 Litres. Chamber split criteria requires 2/3 space for the first chamber and 1/3 space for the second chamber. Liquid operational depth must fall between 1.2m to 1.8m boundaries. Freeboard headroom space must be >= 300 mm. T-piece submergence requires 300-450mm at the inlet and 200-300mm at the outlet arrays.
Secondary Soil Absorption networks require percolation rates between 1 to 60 mins/inch. Maximum absorption trench run length is <= 30m. Clear separation to the highest local water table must be >= 1.2m. Pipe gradient configurations must line up between 1 in 200 to 1 in 400.
Pipe Selection rules guarantee design lives >= 50 years. All structural fasteners must be SS304. Vitrified Clay public sewers require a minimum size of 225mm. Reinforced Concrete and GRP options are permitted only for line sizes >= 600mm with certified protective lining. No brick manholes are allowed. Pre-cast or in-situ Grade C30 or C35 concrete must be utilized.
Backdrop Criteria mandates an IL drop >= 900mm for line sizes <= 225mm and an IL drop >= 1000mm for pipes > 225mm. Maximum allowable manhole depth equals 9m. Depth settings > 6m require prior formal SPAN authorization approvals. Bolted steps are banned. Lightweight removable ladders must be utilized. Manhole covers situated on roads must be heavy-duty Class D400.
Testing Field Metrics demand an Air Test maximum loss <= 7 kPa for VC/RC, and <= 2 kPa for plastic options over 15 mins. Water test head parameters require 2m-7m measurements above the pipe crown. VC/RC line loss limits equal 1L/hour/linear-meter/meter-ID. CCTV diagnostics require 100% inspection for high risk depths >= 6m or diameters > 600mm. Grade 3-5 structural defects trigger automated rejections.
"""

if "hardcoded_engine" not in st.session_state:
    st.session_state.hardcoded_engine = HardcodedMarkovEngine(JARVIS_MASTER_PROMPT, state_size=2)

# ==========================================
# MULTI-TURN UI RENDERING LOGIC
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Custom Python Mainframe Core online, sir. No external handshakes or API dependencies active. I am computing entirely from native Python data blocks. Awaiting instructions."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Split tokens to avoid rendering raw system tags to user
        clean_display_text = message["content"].split("|||")[0]
        st.markdown(clean_display_text)

# ==========================================
# APPLICATION INTERCEPT & ENGINE INFERENCE
# ==========================================
if user_input := st.chat_input("Input local mainframe parameters..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Executing custom local text-generation algorithms..."):
            
            # Execute native mathematical textual engine calculation
            raw_jarvis_output = st.session_state.hardcoded_engine.generate_response(user_input)
            
            # Process clean string split for UI parsing
            display_text = raw_jarvis_output.split("|||")[0]
            st.markdown(display_text)
            
            # Save raw footprint to thread history
            st.session_state.messages.append({"role": "assistant", "content": raw_jarvis_output})
            
            # Catch structural download triggers if present in output token stream
            if "|||ATTACHMENT:" in raw_jarvis_output:
                extracted_name = raw_jarvis_output.split("|||ATTACHMENT:")[1].split("|||")[0]
                if os.path.exists(extracted_name):
                    st.sidebar.info(f"⚡ File Generated: {extracted_name}")
                    with open(extracted_name, "r", encoding="utf-8") as dl_file:
                        st.download_button(
                            label=f"📥 Download Generated Asset ({extracted_name})",
                            data=dl_file.read(),
                            file_name=extracted_name,
                            mime="text/plain"
                        )
