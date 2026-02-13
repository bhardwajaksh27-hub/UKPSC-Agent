import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide", page_icon="🛡️")

# 1. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Load Data (ttl=0 ensures fresh data every time)
try:
    df = conn.read(worksheet="Tasks", ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status"])

# 3. Sidebar Navigation
st.sidebar.title("🛡️ Sentinel Control")
page = st.sidebar.radio("Navigate", ["Dashboard", "Study Planner", "Settings"])

# --- DASHBOARD PAGE ---
if page == "Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    
    # CALCULATE PROGRESS RING
    if not df.empty and "Status" in df.columns:
        total = len(df)
        completed = len(df[df["Status"] == "Completed"])
        progress_val = completed / total if total > 0 else 0
        
        # Dashboard Layout
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Total Topics", total)
        with col2:
            st.metric("Progress", f"{int(progress_val * 100)}%")
        with col3:
            st.write("**Course Completion**")
            st.progress(progress_val)
            
        st.divider()

        # DAILY NOTIFICATION LOGIC
        # We assume Day 1 starts today (Feb 13). You can adjust this start date.
        start_date = datetime(2026, 2, 13).date()
        today = datetime.now().date()
        days_since_start = (today - start_date).days + 1
        
        current_topic = df[df["Day"] == days_since_start]
        
        if not current_topic.empty:
            topic_name = current_topic.iloc[0]["Topic"]
            subject_name = current_topic.iloc[0]["Subject"]
            st.info(f"📅 **Today's Sentinel Duty (Day {days_since_start}):** {subject_name} — *{topic_name}*")
        else:
            st.warning("🌙 No specific duty assigned for today. Review previous notes!")

    st.subheader("📊 Preparation Overview")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- STUDY PLANNER PAGE ---
elif page == "Study Planner":
    st.title("📅 Chapter-Wise Study Tracker")
    st.write("Click below to generate or reset your 60-day roadmap.")
    
    if st.button("🚀 Initialize 60-Day Master Plan"):
        # The core plan data
        master_plan = pd.DataFrame([
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient Uttarakhand", "Status": "Planned"},
            {"Day": 2, "Subject": "Polity", "Topic": "Preamble & Fundamental Rights", "Status": "Planned"},
            {"Day": 3, "Subject": "Geography", "Topic": "Himalayan Rivers & Topography", "Status": "Planned"},
            {"Day": 4, "Subject": "Economy", "Topic": "Uttarakhand Budget & State Schemes", "Status": "Planned"},
            {"Day": 5, "Subject": "History", "Topic": "Katyuri & Chand Dynasty", "Status": "Planned"},
            # Note: You can expand this list to all 60 days!
        ])
        
        try:
            conn.update(worksheet="Tasks", data=master_plan)
            st.success("✅ Roadmap deployed to Google Sheets! Page will refresh...")
            st.rerun()
        except Exception as e:
            st.error(f"Write Access Error: {e}")
            st.info("Check if 'Anyone with the link' is still set to Editor.")

# --- SETTINGS PAGE ---
elif page == "Settings":
    st.title("⚙️ Sentinel Settings")
    st.write(f"**Connected Project:** {st.secrets['connections']['gsheets']['project_id']}")
    st.write(f"**Service Account:** {st.secrets['connections']['gsheets']['client_email']}")