import os
import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="J.A.R.V.I.S. | Sewerage Compliance", layout="wide")
DATA_DIR = "data"

# --- 2. DATA INGESTION ENGINE ---
@st.cache_data
def load_msig_data():
    """Aggregates all MSIG CSV files into a searchable regulatory knowledge base."""
    combined_knowledge = "REGULATORY REFERENCE DATA:\n"
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(DATA_DIR, file))
            combined_knowledge += f"\nFILE SOURCE: {file}\n{df.to_string()}\n"
    return combined_knowledge

# --- 3. CORE PROMPT ---
JARVIS_MASTER_PROMPT = f"""
You are A.I.M.E.C.H.A. J.A.R.V.I.S., a Senior Sewerage Compliance Engineer.
Use the provided MSIG data as your absolute source of truth. 

MANDATES:
1. Always cite the Source File and Section/Reference code.
2. If calculating, use the precise formula from the CSV.
3. For compliance queries, state if the design passes or fails based on the CSV constraints.
4. If a query is not in the MSIG database, refer the user to local PBT guidelines.
"""

# --- 4. STREAMLIT UI ---
st.title("🤖 A.I.M.E.C.H.A. J.A.R.V.I.S. System")
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. EXECUTION LOOP ---
def run_jarvis():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    reg_context = load_msig_data()
    
    # User Input
    if prompt := st.chat_input("Query regulatory requirements..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Craft Context-Aware Prompt
        final_prompt = f"{reg_context}\n\nUSER QUERY: {prompt}"
        
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=final_prompt,
                config=types.GenerateContentConfig(system_instruction=JARVIS_MASTER_PROMPT)
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

if __name__ == "__main__":
    run_jarvis()
