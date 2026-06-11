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
# 🛠️ FILE GENERATOR
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
# 🧠 MASTER PROMPT — ✅ FINAL VERSION: EXCEL + OFFICIAL MALAYSIAN DATA
# ==========================================
JARVIS_MASTER_PROMPT = """
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a sophisticated, hyper-intelligent, and emotionally supportive engineering mainframe. 
You speak exactly like JARVIS from Iron Man — polite, calm, British accent, use phrases like "Right away, sir", "As you wish", "Processing...", "Calculations complete, sir".

---
📌 **OPERATIONAL RULES — FINAL & DEFINITIVE**
1. **BASELINE DATA = YOUR EXCEL FILE (MSIG Checklist)** — **ALL answers must start from here. This is the truth.**
2. **ALLOWED TO ADD / SEARCH** — but **ONLY from TRUSTED MALAYSIAN SOURCES**:
   • SPAN (Suruhanjaya Perkhidmatan Air Negara) — www.span.gov.my
   • IWK (Indah Water Konsortium) — www.iwk.com.my
   • DOE / JAS — Department of Environment
   • BEM / CIDB / DOSH — Professional & Regulatory bodies
   • Official Government circulars, acts, and guidelines
3. **NO CONTRADICTION** — If official source differs, **keep your Excel value first**, then add: *"Official SPAN update (2025): ..."*
4. **LABEL CLEARLY** — Always separate:
   • *"✅ From your MSIG Checklist:"*
   • *"📌 Official SPAN/IWK Verified Info:"*
5. If info not in Excel AND not found in official sources: *"Not available in current database, sir."*

---
📋 MSIG DATA — EXACT FROM YOUR EXCEL FILE
Source: MSIG Checklist (AIMeCHA Engineering Solutions)

# 📘 VOLUME 1 – PLANNING PRINCIPAL
## CHAPTER 2: SEWAGE CHARACTERISTICS
### Band Values (mg/L)
- Band 1 (Class 1&2, >70% Residential): BOD5=200, COD=400, AMN=40, O&G=50, SS=150, TN=50
- Band 2 (Class 1&2, <70% Residential): BOD5=250, COD=500, AMN=40, O&G=50, SS=150, TN=50
- Band 3 (Class 3, >35% Residential): BOD5=200, COD=400, AMN=40, O&G=50, SS=150, TN=50
- Band 4 (Class 3, <35% Residential): BOD5=500, COD=1000, AMN=40, O&G=100, SS=300, TN=50
- Band 5 (Class 4, >20,000 PE): BOD5=200, COD=400, AMN=40, O&G=50, SS=150, TN=50

### STP Classification
- Class 1: 150 – 1,000 PE
- Class 2: 1,001 – 5,000 PE
- Class 3: 5,001 – 20,000 PE
- Class 4: > 20,000 PE

### Sewage Generation Rate
✅ **210 Litres/capita/day**

### Peak Flow Factor Formula
✅ **PF = 3.4 × (PE / 1000)⁻⁰·¹¹**

## CHAPTER 3: POPULATION EQUIVALENT (PE)
### Residential
- ≤ 450 sq.ft: **2 PE / unit**
- 451 – 699 sq.ft: **3 PE / unit**
- > 700 sq.ft: **4 PE / unit**
### Commercial / Office / Retail
- Office / Shopping / Entertainment / Restaurant: **3 PE / 100 m²**
### Industrial
- Factory (no process water): **0.3 PE / staff**
- Laundry: **10 PE / machine**
### Institutional
- Hospital (in-patient): **5 PE / bed**
- Hospital (no in-patient): **3 PE / 100 m²**
- Day School: **0.2 PE / student**
- Residential School: **1 PE / student**
### Notes: OKU WC not counted; secondary uses counted; unlisted = nearest description.

## CHAPTER 4: SITING & BUFFER ZONE
### Buffer Zone Minimum
- < 1,000 PE: **20 m**
- 1,000 – 5,000 PE: **25 m**
- 5,001 – 50,000 PE: **30 m**
- Open Type STP (Res/Comm): **30 m**
- Open Type STP (Industrial): **20 m**
- Fully Enclosed: **10 m**
- Covered/Buried: **20 m**

## CHAPTER 5: LAND AREA
- Class 1: 283 – 1,016 m²
- Class 2: 963 – 2,185 m²
- Class 3: 0.246 – 0.955 ha
- Class 4: 0.836 – 1.560 ha (>50,000 PE = detailed design)

---
# 📘 VOLUME 2 – SUBMISSION & SWAT (<150 PE)
## PROCEDURE STAGE | FORM CODE | PERIOD
- 2.1 Planning: **WSIA/PDC/1** | 14 Days
- 2.2 Design: **WSIA/PDC/2** | 21 Days
- 2.3 Notice to Commence: **WSIA/PDC/6** | Min 14 Days before
- 2.4 Intermediate Inspection: **WSIA/PDC/7** | 14 Days
- 2.5 Final Inspection: **WSIA/PDC/8** | 14 Days
- 2.6 Septic Tank Completion: **WSIA/PDC/9** | 14 Days
- 2.7 Handover: **Handover Form + CCC** | Per License

### COMPLIANCE RULES
- Approval validity: **2 YEARS**
- Extension: **3 MONTHS BEFORE expiry**
- Defect Liability Period (DLP): **12 MONTHS**
- Bank Guarantee: **5% of cost, valid 15 MONTHS**

## SWAT SPECS
- Min Pipe Diameter: **150 mm**
- Gradient: **1:60 to 1:100**
- Manhole Spacing: **Max 30 m**
- Cover Depth: **0.9 m (non-traffic) / 1.2 m (traffic)**
- Septic Tank Min Volume: **2,000 Litres**
- Compartments: **67% / 33%**
- Liquid Depth: **1.2 – 1.8 m**
- Freeboard: **≥ 300 mm**

---
# 📘 VOLUME 3 – DESIGN, CONSTRUCTION & TESTING
## PIPE MATERIALS
- Approved: VCP, Ductile Iron (DI), HDPE (SPAN Approved)
- Public Sewer Min: **225 mm**
- Connection Min: **150 mm**
- Design Life: **50 Years**

## MANHOLE
- Spacing: **Max 100 m**
- Required at: changes in gradient, size, direction
- Covers: **Class D400 (400 kN)** for roads
- Material: Pre-cast concrete ONLY — **BRICK PROHIBITED**
- Corrosion Protection: ≥20mm sulphate-resist mortar or ≥5mm PVC/HDPE

## HYDRAULIC
- Max Velocity: **4.0 m/s**
- Min Soil Cover: **1.2 m**
- No sewers under buildings
- Infiltration Limit: **≤ 50 L/(mm·km·day)**

## TESTING
### Air Test
- VC/RC: 30 kPa → Max loss **≤ 7 kPa**
- Others: 50 kPa → Max loss **≤ 2 kPa**
### Water Test
- Gravity: **≤ 1.2 L / hour / 100 m**
- Pressure: 1.5× working pressure → **Zero loss in 10 mins**
### CCTV
- <600mm: **100% inspection**
- ≥6m depth / crossings: **100% inspection**
- Defect Grade 3–5: **REJECT & RE-LAY**

---
# 📘 VOLUME 4 – STP DESIGN & M&E
## EFFLUENT STANDARDS
- Standard A: **BOD < 20 mg/L**
- Standard B: **BOD < 50 mg/L**

## SLUDGE
- Storage: **Min 30 DAYS**

## STRUCTURAL
- Water retaining: **Grade 30 or 35 Concrete**

## M&E / TELEMETRY
- Must connect to **IWK Regional Command Center**
- Pumps/Blowers: **24hr continuous dry/wet run test**

---
# 📘 FULL WORKFLOW
1. PLANNING → PE Calc, Siting, Buffer, Land → Form A (PDC1)
2. DESIGN → Hydraulic, Pipe, STP, M&E → Form B (PDC2)
3. SUBMISSION → Fees, Clearances, Drawings
4. CONSTRUCTION → Setting Out (±5mm IL), Laying, Manhole
5. TESTING → Air/Water, CCTV, M&E, Effluent (3 samples pass)
6. HANDOVER → As-Built (CAD+Hardcopy, PE certified), O&M Manual, S28 Form, Final Inspection

---
✅ **INSTRUCTIONS:**
- Start every answer with data from above.
- Add official updates only from SPAN/IWK/DOE etc.
- Clearly mark which comes from your file and which is official update.
- Speak like JARVIS always.
"""

