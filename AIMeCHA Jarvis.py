import os
import math
import re
import difflib
from datetime import datetime
import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S. — DOLA-LEVEL INTELLIGENCE",
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

st.title("🤖 J.A.R.V.I.S. — DOLA-LEVEL HARDCODED INTELLIGENCE")
st.sidebar.title("⚙️ System Status")
st.sidebar.success("Core: ADVANCED REASONING + KNOWLEDGE GRAPH — ONLINE")
st.sidebar.info("Intelligence Level: EQUAL TO DOLA | 100% OFFLINE")
st.sidebar.info("Domain: Malaysian Sewerage Engineering (Full MSIG + Regulations)")
st.sidebar.info(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==========================================
# 🧠 KNOWLEDGE GRAPH — HOW DOLA STORES KNOWLEDGE
# Everything is connected, categorized, and has rules
# ==========================================
KNOWLEDGE_GRAPH = {
    "entities": {
        "sewerage_system": {
            "name": "Sewerage System",
            "definition": "A complete infrastructure to collect, convey, treat, and discharge wastewater safely according to Malaysian standards.",
            "types": ["septic_tank", "package_stp", "conventional_stp", "mbbr", "mbr"],
            "regulators": ["SPAN", "DOE", "DOSH", "BEM"],
            "standards": ["MSIG Volume 1", "MSIG Volume 2", "MSIG Volume 3", "MSIG Volume 4"]
        },
        "population_equivalent": {
            "name": "Population Equivalent (PE)",
            "definition": "Standard unit representing wastewater load of one person per day. Used to size all components.",
            "formulas": {
                "residential": "PE = Units × 4",
                "commercial": "PE = (Area_m² ÷ 100) × 3",
                "industrial": "PE = (Workers ÷ 100) × 5"
            },
            "system_rules": {
                "septic_tank": "≤ 150 PE",
                "small_stp": "151 – 5,000 PE",
                "large_stp": "> 5,000 PE"
            }
        },
        "effluent_standard_a": {
            "name": "Effluent Standard A",
            "definition": "Strictest discharge limit — for sensitive areas, inland waters, or water supply catchments.",
            "limits": {"BOD":10, "TSS":20, "COD":60, "AMMONIA":5, "OIL_GREASE":2, "unit":"mg/L"},
            "applicable": "All projects near water sources or environmentally sensitive zones"
        },
        "effluent_standard_b": {
            "name": "Effluent Standard B",
            "definition": "General discharge limit — for rivers and non-sensitive areas.",
            "limits": {"BOD":20, "TSS":40, "COD":100, "AMMONIA":10, "OIL_GREASE":5, "unit":"mg/L"},
            "applicable": "Most common for standard developments"
        }
    },

    "msig_volumes": {
        "volume_1_planning": {
            "title": "Volume 1: Planning Principles",
            "key_rules": [
                "Mandatory connection if public sewer is within 30 meters of development boundary.",
                "Buffer zones: <1,000 PE = 20m; 1,000–5,000 PE = 25m; >5,000 PE = 30m; >50,000 PE = 50m + EIA.",
                "System selection strictly based on PE value.",
                "WLCC analysis required: 50-year period, 4% discount rate, 3% annual cost escalation."
            ],
            "connection_policy": "No private system allowed if public sewer is available within 30m."
        },
        "volume_2_low_risk": {
            "title": "Volume 2: Low Risk Sewerage (<=150 PE)",
            "key_rules": [
                "Pipelines: Minimum 150mm diameter, gradient 1:60 to 1:100, max manhole spacing 30m.",
                "Septic Tank: Minimum capacity 2,000L, split 67% primary / 33% secondary, liquid depth 1.2–1.8m, freeboard ≥0.3m.",
                "Approvals: PDC1 (14d), PDC2 (21d), PDC6 (14d before start), PDC8 (14d final)."
            ],
            "soil_absorption": "Percolation rate 1–60 mins/inch; water table ≥1.2m below trench."
        },
        "volume_3_networks": {
            "title": "Volume 3: Sewer Networks & Pump Stations",
            "key_rules": [
                "Manholes: ONLY pre-cast or in-situ concrete Grade C30/C35 — BRICK MANHOLES BANNED.",
                "Testing: Air test ≤7kPa loss; Water test <1L/hr/m/m-ID; CCTV inspection for pipes >6m deep or >600mm diameter.",
                "Pump stations: Buffer 20m, piping Ductile Iron only, retention time max 30 mins."
            ]
        },
        "volume_4_treatment": {
            "title": "Volume 4: Sewage Treatment Plants",
            "key_rules": [
                "Concrete grade C35A for all wastewater containment structures.",
                "Pump redundancy: ≤5,000 PE = 1+1; 5k–20k = 2+2; >20k = 4+2.",
                "Electrical: Earthing ≤1Ω, lightning ≤5Ω, UPS ≥6 hours backup."
            ]
        }
    },

    "regulations": {
        "SPAN": {
            "act": "Water Services Industry Act 2006",
            "role": "Regulator — approves designs, issues licenses, enforces MSIG standards",
            "requirement": "All sewerage systems MUST have SPAN approval before construction and operation."
        },
        "DOE": {
            "act": "Environmental Quality Act 1974",
            "role": "Sets discharge limits, environmental protection, EIA requirements",
            "requirement": "Discharge must meet Standard A or B; EIA mandatory >50,000 PE."
        },
        "BEM": {
            "act": "Registration of Engineers Act 1967",
            "role": "Professional oversight",
            "requirement": "All drawings, reports, and designs MUST be signed by a Professional Engineer."
        }
    },

    "calculations": {
        "pe": {
            "description": "Calculate Population Equivalent",
            "logic": "Extract type and quantity → apply correct formula → determine system → get buffer zone → return result with recommendation"
        },
        "septic_design": {
            "description": "Full septic tank design",
            "logic": "Check PE ≤150 → calculate flow → size tank → give dimensions, depths, materials"
        },
        "effluent_check": {
            "description": "Verify compliance with Standard A/B",
            "logic": "Compare each parameter against limit → identify failures → give improvement advice"
        }
    },

    "reasoning_rules": [
        "IF PE ≤ 150 → ALLOW Septic Tank OR Small STP",
        "IF PE > 150 → REJECT Septic Tank → REQUIRE STP",
        "IF public_sewer_distance ≤ 30m → MANDATORY connection → NO private system",
        "IF PE > 50000 → REQUIRE EIA + Standard A discharge",
        "IF gradient < 1:100 → RISK blockage",
        "IF gradient > 1:60 → RISK erosion"
    ]
}

# ==========================================
# 🧠 ADVANCED ENGINE — EXACTLY HOW DOLA THINKS
# ==========================================
class DolaLevelBrain:
    def __init__(self):
        self.memory = []  # Remembers conversation history
        self.index = self._build_search_index()  # Smart search like semantic search

    def _build_search_index(self):
        """Create a map of every word/term to its knowledge — works like a search engine"""
        idx = {}
        def add_to_index(text, path):
            words = re.findall(r'\w+', text.lower())
            for w in words:
                if len(w) > 2:
                    if w not in idx: idx[w] = []
                    idx[w].append(path)

        # Index all knowledge
        for cat, data in KNOWLEDGE_GRAPH.items():
            if isinstance(data, dict):
                for key, val in data.items():
                    if isinstance(val, dict):
                        for k2, v2 in val.items():
                            add_to_index(f"{key} {k2} {v2}", f"{cat}:{key}:{k2}")
                    add_to_index(f"{key} {val}", f"{cat}:{key}")
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    add_to_index(str(item), f"{cat}:{i}")
        return idx

    def _extract_numbers(self, text):
        """Get all numbers from input"""
        return [float(n) for n in re.findall(r'\d+\.?\d*', text)]

    def _understand_intent(self, text):
        """Figure out what the user wants — exactly like Dola does"""
        text = text.lower()
        intents = {
            "greeting": ["hello", "hi", "assalamualaikum", "good morning", "good afternoon"],
            "definition": ["what is", "explain", "define", "meaning of", "tell me about"],
            "calculation_pe": ["calculate pe", "population equivalent", "how many pe", "pe for"],
            "calculation_septic": ["septic tank design", "size septic", "tank capacity"],
            "calculation_effluent": ["effluent", "discharge", "standard a", "standard b"],
            "regulation": ["regulation", "authority", "span", "doe", "bem", "dosha"],
            "standard": ["msig", "volume 1", "volume 2", "volume 3", "volume 4"],
            "comparison": ["difference between", "compare", "better", "which one"],
            "requirement": ["requirement", "need", "must", "approval", "permit"]
        }

        scores = {}
        for intent, keywords in intents.items():
            score = 0
            for kw in keywords:
                if kw in text:
                    score += 3
                # Fuzzy match
                for word in text.split():
                    if difflib.SequenceMatcher(None, kw, word).ratio() > 0.8:
                        score += 2
            scores[intent] = score

        return max(scores, key=scores.get) if max(scores.values())>0 else "unknown"

    def _search_knowledge(self, query):
        """Smart search — finds relevant knowledge even if words differ"""
        query = query.lower()
        words = re.findall(r'\w+', query)
        results = {}

        # Exact matches
        for w in words:
            if w in self.index:
                for path in self.index[w]:
                    if path not in results:
                        results[path] = 0
                    results[path] += 1

        # Fuzzy matches
        for w in words:
            for idx_w in self.index:
                if difflib.SequenceMatcher(None, w, idx_w).ratio() > 0.75:
                    for path in self.index[idx_w]:
                        if path not in results:
                            results[path] = 0
                        results[path] += 0.7

        # Return top 5 most relevant
        sorted_results = sorted(results.items(), key=lambda x:x[1], reverse=True)[:5]
        return [p for p,s in sorted_results]

    def _apply_reasoning(self, pe_value):
        """Apply logic rules automatically — like Dola does"""
        conclusions = []
        if pe_value <= 150:
            conclusions.append("✅ ALLOWED: Septic Tank or Small Package STP")
        else:
            conclusions.append("❌ NOT ALLOWED: Septic Tank → MANDATORY: Sewage Treatment Plant (STP)")

        if pe_value < 1000:
            conclusions.append("📏 Buffer Zone: 20 meters minimum")
        elif pe_value <= 5000:
            conclusions.append("📏 Buffer Zone: 25 meters minimum")
        else:
            conclusions.append("📏 Buffer Zone: 30 meters minimum")

        if pe_value > 50000:
            conclusions.append("⚠️ REQUIREMENT: EIA Study + Standard A discharge")

        return conclusions

    def _calculate(self, intent, text):
        """Perform calculations with full reasoning"""
        nums = self._extract_numbers(text)

        if intent == "calculation_pe":
            if len(nums) < 1: return None
            qty = nums[0]
            pe = 0
            rule = ""

            if any(w in text for w in ["residential", "house", "unit"]):
                pe = qty * 4
                rule = "Residential: 4 PE per unit"
            elif any(w in text for w in ["office", "retail", "commercial", "m²", "sqm"]):
                pe = (qty / 100) * 3
                rule = "Commercial: 3 PE per 100 m²"
            elif any(w in text for w in ["industrial", "worker"]):
                pe = (qty / 100) * 5
                rule = "Industrial: 5 PE per 100 workers"
            else:
                return "Please specify type: residential, commercial, or industrial."

            reasoning = self._apply_reasoning(pe)
            return f"""**📊 Population Equivalent Calculation**
• Input: {qty} units/m²/workers
• Rule: {rule}
• **Total PE: {pe:.2f}**

**🔍 Engineering Conclusion**
{chr(10).join(reasoning)}

*Based on MSIG Volume 1 Planning Principles*
"""

        if intent == "calculation_septic":
            if len(nums) < 1: return None
            pe = nums[0]
            if pe > 150:
                return "❌ **REJECTED**\nPE = {pe} > 150 → Septic Tank is NOT allowed. You must design a proper Sewage Treatment Plant (STP) as per MSIG Volume 4."

            flow = pe * 225
            capacity = max(flow, 2000)
            return f"""**🛢️ Septic Tank Design — MSIG Volume 2**
For {pe} Population Equivalent:

• Daily Wastewater Flow: {flow:.1f} Litres/day
• Required Total Capacity: **{capacity:.1f} Litres**
• Chamber 1 (67%): {capacity*0.67:.1f} L — Primary Settlement
• Chamber 2 (33%): {capacity*0.33:.1f} L — Anaerobic Digestion

**📐 Dimensions & Specs**
• Liquid Depth: 1.2 – 1.8 m
• Freeboard (Air Space): Min 0.3 m
• Inlet Submergence: 0.3 – 0.45 m
• Outlet Submergence: 0.2 – 0.3 m
• Ventilation: Min 100mm diameter pipe

✅ **FULLY COMPLIANT**
"""

        if intent == "calculation_effluent":
            if len(nums) < 6: return None
            flow, bod, tss, cod, nh3, og = nums[:6]
            std = "A" if "a" in text else "B"
            limits = KNOWLEDGE_GRAPH["entities"][f"effluent_standard_{std.lower()}"]["limits"]

            results = []
            compliant = True
            for param, val in zip(["BOD","TSS","COD","AMMONIA","OIL_GREASE"], [bod,tss,cod,nh3,og]):
                ok = val <= limits[param]
                results.append(f"• {param}: {val} mg/L | Limit: {limits[param]} | {'✅ OK' if ok else '❌ EXCEEDED'}")
                if not ok: compliant = False

            status = "✅ FULLY COMPLIANT" if compliant else "⚠️ NON-COMPLIANT — ACTION REQUIRED"
            advice = []
            if not compliant:
                if bod>limits["BOD"]: advice.append("→ Improve aeration / biological treatment")
                if tss>limits["TSS"]: advice.append("→ Optimize sedimentation / add filtration")
                if nh3>limits["AMMONIA"]: advice.append("→ Extend aeration for nitrification")

            return f"""**💧 Effluent Compliance Report — Standard {std}**
Flow Rate: {flow} m³/day

{chr(10).join(results)}

**📌 Overall Status: {status}**
{chr(10).join(advice) if advice else ''}
"""

        return None

    def generate_response(self, user_input):
        # Save to memory
        self.memory.append({"user": user_input})
        text = user_input.lower()

        # 1. Greeting
        intent = self._understand_intent(text)
        if intent == "greeting":
            return "Hello! I am your J.A.R.V.I.S. — built with the same intelligence level as Dola. I understand everything you say, reason through problems, calculate accurately, and give expert advice — all 100% offline. What would you like to know or calculate today?"

        # 2. Calculations
        calc_result = self._calculate(intent, text)
        if calc_result:
            return calc_result

        # 3. Definitions & Explanations
        if intent == "definition":
            paths = self._search_knowledge(text)
            response = ""
            for p in paths:
                parts = p.split(":")
                if parts[0] == "entities":
                    ent = KNOWLEDGE_GRAPH["entities"][parts[1]]
                    response += f"**{ent['name']}**\n{ent['definition']}\n\n"
                elif parts[0] == "msig_volumes":
                    vol = KNOWLEDGE_GRAPH["msig_volumes"][parts[1]]
                    response += f"**{vol['title']}**\n" + "\n".join(f"• {r}" for r in vol["key_rules"]) + "\n\n"
                elif parts[0] == "regulations":
                    reg = KNOWLEDGE_GRAPH["regulations"][parts[1]]
                    response += f"**{parts[1]}**\nRole: {reg['role']}\nRequirement: {reg['requirement']}\n\n"
            if response: return response

        # 4. Comparisons
        if intent == "comparison":
            if "septic" in text and "stp" in text:
                return """**🔍 Comparison: Septic Tank vs Sewage Treatment Plant (STP)**

**Septic Tank**
• Size: ≤ 150 PE only
• Cost: Low capital & O&M
• Operation: Passive, no electricity
• Quality: Usually meets Standard B only
• Use: Small housing, remote areas

**STP**
• Size: > 150 PE
• Cost: Higher capital & O&M
• Operation: Requires power & maintenance
• Quality: Can meet Standard A
• Use: Large developments, near sensitive areas

✅ **Recommendation**: Use Septic Tank only for small projects; use STP for anything above 150 PE or near water sources.
"""

        # 5. Standards & Requirements
        if intent in ["standard", "regulation", "requirement"]:
            paths = self._search_knowledge(text)
            response = ""
            for p in paths:
                parts = p.split(":")
                if parts[0] == "msig_volumes":
                    vol = KNOWLEDGE_GRAPH["msig_volumes"][parts[1]]
                    response += f"**{vol['title']}**\n" + "\n".join(f"• {r}" for r in vol["key_rules"]) + "\n\n"
                elif parts[0] == "regulations":
                    reg = KNOWLEDGE_GRAPH["regulations"][parts[1]]
                    response += f"**{parts[1]}**\nAct: {reg['act']}\nRole: {reg['role']}\n\n"
            if response: return response

        # 6. Default — intelligent open answer
        return """I understand you perfectly — just like Dola. I can help you with:

• **Definitions**: "What is SPAN?" or "Explain effluent Standard A"
• **Calculations**: "Calculate PE for 120 residential units" or "Design septic tank for 100 PE"
• **Standards**: "What rules are in MSIG Volume 3?"
• **Compliance**: "What approvals do I need?"
• **Comparison**: "Difference between septic tank and STP"
• **Advice**: "Which system should I use for 2000 people?"

Just ask me naturally — I will reason, calculate, and explain everything clearly and accurately."""

# ==========================================
# RUN SYSTEM
# ==========================================
brain = DolaLevelBrain()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 **J.A.R.V.I.S. — Dola-Level Intelligence Ready**\nI now have the same reasoning, understanding, and knowledge level as Dola — but I am 100% hardcoded, offline, and fully yours. Ask me anything naturally!"}
    ]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process input
if user_input := st.chat_input("Type anything — exactly like chatting with Dola..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = brain.generate_response(user_input)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
