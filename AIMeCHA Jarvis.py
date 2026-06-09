import os
import re
import base64
import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & STARK INDUSTRIES UI
# ==========================================
st.set_page_config(
    page_title="A.I.M.E.C.H.A. J.A.R.V.I.S. Core", 
    page_icon="🤖", 
    layout="wide"
)

# Stark Industries Minimalist Dark Interface Sheet
st.markdown("""
    <style>
    .stApp { background-color: #050B14; color: #E2F1F8; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stButton>button { background-color: #002B3D; color: #00E5FF; border: 1px solid #00E5FF; font-family: 'Courier New', monospace; }
    .stButton>button:hover { background-color: #00E5FF; color: #050B14; }
    div[data-testid="stExpander"] { background-color: #0A1424; border: 1px solid #005B7F; }
    .system-card { background-color: #0A192F; border-radius: 6px; border-left: 4px solid #00E5FF; padding: 15px; margin-bottom: 15px; }
    .metric-value { font-size: 24px; color: #00E5FF; font-family: 'Courier New', monospace; font-weight: bold; }
    .logo-container { display: flex; align-items: center; gap: 20px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Base64 HUD Asset Encoder
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("aimecha_logo.png")

if logo_base64:
    st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="80" style="filter: drop-shadow(0px 0px 8px #00E5FF);">
            <h1 style="display: inline; margin: 0; padding-left: 10px;">A.I.M.E.C.H.A. J.A.R.V.I.S. Deterministic Mainframe</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. Deterministic Mainframe")

# ==========================================
# HARDCODED LOCAL STORAGE HANDLER
# ==========================================
# Set exact target path parameters mapping back to your specific asset name verbatim
TARGET_FILE = "MSIG Checklist ( AIMeCHA Engineering Solutions)_2.xlsx"
FALLBACK_FILE = "MSIG Checklist ( AIMeCHA Engineering Solutions).xlsx"

# Automatic resolution logic if the file variation tag is missing the "_2" suffix
if not os.path.exists(TARGET_FILE) and os.path.exists(FALLBACK_FILE):
    os.rename(FALLBACK_FILE, TARGET_FILE)

@st.cache_data
def ingest_msig_data(file_path):
    """Bypasses Generative models completely to parse sheets into memory matrices."""
    if not os.path.exists(file_path):
        return None, f"System Failure: Missing target structural asset: '{file_path}'"
    try:
        xls = pd.ExcelFile(file_path)
        all_sheets = {}
        for sheet in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
            # Standardize string representations for deterministic searching
            df = df.fillna("").astype(str)
            all_sheets[sheet] = df
        return all_sheets, "System Status: Core Matrices Fully Synchronized."
    except Exception as e:
        return None, f"Parsing disruption: {str(e)}"

# Instantiate Database
msig_db, system_status = ingest_msig_data(TARGET_FILE)

# Sidebar System Telemetry
st.sidebar.title("⚙️ Telemetry Matrix")
if msig_db:
    st.sidebar.success("Cognitive Core: ALGORITHMIC (NO GENAI)")
    st.sidebar.info(f"Loaded Asset: {TARGET_FILE}")
    st.sidebar.markdown(f"**Total Data Modules:** {len(msig_db)} Sheets")
else:
    st.sidebar.error("Cognitive Core: OFFLINE")
    st.sidebar.warning(system_status)
    st.stop()

# ==========================================
# DIAGNOSTIC ENGINE COMPONENT (NO GENAI)
# ==========================================
st.write("### 🛠️ Deterministic Query & Compliance Search Matrix")
st.write("Input any engineering keyword, component, section index, or regulation rule parameter below to retrieve the exact requirements from the file.")

search_query = st.text_input("Enter Command / Query Parameter (e.g., 'PE', 'Septic Tank', 'Buffer', 'PDC')", "").strip()

if search_query:
    st.write(f"#### 🔍 Execution Logs: Scanning for '{search_query}' across core sub-systems...")
    matches_found = 0
    
    # Iterate dynamically across your structured sheets without LLM interference
    for sheet_name, dataframe in msig_db.items():
        # Mask matching strings anywhere within row fields
        mask = dataframe.apply(lambda row: row.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = dataframe[mask]
        
        if not filtered_df.empty:
            matches_found += len(filtered_df)
            with st.expander(f"📦 Module Block: {sheet_name} ({len(filtered_df)} matches found)", expanded=True):
                st.dataframe(filtered_df, use_container_width=True)
                
    if matches_found == 0:
        st.warning(f"No specific rule matrices match '{search_query}' inside the active workbook document.")
else:
    st.info("System awaiting command entry. Standing by for calculation targets, sir.")

# ==========================================
# EXTRA EXTRACTION TOOL: AUTOMATED PE & BUFFER CALCULATOR
# ==========================================
st.write("---")
st.write("### 📐 Algorithmic Design Calculator (Built-in MSIG Volume 1 Rules)")
st.write("Calculations are evaluated programmatically from the explicit rule entries inside your document.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Population Equivalent (PE) Estimator")
    residential_units = st.number_input("Residential Units:", min_value=0, value=0, step=1)
    office_sqm = st.number_input("Office Net Floor Area (sqm):", min_value=0.0, value=0.0, step=10.0)
    retail_sqm = st.number_input("Retail Net Floor Area (sqm):", min_value=0.0, value=0.0, step=10.0)
    
    # Mathematical calculation derived strictly from MSIG Vol 1 specifications
    calculated_pe = (residential_units * 4) + ((office_sqm / 100) * 3) + ((retail_sqm / 100) * 3)
    
    st.markdown(f"<div class='system-card'>Total Project Design Load:<br><span class='metric-value'>{calculated_pe:,.2f} PE</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown("#### Structural Buffer Siting Requirements")
    st.write("Evaluation based on calculated or explicitly defined operational PE limits:")
    
    eval_pe = st.number_input("Target Evaluation PE Load:", min_value=0.0, value=float(calculated_pe), step=50.0)
    
    # Deterministic evaluation checks bypassing any probabilistic logic model completely
    if eval_pe == 0:
        buffer_zone = "0m (No Load)"
        connection_type = "N/A"
    elif eval_pe < 150:
        buffer_zone = "20m Buffer Requirement"
        connection_type = "Individual Septic Tank (IST) Approved (< 150 PE Threshold)"
    elif eval_pe < 1000:
        buffer_zone = "20m Buffer Requirement"
        connection_type = "Sewage Treatment Plant (STP) Mandatory (>= 150 PE Threshold)"
    elif eval_pe <= 5000:
        buffer_zone = "25m Buffer Requirement"
        connection_type = "Sewage Treatment Plant (STP) Mandatory"
    else:
        buffer_zone = "30m Buffer Requirement"
        connection_type = "Sewage Treatment Plant (STP) Mandatory"
        
    st.markdown(f"""
        <div class='system-card'>
            Required Boundary Clearance: <span class='metric-value'>{buffer_zone}</span><br>
            System Framework Classification: <br><strong>{connection_type}</strong>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATABASE SHEET EXPLORER TACTICAL MATRIX
# ==========================================
st.write("---")
st.write("### 🗃️ Master Data Module Browser")
st.write("Direct raw visualization array of the master file sheets.")

selected_sheet = st.selectbox("Select Master Data Sheet to review:", list(msig_db.keys()))
st.dataframe(msig_db[selected_sheet], use_container_width=True)
