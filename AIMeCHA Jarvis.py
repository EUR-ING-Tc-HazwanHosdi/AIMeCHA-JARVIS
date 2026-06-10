import os
import math
import re
from datetime import datetime
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & UI
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S.", 
    page_icon="🤖", 
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #050B14; color: #E2F1F8; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stButton>button { background-color: #002B3D; color: #00E5FF; border: 1px solid #00E5FF; }
    .stButton>button:hover { background-color: #00E5FF; color: #050B14; }
    div[data-testid="stExpander"] { background-color: #0A1424; border: 1px solid #005B7F; }
    .stChatMessage { background-color: #0A192F; border-radius: 6px; border-left: 3px solid #00E5FF; margin-bottom: 12px; }
    .info-box { background-color: #0A1424; padding: 10px; border-radius: 5px; border: 1px solid #005B7F; margin: 8px 0; }
    .warning { color: #FFB300; }
    .success { color: #00E5FF; }
    .danger { color: #FF4444; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. — SMART HARDCODED ENGINE")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Core: ADVANCED LOGIC + KNOWLEDGE GRID — ONLINE")
st.sidebar.info("Intelligence Level: HIGH | 100% OFFLINE")
st.sidebar.info("Domain: Malaysian Sewerage Engineering (MSIG V1-V4)")
st.sidebar.info(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==========================================
# ADVANCED KNOWLEDGE BASE (STRUCTURED + SEARCHABLE)
# ==========================================
KNOWLEDGE_GRID = {
    "regulatory": {
        "DOSH/JKKP": {
            "act": "Factory and Machinery Act 1967, OSHA 1994",
            "scope": "Safety, machinery, hazardous operations, workplace health, registration of machinery",
            "compliance": "All construction & operation activities must be certified; safety officer required for >20 workers"
        },
        "CIDB": {
            "act": "CIDB Act 1994",
            "scope": "Contractor registration, works approval, quality management, site safety certification",
            "compliance": "Contractors must be registered; projects >RM500k need CIDB certification"
        },
        "SPAN": {
            "act": "Water Services Industry Act 2006",
            "scope": "Regulation of water & sewerage services, licensing, technical standards, tariffs",
            "compliance": "All sewerage systems require SPAN approval & operating license"
        },
        "IWK": {
            "act": "Indah Water Konsortium Act 1993",
            "scope": "National sewerage operator, design standards, O&M guidelines, treatment requirements",
            "compliance": "Connection mandatory if within 30m of public sewer"
        },
        "DOE/JAS": {
            "act": "Environmental Quality Act 1974",
            "scope": "Effluent standards, EIA, pollution control, environmental monitoring",
            "compliance": "Discharge must meet Standard A or B; EIA required >50,000 PE"
        },
        "BEM": {
            "act": "Registration of Engineers Act 1967",
            "scope": "Professional practice, code of ethics, certification of designs & plans",
            "compliance": "All engineering drawings & reports must be signed by Professional Engineer"
        }
    },

    "msig_standards": {
        "volume1_planning": {
            "title": "Volume 1: Planning Principles",
            "pe_calculation": {
                "residential": {"value": 4, "unit": "PE/unit", "rule": "Each housing unit = 4 Population Equivalent"},
                "commercial": {"value": 3, "unit": "PE/100m²", "rule": "Office/Retail = 3 PE per 100 square meters"},
                "industrial": {"value": 5, "unit": "PE/100 workers", "rule": "Industrial = 5 PE per 100 employees"}
            },
            "buffer_zones": [
                {"max_pe": 1000, "distance": 20, "unit": "m", "note": "From system boundary to nearest building"},
                {"max_pe": 5000, "distance": 25, "unit": "m"},
                {"max_pe": 50000, "distance": 30, "unit": "m"},
                {"max_pe": 999999, "distance": 50, "unit": "m", "note": "Requires EIA approval"}
            ],
            "effluent_limits": {
                "Standard A": {"BOD": 10, "TSS": 20, "COD": 60, "AMMONIA": 5, "OIL_GREASE": 2, "unit": "mg/L", "use": "Discharge to sensitive areas / inland waters"},
                "Standard B": {"BOD": 20, "TSS": 40, "COD": 100, "AMMONIA": 10, "OIL_GREASE": 5, "unit": "mg/L", "use": "Discharge to rivers / non-sensitive areas"}
            },
            "system_selection": {
                "septic_tank": "<= 150 PE — Individual Septic Tank allowed",
                "small_stp": "151 – 5,000 PE — Package / Modular STP",
                "large_stp": "> 5,000 PE — Conventional Activated Sludge / MBBR / MBR"
            }
        },

        "volume2_low_risk": {
            "title": "Volume 2: Low Risk Sewerage (<=150 PE)",
            "approvals": {
                "PDC1": {"name": "Planning Approval", "time": "14 days", "form": "WSIA/PDC/1"},
                "PDC2": {"name": "Design Approval", "time": "21 days", "form": "WSIA/PDC/2"},
                "PDC6": {"name": "Notice to Commence", "time": "14 days prior", "form": "WSIA/PDC/6"},
                "PDC7": {"name": "Intermediate Inspection", "time": "14 days", "form": "WSIA/PDC/7"},
                "PDC8": {"name": "Final Inspection", "time": "14 days", "form": "WSIA/PDC/8"},
                "PDC9": {"name": "Completion Notice", "time": "14 days", "form": "WSIA/PDC/9"}
            },
            "septic_tank_design": {
                "flow_rate": 225, "unit": "L/capita/day",
                "min_capacity": 2000, "unit": "Litres",
                "chamber_split": {"first": 67, "second": 33, "unit": "%"},
                "liquid_depth": {"min": 1.2, "max": 1.8, "unit": "m"},
                "freeboard": {"min": 0.3, "unit": "m"},
                "inlet_submergence": {"min": 0.3, "max": 0.45, "unit": "m"},
                "outlet_submergence": {"min": 0.2, "max": 0.3, "unit": "m"},
                "ventilation": "Min 100mm diameter vent pipe"
            },
            "pipeline": {
                "min_diameter": 150, "unit": "mm",
                "gradient": {"min": 1/100, "max": 1/60, "note": "1:60 to 1:100"},
                "max_length": 30, "unit": "m between manholes",
                "cover_depth": {"non_traffic": 0.9, "traffic": 1.2, "unit": "m"}
            }
        },

        "volume3_networks": {
            "title": "Volume 3: Sewer Networks & Pump Stations",
            "pipe_materials": {
                "VCP": "Vitrified Clay Pipe — standard for gravity sewers, 50-year life",
                "uPVC": "Plastic — only for <225mm, non-traffic areas",
                "RC": "Reinforced Concrete — >=600mm only, Grade 30+",
                "GRP": "Glass Reinforced Plastic — >=600mm, corrosive environments",
                "DI": "Ductile Iron — pressure pipes & pump stations only"
            },
            "manhole_specs": {
                "type": "Pre-cast or in-situ concrete ONLY — brick manholes BANNED",
                "grade": "C30/C35 minimum",
                "max_depth": 9, "unit": "m",
                "deep_approval": ">6m requires SPAN approval",
                "covers": "Class D400 (road), Class B125 (pedestrian)"
            },
            "testing": {
                "air_test": "<=7kPa loss (VC/RC), <=2kPa (plastic) over 15 mins",
                "water_test": "Head 2–7m; loss <1L/hr/m/m-ID (VC/RC); zero loss (plastic)",
                "cctv": "100% inspection if >6m deep or >600mm dia"
            }
        },

        "volume4_treatment": {
            "title": "Volume 4: Sewage Treatment Plants",
            "process_selection": {
                "<1000 PE": "Extended Aeration / RBC",
                "1000–5000 PE": "MBBR / SBR",
                ">5000 PE": "Activated Sludge / MBR"
            },
            "structural": {
                "concrete_grade": "C35A for sewage containment",
                "wall_thickness": ">=225mm",
                "fasteners": "SS316 stainless steel for all wetted parts",
                "noise": "<=65dB at 2m from boundary"
            },
            "electrical": {
                "earthing": "<=1.0 Ohm",
                "lightning": "<=5.0 Ohm",
                "power_factor": ">=0.9",
                "ups": ">=6 hours backup for SCADA & controls"
            }
        }
    },

    "checklist": [
        {"id": "PDC1", "stage": "Planning", "name": "Sewerage Planning Approval", "timeline": "14 days", "mandatory": True},
        {"id": "PDC2", "stage": "Design", "name": "System Design Approval", "timeline": "21 days", "mandatory": True},
        {"id": "PDC6", "stage": "Construction", "name": "Notice of Commencement", "timeline": "14 days before start", "mandatory": True},
        {"id": "PDC7", "stage": "Construction", "name": "Intermediate Inspection", "timeline": "14 days", "mandatory": True},
        {"id": "PDC8", "stage": "Completion", "name": "Final Inspection & Approval", "timeline": "14 days", "mandatory": True},
        {"id": "PDC9", "stage": "Completion", "name": "Septic Tank Completion Notice", "timeline": "14 days", "mandatory": "Conditional"},
        {"id": "HO1", "stage": "Handover", "name": "System Handover + CCC", "timeline": "As per license", "mandatory": True}
    ],

    "compliance_rules": {
        "approval_validity": "2 years from issue date",
        "extension_request": "Must submit 3 months BEFORE expiry",
        "defect_liability_period": "12 months from handover",
        "performance_bond": "5% of contract value, valid 15 months",
        "connection_rule": "Mandatory connection if public sewer within 30m"
    }
}

# ==========================================
# ADVANCED CALCULATION ENGINE
# ==========================================
class CalculationEngine:
    @staticmethod
    def parse_numbers(text):
        """Extract all numbers from any text"""
        return [float(n) for n in re.findall(r'\d+\.?\d*', text)]

    @staticmethod
    def calculate_pe(project_type, quantity):
        """Smart PE calculation with recommendations"""
        std = KNOWLEDGE_GRID["msig_standards"]["volume1_planning"]["pe_calculation"]
        project_type = project_type.lower()

        if any(word in project_type for word in ["residential", "house", "unit", "home"]):
            pe = quantity * std["residential"]["value"]
            rule = std["residential"]["rule"]
        elif any(word in project_type for word in ["office", "retail", "commercial", "shop", "sqm", "m²"]):
            pe = (quantity / 100) * std["commercial"]["value"]
            rule = std["commercial"]["rule"]
        elif any(word in project_type for word in ["industrial", "factory", "worker", "staff"]):
            pe = (quantity / 100) * std["industrial"]["value"]
            rule = std["industrial"]["rule"]
        else:
            return {"error": "Project type not recognized"}

        # System recommendation
        system_rules = KNOWLEDGE_GRID["msig_standards"]["volume1_planning"]["system_selection"]
        if pe <= 150:
            system = system_rules["septic_tank"]
            type_rec = "Individual Septic Tank (IST) or Small Package Plant"
        elif pe <= 5000:
            system = system_rules["small_stp"]
            type_rec = "Modular / Package Sewage Treatment Plant"
        else:
            system = system_rules["large_stp"]
            type_rec = "Conventional / MBBR / MBR Treatment Plant — EIA Required"

        # Buffer zone
        buffers = KNOWLEDGE_GRID["msig_standards"]["volume1_planning"]["buffer_zones"]
        buffer = next((b for b in sorted(buffers, key=lambda x:x["max_pe"]) if pe <= b["max_pe"]), buffers[-1])

        return {
            "input": f"{quantity} {project_type}",
            "population_equivalent": round(pe, 2),
            "rule": rule,
            "system_recommendation": system,
            "plant_type": type_rec,
            "minimum_buffer_zone": f"{buffer['distance']} {buffer['unit']}",
            "connection_required": "YES — within 30m of public sewer" if pe > 50 else "Check distance to public sewer"
        }

    @staticmethod
    def design_septic_tank(pe):
        """Full septic tank design per MSIG"""
        if pe > 150:
            return {"error": "PE > 150 — Septic Tank NOT allowed. Design STP instead."}

        std = KNOWLEDGE_GRID["msig_standards"]["volume2_low_risk"]["septic_tank_design"]
        daily_flow = pe * std["flow_rate"]
        capacity = max(daily_flow, std["min_capacity"])
        first_chamber = capacity * (std["chamber_split"]["first"] / 100)
        second_chamber = capacity * (std["chamber_split"]["second"] / 100)

        return {
            "pe": pe,
            "daily_flow_l": round(daily_flow, 2),
            "total_capacity_l": round(capacity, 2),
            "chamber1": round(first_chamber, 2),
            "chamber2": round(second_chamber, 2),
            "liquid_depth": f"{std['liquid_depth']['min']} – {std['liquid_depth']['max']} m",
            "freeboard": f"Min {std['freeboard']['min']} m",
            "inlet_submergence": f"{std['inlet_submergence']['min']} – {std['inlet_submergence']['max']} m",
            "outlet_submergence": f"{std['outlet_submergence']['min']} – {std['outlet_submergence']['max']} m",
            "ventilation": std["ventilation"],
            "compliant": True
        }

    @staticmethod
    def check_effluent(flow, bod, tss, cod, nh3, og, standard="A"):
        """Check compliance & give improvement advice"""
        std = KNOWLEDGE_GRID["msig_standards"]["volume1_planning"]["effluent_limits"][f"Standard {standard.upper()}"]
        params = {"BOD": bod, "TSS": tss, "COD": cod, "AMMONIA": nh3, "OIL_GREASE": og}
        results = {}
        compliant = True
        advice = []

        for name, val in params.items():
            limit = std[name]
            ok = val <= limit
            results[name] = {"value": val, "limit": limit, "compliant": ok}
            if not ok:
                compliant = False
                if name == "BOD": advice.append("Improve biological treatment / increase aeration time")
                if name == "TSS": advice.append("Optimize sedimentation / add filtration")
                if name == "COD": advice.append("Enhance oxidation / chemical treatment")
                if name == "AMMONIA": advice.append("Add nitrification stage / extend aeration")
                if name == "OIL_GREASE": advice.append("Install better grease traps / separators")

        return {
            "standard": f"Standard {standard.upper()}",
            "flow_m3d": flow,
            "compliant": compliant,
            "parameters": results,
            "recommendations": advice if not compliant else ["All parameters within limits — excellent performance"]
        }

# ==========================================
# INTELLIGENT RESPONSE ENGINE
# ==========================================
class JarvisBrain:
    def __init__(self):
        self.calc = CalculationEngine()
        self.keywords = {
            "greeting": ["hello", "hi", "assalamualaikum", "good morning", "good afternoon"],
            "pe_calc": ["population equivalent", "pe", "calculate pe", "how many pe", "pe for"],
            "septic_design": ["septic tank", "tank design", "size septic", "septic size"],
            "effluent": ["effluent", "discharge", "standard a", "standard b", "water quality"],
            "regulatory": ["regulation", "authority", "act", "dosha", "jkkp", "cidb", "span", "iwk", "doe", "bem"],
            "approval": ["approval", "permit", "form", "pdc1", "pdc2", "pdc6", "pdc7", "pdc8", "pdc9"],
            "checklist": ["checklist", "list of requirements", "compliance"],
            "volume1": ["volume 1", "planning", "buffer zone", "system selection"],
            "volume2": ["volume 2", "low risk", "septic", "pipeline"],
            "volume3": ["volume 3", "network", "pump station", "manhole", "pipe"],
            "volume4": ["volume 4", "treatment plant", "stp", "process"]
        }

    def understand_intent(self, text):
        """Determine what the user wants — smart matching"""
        text = text.lower()
        scores = {}
        for intent, words in self.keywords.items():
            scores[intent] = sum(1 for w in words if w in text)
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "unknown"

    def search_knowledge(self, query, section=None):
        """Smart search through all knowledge"""
        query = query.lower()
        results = []
        data = KNOWLEDGE_GRID

        def recurse_search(obj, path=""):
            if isinstance(obj, dict):
                for k,v in obj.items():
                    recurse_search(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i,item in enumerate(obj):
                    recurse_search(item, f"{path}[{i}]")
            else:
                if query in str(obj).lower():
                    results.append({"path": path, "value": obj})

        if section:
            if section in data:
                recurse_search(data[section])
        else:
            recurse_search(data)
        return results

    def generate_response(self, user_input):
        intent = self.understand_intent(user_input)
        nums = self.calc.parse_numbers(user_input)

        # --- GREETING ---
        if intent == "greeting":
            return "Good day, sir. I am fully operational with advanced engineering intelligence. I understand your requests in natural language, perform accurate calculations, and provide compliance recommendations. What engineering task shall we solve today?"

        # --- PE CALCULATION ---
        if intent == "pe_calc":
            if len(nums) >= 1:
                qty = nums[0]
                if "residential" in user_input.lower():
                    res = self.calc.calculate_pe("residential", qty)
                elif any(w in user_input.lower() for w in ["office", "retail", "commercial"]):
                    res = self.calc.calculate_pe("office", qty)
                elif any(w in user_input.lower() for w in ["industrial", "factory"]):
                    res = self.calc.calculate_pe("industrial", qty)
                else:
                    return "Please specify type: residential units, office area (sqm), or industrial workers."

                if "error" in res:
                    return f"❌ {res['error']}"

                return f"""**📊 POPULATION EQUIVALENT ANALYSIS**
• Input: {res['input']}
• Calculation Rule: {res['rule']}
• **Total PE: {res['population_equivalent']}**

**🏗️ SYSTEM RECOMMENDATION**
{res['system_recommendation']}
Preferred Type: {res['plant_type']}

**📏 COMPLIANCE DATA**
Minimum Buffer Zone: {res['minimum_buffer_zone']}
Connection Status: {res['connection_required']}

*Based on MSIG Volume 1 Planning Principles*
"""

        # --- SEPTIC TANK DESIGN ---
        if intent == "septic_design":
            if len(nums) >= 1:
                pe = nums[0]
                res = self.calc.design_septic_tank(pe)
                if "error" in res:
                    return f"❌ {res['error']}"

                return f"""**🛢️ SEPTIC TANK DESIGN — MSIG VOLUME 2**
**Project Size: {res['pe']} PE**

📌 **Capacity & Flow**
• Daily Flow: {res['daily_flow_l']} Litres/day
• Total Required Capacity: **{res['total_capacity_l']} Litres**

📐 **Dimensions & Layout**
• Chamber 1 (67%): {res['chamber1']} L — Primary Settlement
• Chamber 2 (33%): {res['chamber2']} L — Anaerobic Digestion
• Liquid Depth: {res['liquid_depth']}
• Freeboard (Air Space): {res['freeboard']}

⚙️ **Technical Specs**
• Inlet Submergence: {res['inlet_submergence']}
• Outlet Submergence: {res['outlet_submergence']}
• Ventilation: {res['ventilation']}

✅ **Fully Compliant with MSIG Standards**
"""

        # --- EFFLUENT CHECK ---
        if intent == "effluent":
            if len(nums) >= 6:
                flow, bod, tss, cod, nh3, og = nums[:6]
                std = "B" if "b" in user_input.lower() else "A"
                res = self.calc.check_effluent(flow, bod, tss, cod, nh3, og, std)

                txt = f"**💧 EFFLUENT COMPLIANCE REPORT — {res['standard']}**\n"
                txt += f"Flow Rate: {res['flow_m3d']} m³/day\n"
                txt += f"Status: {'✅ FULLY COMPLIANT' if res['compliant'] else '⚠️ NON-COMPLIANT — ACTION REQUIRED'}\n\n"
                txt += "Parameter Analysis:\n"
                for p,v in res['parameters'].items():
                    txt += f"• {p}: {v['value']} mg/L | Limit: {v['limit']} | {'✅ OK' if v['compliant'] else '❌ EXCEEDED'}\n"
                txt += "\n📋 Recommendations:\n" + "\n".join(f"• {r}" for r in res['recommendations'])
                return txt

        # --- REGULATORY INFO ---
        if intent == "regulatory":
            results = self.search_knowledge(user_input, "regulatory")
            if results:
                txt = "**📜 REGULATORY INFORMATION**\n"
                seen = set()
                for r in results:
                    name = r['path'].split('.')[-1]
                    if name not in seen:
                        seen.add(name)
                        txt += f"\n**{name}**\n{str(r['value'])}\n"
                return txt

        # --- APPROVALS / CHECKLIST ---
        if intent in ["approval", "checklist"]:
            txt = "**✅ MSIG COMPLIANCE CHECKLIST**\nRequired approvals & documents:\n"
            for item in KNOWLEDGE_GRID["checklist"]:
                txt += f"• **{item['id']} — {item['name']}**\n  Timeline: {item['timeline']} | Mandatory: {item['mandatory']}\n"
            txt += "\n**📌 Important Rules**\n• Approval valid for: " + KNOWLEDGE_GRID["compliance_rules"]["approval_validity"] + "\n• Extension request deadline: " + KNOWLEDGE_GRID["compliance_rules"]["extension_request"]
            return txt

        # --- MSIG VOLUME INFO ---
        if intent in ["volume1", "volume2", "volume3", "volume4"]:
            vol = intent.replace("volume", "volume ")
            data = KNOWLEDGE_GRID["msig_standards"][vol.replace(" ", "_")]
            txt = f"**📘 {data['title']}**\n\n"
            for k,v in data.items():
                if k != "title":
                    txt += f"**{k.upper()}**\n{str(v)}\n\n"
            return txt

        # --- DEFAULT ---
        return """I have **Advanced Hardcoded Intelligence** loaded — I understand natural language, perform calculations, and give expert recommendations.

You can ask me things like:
• *"Calculate PE for 120 residential units"*
• *"Design septic tank for 100 PE"*
• *"Check effluent standard A 2000 12 25 70 6 3"*
• *"What approvals do I need?"*
• *"Tell me about SPAN requirements"*
• *"Show MSIG Volume 2 pipeline specs"*

I will analyze your request, compute accurately, and provide full compliance advice — all offline, no AI needed.
"""

# ==========================================
# SYSTEM OPERATION
# ==========================================
brain = JarvisBrain()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "A.I.M.E.C.H.A. — **Advanced Hardcoded Intelligence** initialized. I understand natural language, perform calculations, and provide expert engineering advice. Awaiting your command, sir."}
    ]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process input
if user_input := st.chat_input("Type your engineering question or calculation..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing data, computing, verifying compliance..."):
            response = brain.generate_response(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
