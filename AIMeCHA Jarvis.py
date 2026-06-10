import os
import math
from datetime import datetime
import streamlit as st

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
    .info-box { background-color: #0A1424; padding: 10px; border-radius: 5px; border: 1px solid #005B7F; margin: 8px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. AI Engine")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Core: HARDCODED INTELLIGENCE - ONLINE")
st.sidebar.info("Grounding: Malaysia Federal Regulatory Dataset V2026")
st.sidebar.info("Updated: MSIG Checklist + Full Calculation Engine")
st.sidebar.info(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==========================================
# HARDCODED KNOWLEDGE BASE - FULL DATASET
# ==========================================
HARDCODED_KNOWLEDGE = {
    "regulatory_bodies": {
        "DOSH/JKKP": "Factory and Machinery Act 1967, OSHA 1994 — covers safety, machinery, hazardous operations, workplace health.",
        "CIDB": "Construction Industry Board guidelines — works registration, contractor grading, site safety, quality standards.",
        "MIDA": "Malaysian Investment Development Authority — project incentives, compliance, industrial licensing.",
        "DOE/JAS": "Environmental Quality Act 1974 — EIA, effluent standards, air emissions, waste management.",
        "Suruhanjaya Tenaga": "Energy Commission — electrical safety, grid connection, wiring codes, renewable energy rules.",
        "BEM": "Board of Engineers Malaysia — professional practice, code of ethics, accreditation, project certification.",
        "SPAN": "Water Services Commission — sewerage & water industry standards, licensing, compliance monitoring.",
        "IWK": "Indah Water Konsortium — national sewerage operator, design guidelines, operation & maintenance standards."
    },

    "msig_volume1": {
        "title": "Volume 1: Planning Principles",
        "population_equivalent": {
            "residential": 4,  # PE per unit
            "office_retail": 3  # PE per 100 sqm
        },
        "buffer_zones": {
            "<1000 PE": 20,   # meters
            "1000-5000 PE": 25,
            "5000-50000 PE": 30
        },
        "effluent_standards": {
            "Standard A": {
                "BOD": 10, "TSS": 20, "COD": 60, "AMN": 5, "O&G": 2, "unit": "mg/L"
            },
            "Standard B": {
                "BOD": 20, "TSS": 40, "COD": 100, "AMN": 10, "O&G": 5, "unit": "mg/L"
            }
        },
        "wlcc": {
            "period": 50, "discount_rate": 4, "growth_rate": 3
        },
        "connection_rules": {
            "mandatory_connection_distance": 30,  # meters
            "ist_max_pe": 150,
            "stp_min_pe": 150
        },
        "ghg_footprint": {
            "Class 1": 13, "Class 2": 8, "Class 3": 6, "Class 4": 4,
            "electricity_factor": 0.78  # kg CO2e/kWh
        }
    },

    "msig_volume2": {
        "title": "Volume 2: Low Risk Sewerage (<=150 PE)",
        "forms_timeline": {
            "PDC 1": "Planning Approval — 14 calendar days",
            "PDC 2": "Design & Structural Review — 21 calendar days",
            "PDC 6": "Notice of Work Commencement — submit minimum 14 days before start",
            "PDC 7": "Intermediate Inspection — 14 calendar days",
            "PDC 8": "Final Inspection / Operating Clearance — 14 calendar days",
            "PDC 9": "Septic Tank Completion Notice — 14 calendar days"
        },
        "pipeline": {
            "min_diameter": 150,  # mm
            "gradient_min": 1/100,
            "gradient_max": 1/60,
            "max_manhole_spacing": 30,  # m
            "depth_cover_non_traffic": 0.9,  # m
            "depth_cover_traffic": 1.2     # m
        },
        "septic_tank": {
            "flow_allocation": 225,  # L/capita/day
            "min_capacity": 2000,    # Litres
            "chamber_split_first": 0.67,
            "chamber_split_second": 0.33,
            "liquid_depth_min": 1.2,
            "liquid_depth_max": 1.8,
            "freeboard_min": 0.3,    # m
            "inlet_submergence_min": 0.3,
            "inlet_submergence_max": 0.45,
            "outlet_submergence_min": 0.2,
            "outlet_submergence_max": 0.3
        },
        "soil_absorption": {
            "percolation_min": 1,   # mins/inch
            "percolation_max": 60,
            "max_trench_length": 30, # m
            "water_table_separation": 1.2, # m
            "gradient_min": 1/400,
            "gradient_max": 1/200
        }
    },

    "msig_volume3": {
        "title": "Volume 3: Sewer Networks & Pump Stations",
        "pipe_specs": {
            "design_life": 50, # years
            "fasteners": "SS304",
            "vcp_public_min": 225, # mm
            "vcp_service_min": 150,
            "rc_grp_min": 600, # mm
            "manhole_type": "Pre-cast or in-situ Grade C30/C35 only — brick banned"
        },
        "backdrop": {
            "drop_upto225": 0.9, # m
            "drop_over225": 1.0, # m
            "max_depth": 9, # m
            "approval_depth": 6 # m — above this needs SPAN approval
        },
        "testing": {
            "air_test_vc_rc": 7, # kPa
            "air_test_plastic": 2, # kPa
            "water_test_head_min": 2, # m
            "water_test_head_max": 7, # m
            "water_loss_vc_rc": 1, # L/hr/m/m-ID
            "water_loss_plastic": 0
        },
        "pump_station": {
            "buffer": 20, # m
            "piping": "Ductile Iron (DI)",
            "hopper_slope": 1.5/1.0, # V:H
            "flushing_pe": 2000, # auto flush above this PE
            "retention_time_max": 0.5 # hours
        }
    },

    "msig_volume4": {
        "title": "Volume 4: Sewage Treatment Plants",
        "structure": {
            "concrete_grade": "C35A",
            "thickness_min": 225, # mm
            "fasteners": "SS316",
            "noise_limit": 65 # dB at 2m
        },
        "process": {
            "screen_spacing_max": 25, # mm
            "pump_redundancy": {
                "<=5000": "1 duty + 1 standby",
                "5000-20000": "2 duty + 2 standby",
                ">20000": "4 duty + 2 standby"
            },
            "clarifier_depth_min": 3.0, # m
            "hrt_min": 2, # hours
            "solids_loading_max": 150, # kg/d/m²
            "uv_dose_min": 30, # mJ/cm²
            "uv_tss_limit": 10 # mg/L before UV
        },
        "electrical": {
            "power_factor_min": 0.9,
            "earthing_max": 1.0, # Ohm
            "lightning_max": 5.0, # Ohm
            "panel_clearance_min": 900, # mm
            "ups_duration_min": 6 # hours
        }
    },

    "msig_checklist": [
        {
            "procedure": "2.1 Perancangan Pembetungan",
            "form": "WSIA/PDC/1",
            "timeline": "14 Hari Kalendar",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.2 Reka Bentuk Sistem / Tangki Septik",
            "form": "WSIA/PDC/2",
            "timeline": "21 Hari Kalendar",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.3 Notis Mula Kerja",
            "form": "WSIA/PDC/6 (3,4,5,6-1)",
            "timeline": "Hantar Min 14 Hari Sebelum",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.4 Pemeriksaan Pertengahan",
            "form": "WSIA/PDC/7",
            "timeline": "14 Hari Kalendar",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.5 Pemeriksaan Akhir",
            "form": "WSIA/PDC/8",
            "timeline": "14 Hari Kalendar",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.6 Notis Penyiapan Tangki Septik",
            "form": "WSIA/PDC/9",
            "timeline": "14 Hari Kalendar",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        },
        {
            "procedure": "2.7 Penyerahan Sistem Pembetungan Awam",
            "form": "Handover Form + CCC",
            "timeline": "Tertakluk kepada pemegang lesen",
            "status": ["Belum Mula", "Dalam Proses", "Selesai"]
        }
    ],

    "compliance_notes": [
        "Kelulusan Perancangan & Reka Bentuk sah selama DUA (2) TAHUN dari tarikh dikeluarkan.",
        "Permohonan lanjutan mesti dikemukakan TIGA (3) BULAN sebelum tamat tempoh.",
        "Tempoh Tanggungan Kecacatan (DLP) = DUA BELAS (12) BULAN dari tarikh penyerahan rasmi.",
        "Jaminan Bank (BG) = LIMA PERATUS (5%) kos projek; sah LIMA BELAS (15) BULAN."
    ]
}

# ==========================================
# HARDCODED CALCULATION ENGINE
# ==========================================
class JarvisCalculator:
    @staticmethod
    def calculate_pe(project_type: str, quantity: float) -> dict:
        """Calculate Population Equivalent"""
        if project_type.lower() in ["residential", "house", "unit"]:
            pe = quantity * HARDCODED_KNOWLEDGE["msig_volume1"]["population_equivalent"]["residential"]
            rule = "Residential: 4 PE per unit"
        elif project_type.lower() in ["office", "retail", "commercial", "sqm", "m2"]:
            pe = (quantity / 100) * HARDCODED_KNOWLEDGE["msig_volume1"]["population_equivalent"]["office_retail"]
            rule = "Office/Retail: 3 PE per 100 m²"
        else:
            return {"error": "Invalid type. Use: residential / office / retail"}
        
        # Determine system type
        rules = HARDCODED_KNOWLEDGE["msig_volume1"]["connection_rules"]
        if pe <= rules["ist_max_pe"]:
            system_type = "Individual Septic Tank (IST) allowed"
        else:
            system_type = "Sewage Treatment Plant (STP) REQUIRED"

        # Buffer zone
        if pe < 1000:
            buffer = HARDCODED_KNOWLEDGE["msig_volume1"]["buffer_zones"]["<1000 PE"]
        elif pe <= 5000:
            buffer = HARDCODED_KNOWLEDGE["msig_volume1"]["buffer_zones"]["1000-5000 PE"]
        else:
            buffer = HARDCODED_KNOWLEDGE["msig_volume1"]["buffer_zones"]["5000-50000 PE"]

        return {
            "project_type": project_type,
            "quantity": quantity,
            "population_equivalent": round(pe, 2),
            "rule": rule,
            "system_recommendation": system_type,
            "minimum_buffer_zone_m": buffer
        }

    @staticmethod
    def calculate_septic_tank(pe: float) -> dict:
        """Calculate Septic Tank Design Parameters (MSIG Vol 2)"""
        if pe > 150:
            return {"error": "PE exceeds 150 — STP required, not septic tank"}
        
        flow = pe * HARDCODED_KNOWLEDGE["msig_volume2"]["septic_tank"]["flow_allocation"]
        capacity = max(flow, HARDCODED_KNOWLEDGE["msig_volume2"]["septic_tank"]["min_capacity"])
        first_chamber = capacity * HARDCODED_KNOWLEDGE["msig_volume2"]["septic_tank"]["chamber_split_first"]
        second_chamber = capacity * HARDCODED_KNOWLEDGE["msig_volume2"]["septic_tank"]["chamber_split_second"]
        
        return {
            "population_equivalent": pe,
            "daily_flow_L": round(flow, 2),
            "required_capacity_L": round(capacity, 2),
            "first_chamber_L": round(first_chamber, 2),
            "second_chamber_L": round(second_chamber, 2),
            "liquid_depth_range_m": f"{HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['liquid_depth_min']} - {HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['liquid_depth_max']}",
            "freeboard_min_m": HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['freeboard_min'],
            "inlet_submergence_m": f"{HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['inlet_submergence_min']} - {HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['inlet_submergence_max']}",
            "outlet_submergence_m": f"{HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['outlet_submergence_min']} - {HARDCODED_KNOWLEDGE['msig_volume2']['septic_tank']['outlet_submergence_max']}"
        }

    @staticmethod
    def calculate_pipe_gradient(diameter_mm: int, length_m: float, drop_m: float = None) -> dict:
        """Check or calculate sewer pipe gradient per MSIG"""
        std = HARDCODED_KNOWLEDGE["msig_volume2"]["pipeline"]
        if drop_m is not None:
            gradient = drop_m / length_m
            ratio = f"1:{round(1/gradient, 0)}"
        else:
            gradient = (std["gradient_min"] + std["gradient_max"]) / 2
            ratio = f"1:{round(1/gradient, 0)} (standard mid-range)"

        compliant = std["gradient_min"] <= gradient <= std["gradient_max"]
        
        return {
            "diameter_mm": diameter_mm,
            "length_m": length_m,
            "gradient_value": round(gradient, 4),
            "gradient_ratio": ratio,
            "compliant": compliant,
            "allowed_range": f"1:{round(1/std['gradient_max'],0)} to 1:{round(1/std['gradient_min'],0)}",
            "min_diameter_rule": "Min 150mm for gravity sewers" if diameter_mm >= 150 else "❌ Below minimum diameter!"
        }

    @staticmethod
    def check_effluent(flow_m3d: float, bod: float, tss: float, cod: float, amn: float, og: float, standard: str = "A") -> dict:
        """Check compliance against Standard A or B"""
        std = HARDCODED_KNOWLEDGE["msig_volume1"]["effluent_standards"][f"Standard {standard.upper()}"]
        results = {}
        compliant = True
        for param, val in {"BOD": bod, "TSS": tss, "COD": cod, "AMN": amn, "O&G": og}.items():
            ok = val <= std[param]
            results[param] = {"measured": val, "limit": std[param], "compliant": ok}
            if not ok:
                compliant = False
        
        return {
            "standard": f"Standard {standard.upper()}",
            "flow_m3d": flow_m3d,
            "compliant_overall": compliant,
            "parameters": results
        }

# ==========================================
# HARDCODED RESPONSE ENGINE
# ==========================================
def get_hardcoded_response(user_input: str) -> str:
    user_input = user_input.lower().strip()
    calc = JarvisCalculator()

    # --- GREETINGS ---
    if any(greet in user_input for greet in ["hello", "hi", "hey", "assalamualaikum", "hai"]):
        return "Right away, sir. Systems are fully optimized and all engineering protocols are loaded — including full calculation engine. How may I assist with your project today?"

    # --- PE CALCULATION ---
    if any(word in user_input for word in ["calculate pe", "population equivalent", "pe for"]):
        try:
            if "residential" in user_input:
                qty = float(''.join(filter(str.isdigit, user_input)))
                res = calc.calculate_pe("residential", qty)
                return f"""**📊 Population Equivalent Calculation**
• Type: Residential
• Quantity: {res['quantity']} units
• Rule: {res['rule']}
• Total PE: **{res['population_equivalent']}**
• Recommendation: {res['system_recommendation']}
• Minimum Buffer Zone: {res['minimum_buffer_zone_m']} m
"""
            elif any(term in user_input for term in ["office", "retail", "commercial", "m²", "sqm"]):
                qty = float(''.join(filter(str.isdigit, user_input)))
                res = calc.calculate_pe("office", qty)
                return f"""**📊 Population Equivalent Calculation**
• Type: Office/Retail
• Area: {res['quantity']} m²
• Rule: {res['rule']}
• Total PE: **{res['population_equivalent']}**
• Recommendation: {res['system_recommendation']}
• Minimum Buffer Zone: {res['minimum_buffer_zone_m']} m
"""
            else:
                return "Please specify type and number. Example: 'Calculate PE for 50 residential units' or 'Calculate PE for 800 sqm office'"
        except:
            return "⚠️ Please enter a valid number. Example: 'Calculate PE for 50 residential units'"

    # --- SEPTIC TANK DESIGN ---
    if any(word in user_input for word in ["septic tank", "tank design", "tank size"]):
        try:
            pe = float(''.join(filter(str.isdigit, user_input)))
            res = calc.calculate_septic_tank(pe)
            if "error" in res:
                return f"❌ {res['error']}"
            return f"""**🛢️ Septic Tank Design (MSIG Vol 2)**
• Population Equivalent: {res['population_equivalent']} PE
• Daily Flow: {res['daily_flow_L']} Litres/day
• Required Capacity: **{res['required_capacity_L']} Litres**
• Chamber Split: {res['first_chamber_L']} L (67%) / {res['second_chamber_L']} L (33%)
• Liquid Depth: {res['liquid_depth_range_m']} m
• Minimum Freeboard: {res['freeboard_min_m']} m
• Inlet Submergence: {res['inlet_submergence_m']} m
• Outlet Submergence: {res['outlet_submergence_m']} m
"""
        except:
            return "Please provide PE value. Example: 'Septic tank design for 120 PE'"

    # --- PIPE GRADIENT ---
    if any(word in user_input for word in ["pipe gradient", "sewer gradient", "pipeline slope"]):
        try:
            nums = [float(s) for s in user_input.split() if s.replace('.','',1).isdigit()]
            if len(nums) >= 2:
                dia, length = int(nums[0]), nums[1]
                drop = nums[2] if len(nums)>2 else None
                res = calc.calculate_pipe_gradient(dia, length, drop)
                return f"""**〰️ Sewer Pipe Gradient Check**
• Diameter: {res['diameter_mm']} mm — {res['min_diameter_rule']}
• Length: {res['length_m']} m
• Gradient: {res['gradient_ratio']} ({res['gradient_value']})
• Allowed Range: {res['allowed_range']}
• Compliant: {'✅ YES' if res['compliant'] else '❌ NO — adjust slope'}
"""
            else:
                return "Example: 'Pipe gradient 150mm 50m 0.7m drop'"
        except:
            return "Example: 'Pipe gradient 150mm 50m 0.7m drop'"

    # --- EFFLUENT CHECK ---
    if any(word in user_input for word in ["effluent", "standard a", "standard b", "discharge"]):
        try:
            nums = [float(s) for s in user_input.split() if s.replace('.','',1).isdigit()]
            if len(nums)>=6:
                flow, bod, tss, cod, amn, og = nums[:6]
                std = "B" if "b" in user_input else "A"
                res = calc.check_effluent(flow, bod, tss, cod, amn, og, std)
                txt = f"**💧 Effluent Compliance — {res['standard']}**\n• Flow: {res['flow_m3d']} m³/d\n• Overall: {'✅ COMPLIANT' if res['compliant_overall'] else '❌ NON-COMPLIANT'}\n"
                for p,v in res['parameters'].items():
                    txt += f"• {p}: {v['measured']} mg/L | Limit: {v['limit']} | {'✅' if v['compliant'] else '❌'}\n"
                return txt
            else:
                return "Example: 'Check effluent standard A 1000 8 15 40 3 1'"
        except:
            return "Example: 'Check effluent standard A [flow] [BOD] [TSS] [COD] [AMN] [O&G]'"

    # --- REGULATORY BODIES ---
    if any(word in user_input for word in ["regulatory", "body", "authority", "dosha", "jkkp", "cidb", "mida", "doe", "jas", "tenaga", "bem", "span", "iwk"]):
        resp = "**📋 Malaysian Regulatory Authorities:**\n\n"
        for name, desc in HARDCODED_KNOWLEDGE["regulatory_bodies"].items():
            resp += f"• **{name}**: {desc}\n"
        return resp

    # --- MSIG VOLUME 1 ---
    if any(word in user_input for word in ["volume 1", "planning", "buffer", "effluent", "standard a", "standard b", "wlcc", "connection", "ghg"]):
        v1 = HARDCODED_KNOWLEDGE["msig_volume1"]
        resp = f"**📘 {v1['title']}**\n\n"
        resp += f"**Population Equivalent:**\n• Residential: {v1['population_equivalent']['residential']} PE/unit\n• Office/Retail: {v1['population_equivalent']['office_retail']} PE/100m²\n\n"
        resp += "**Buffer Zones:**\n"
        for k, val in v1["buffer_zones"].items():
            resp += f"• {k}: {val} m\n"
        resp += "\n**Effluent Standards:**\n"
        resp += "• **Standard A:** " + ", ".join([f"{k}: {v}{std['unit']}" for k,v,std in v1["effluent_standards"]["Standard A"].items() if k != 'unit']) + "\n"
        resp += "• **Standard B:** " + ", ".join([f"{k}: {v}{std['unit']}" for k,v,std in v1["effluent_standards"]["Standard B"].items() if k != 'unit']) + "\n"
        resp += f"\n**Connection Rule:** Mandatory if public sewer within {v1['connection_rules']['mandatory_connection_distance']}m\n"
        resp += f"**System Rule:** IST ≤ {v1['connection_rules']['ist_max_pe']} PE | STP > {v1['connection_rules']['stp_min_pe']} PE\n"
        return resp

    # --- MSIG VOLUME 2 ---
    if any(word in user_input for word in ["volume 2", "septic", "low risk", "pdc", "pipeline", "gradient", "soil absorption"]):
        v2 = HARDCODED_KNOWLEDGE["msig_volume2"]
        resp = f"**📘 {v2['title']}**\n\n"
        resp += "**Forms & Timelines:**\n"
        for form, time in v2["forms_timeline"].items():
            resp += f"• **{form}**: {time}\n"
        resp += "\n**Pipeline Specs:**\n"
        resp += f"• Min Dia: {v2['pipeline']['min_diameter']}mm | Gradient: 1:{round(1/v2['pipeline']['gradient_max'],0)}–1:{round(1/v2['pipeline']['gradient_min'],0)}\n"
        resp += f"• Max Manhole Spacing: {v2['pipeline']['max_manhole_spacing']}m | Cover: {v2['pipeline']['depth_cover_non_traffic']}m (non-traffic), {v2['pipeline']['depth_cover_traffic']}m (traffic)\n"
        return resp

    # --- CHECKLIST ---
    if any(word in user_input for word in ["checklist", "senarai semak", "pdc1", "pdc2", "pdc6", "pdc7", "pdc8", "pdc9"]):
        resp = "**✅ MSIG Compliance Checklist (AIMeCHA Engineering Solutions)**\n"
        resp += "Based on Garis Panduan Industri Pembetungan Malaysia (Jilid II) Edisi 2 - Pindaan V1 Julai 2013\n\n"
        for item in HARDCODED_KNOWLEDGE["msig_checklist"]:
            resp += f"• **{item['procedure']}**\n  Form: {item['form']} | Timeline: {item['timeline']}\n"
        resp += "\n**📌 Compliance Notes:**\n"
        for note in HARDCODED_KNOWLEDGE["compliance_notes"]:
            resp += f"• {note}\n"
        return resp

    # --- DEFAULT ---
    return """I have **full hardcoded intelligence + calculation engine** loaded. You can:
• **Calculate PE:** "Calculate PE for 60 residential units" or "Calculate PE for 1200 sqm office"
• **Design Septic Tank:** "Septic tank design for 120 PE"
• **Check Pipe Gradient:** "Pipe gradient 150mm 50m 0.7m drop"
• **Verify Effluent:** "Check effluent standard A 1000 8 15 40 3 1"
• View all MSIG Volumes 1–4, regulations, checklist, or compliance rules.

What do you need computed or reviewed, sir?"""

# ==========================================
# LOCAL FILE GENERATOR
# ==========================================
def create_local_file(file_name: str, content: str) -> str:
    try:
        safe_path = os.path.basename(file_name)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File '{safe_path}' generated successfully."
    except Exception as e:
        return f"ERROR: {str(e)}"

# ==========================================
# MULTI-TURN MEMORY LOGIC
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. framework fully initialized. All engineering rules, regulations, and **calculation functions** are hardcoded. Awaiting your instructions, sir."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# COMMAND INTERCEPT & PROCESSING
# ==========================================
if user_input := st.chat_input("Input mainframe command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing tactical parameters..."):
            # Get hardcoded response
            response_text = get_hardcoded_response(user_input)

            # Generate checklist CSV
            if any(word in user_input for word in ["generate checklist", "export checklist", "download checklist"]):
                csv_content = "Procedure,Form Code,Timeline,Status\n"
                for item in HARDCODED_KNOWLEDGE["msig_checklist"]:
                    csv_content += f"{item['procedure']},{item['form']},{item['timeline']},Pending\n"
                create_local_file("MSIG_Checklist_AIMeCHA.csv", csv_content)
                response_text += "\n\n📁 **MSIG Checklist CSV has been created.**"
                with open("MSIG_Checklist_AIMeCHA.csv", "r", encoding="utf-8") as f:
                    st.download_button(
                        label="📥 Download Checklist CSV",
                        data=f.read(),
                        file_name="MSIG_Checklist_AIMeCHA.csv",
                        mime="text/csv"
                    )

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
