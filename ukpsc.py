import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide")

# 1. Establish Connection using Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Sidebar Navigation
st.sidebar.title("🛡️ Sentinel Control")
page = st.sidebar.radio("Navigate", ["Dashboard", "Study Planner", "Settings"])

# 3. Load Data with Cache Clearing (ttl=0)
try:
    # Explicitly targeting the 'Tasks' worksheet
    df = conn.read(worksheet="Tasks", ttl=0)
except Exception as e:
    st.error("Connection Pending: Please ensure the Google Sheet has a tab named 'Tasks'.")
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status"])

# --- DASHBOARD PAGE ---
if page == "Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    
    # Calculate Progress for the Ring
    if not df.empty and "Status" in df.columns:
        total_tasks = len(df)
        completed_tasks = len(df[df["Status"] == "Completed"])
        progress = completed_tasks / total_tasks if total_tasks > 0 else 0
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Progress", f"{int(progress * 100)}%")
            # Progress Ring/Bar
            st.progress(progress)
        with col2:
            st.info(f"You have completed {completed_tasks} out of {total_tasks} topics.")
    
    st.subheader("📊 Preparation Overview")
    st.dataframe(df, use_container_width=True)

# --- STUDY PLANNER PAGE ---
elif page == "Study Planner":
    st.title("📅 Chapter-Wise Study Tracker")
    
    if st.button("🚀 Initialize 60-Day Master Plan"):
        # Define the Master Plan structure
        master_plan = pd.DataFrame([
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient Uttarakhand", "Status": "Planned"},
            {"Day": 2, "Subject": "Polity", "Topic": "Preamble & Fundamental Rights", "Status": "Planned"},
            {"Day": 3, "Subject": "Geography", "Topic": "Himalayan Rivers & Topography", "Status": "Planned"},
            # Add remaining days here...
        ])
        
        try:
            # Pushing data to GSheets
            conn.update(worksheet="Tasks", data=master_plan)
            st.success("Master Plan deployed to Google Sheets! Refreshing...")
            st.rerun()
        except Exception as e:
            st.error(f"Write Access Error: {e}")
            st.info("Check if 'Anyone with the link' is set to Editor in Google Sheets.")

# --- SETTINGS PAGE ---
elif page == "Settings":
    st.title("⚙️ Sentinel Settings")
    st.write(f"Connected as: {st.secrets['connections']['gsheets']['client_email']}")
    st.write(f"Project ID: {st.secrets['connections']['gsheets']['project_id']}")