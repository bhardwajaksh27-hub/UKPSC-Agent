import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide", page_icon="🏔️")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏔️ Sentinel Control")
page = st.sidebar.radio("Navigate", ["Dashboard", "Daily Briefing", "Study Planner", "Settings"])

# --- CORE FUNCTION: PRE-FED SYLLABUS ---
def get_master_plan():
    # Example snippet of the 60-day plan (You can expand this list)
    return [
        {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient UK", "Status": "Planned"},
        {"Day": 5, "Subject": "History", "Topic": "Mauryan Empire & Kunindas", "Status": "Planned"},
        {"Day": 12, "Subject": "Polity", "Topic": "Fundamental Rights & UK Assembly", "Status": "Planned"},
        {"Day": 26, "Subject": "Geography", "Topic": "Ganga River System & UK Hydrology", "Status": "Planned"},
        {"Day": 46, "Subject": "Env", "Topic": "Biodiversity & UK National Parks", "Status": "Planned"},
    ]

# --- PAGE: STUDY PLANNER ---
if page == "Study Planner":
    st.header("📅 Chapter-Wise Study Tracker")
    
    # 1. Fetch current data from Google Sheets
    try:
        df = conn.read(worksheet="Tasks")
    except:
        df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status"])

    # 2. Bulk Upload Button
    if st.sidebar.button("🚀 Initialize 60-Day Master Plan"):
        master_plan = pd.DataFrame(get_master_plan())
        conn.update(worksheet="Tasks", data=master_plan)
        st.success("Master Plan injected into Google Sheets!")
        st.rerun()

    # 3. Manual Entry Form
    with st.expander("➕ Add Custom Task"):
        with st.form("new_task"):
            d = st.number_input("Day", min_value=1, max_value=60)
            sub = st.selectbox("Subject", ["History", "Polity", "Geography", "Economy", "UK GK", "Env/Sci"])
            top = st.text_input("Topic Name")
            if st.form_submit_button("Add Task"):
                new_row = pd.DataFrame([{"Day": d, "Subject": sub, "Topic": top, "Status": "Planned"}])
                df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Tasks", data=df)
                st.rerun()

    # 4. Display Tracker
    st.dataframe(df.sort_values(by="Day"), use_container_width=True, hide_index=True)

# --- PAGE: DASHBOARD ---
elif page == "Dashboard":
    st.header("📊 Preparation Overview")
    col1, col2, col3 = st.columns(3)
    
    df = conn.read(worksheet="Tasks")
    total = len(df)
    done = len(df[df['Status'] == 'Completed'])
    
    col1.metric("Total Topics", total)
    col2.metric("Completed", done)
    col3.metric("Remaining", total - done)
    
    st.progress(done/total if total > 0 else 0)

# --- PAGE: DAILY BRIEFING ---
elif page == "Daily Briefing":
    st.header("🗞️ High-Yield Briefing (Feb 13, 2026)")
    st.info("Target: Focus on UK Hydro-power projects and Current National Budget.")
    st.markdown("""
    1. **Sharda Corridor**: Environmental impact study released.
    2. **UCC Uttarakhand**: 1st Anniversary implementation report.
    3. **Ganga Water Quality**: CPCB report on Haridwar stretch.
    """)