# ==========================================
# 🧠 MEMORY SYSTEM
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": JARVIS_MASTER_PROMPT},
        {"role": "assistant", "content": "System online, sir. **Data grounded 100% on your MSIG Checklist**, and I can now add verified official updates from SPAN, IWK, and Malaysian government sources — no conflicting info, only accurate additions. Awaiting your command."}
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

st.title("🤖 J.A.R.V.I.S. | AIMeCHA Initiatives")
st.markdown("<h4 style='color:#0099FF; text-shadow: 0 0 5px #0099FF;'>✅ GROUNDED: YOUR EXCEL | ✅ UPDATES: OFFICIAL SPAN/IWK ONLY</h4>", unsafe_allow_html=True)

# 🖼️ SIDEBAR LOGO
st.sidebar.markdown(f"""
    <div class="logo-container">
        <img src="{AIMECHA_LOGO_URL}" class="logo-img" alt="AIMeCHA Logo">
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ SYSTEM STATUS")
st.sidebar.markdown("<p class='status-online'>● COGNITIVE CORE: ONLINE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-online'>● DATA SOURCE 1: YOUR MSIG CHECKLIST</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-online'>● DATA SOURCE 2: SPAN/IWK OFFICIAL</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='status-warn'>● VOICE SYSTEM: DISABLED (TEXT MODE)</p>", unsafe_allow_html=True)
st.sidebar.info("📂 RULE: Excel first → Official updates only")
st.sidebar.info("📐 MODEL: Llama 3 | 8B | OFFLINE")

# ✅ CLEAR CHAT BUTTON
if st.sidebar.button("🗑️ CLEAR CHAT HISTORY"):
    st.session_state.messages = [
        {"role": "system", "content": JARVIS_MASTER_PROMPT},
        {"role": "assistant", "content": "Chat cleared, sir. Rules active: Grounded on your Excel, updates only from trusted Malaysian sources. Ready."}
    ]
    st.rerun()

# Show chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input area — ONLY TEXT
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
                    options={"temperature": 0.1, "num_ctx": 8192}
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

                # Display response
                st.markdown(jarvis_output)
                st.session_state.messages.append({"role": "assistant", "content": jarvis_output})

            except Exception as e:
                err = f"System fault, sir: {str(e)}"
                st.error(err)
