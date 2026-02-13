import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide", page_icon="🛡️")

# 1. Connection Handshake
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Loader (ttl=0 for real-time sync)
try:
    df = conn.read(worksheet="Tasks", ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status"])

# 3. Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=80)
st.sidebar.title("Sentinel Control")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "🛤️ Full Course Journey", "📅 Study Planner", "⚙️ Settings"])

# --- DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    
    if not df.empty:
        # Progress Calculation
        total = len(df)
        completed = len(df[df["Status"] == "Completed"])
        progress_val = completed / total if total > 0 else 0
        
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.metric("Total Topics", total)
        c2.metric("Progress", f"{int(progress_val * 100)}%")
        with c3:
            st.write("**Overall Completion**")
            st.progress(progress_val)
            
        st.divider()

        # DAILY NOTIFICATION
        start_date = datetime(2026, 2, 13).date()
        today = datetime.now().date()
        days_since_start = (today - start_date).days + 1
        
        current_duty = df[df["Day"] == days_since_start]
        
        if not current_duty.empty:
            topic = current_duty.iloc[0]["Topic"]
            sub = current_duty.iloc[0]["Subject"]
            st.info(f"🚩 **Sentinel Duty (Day {days_since_start}):** {sub} — *{topic}*")
        else:
            st.warning("🌙 Review Mode: No new duty for today. Check the Full Journey tab for tomorrow's goal.")

    st.subheader("📋 Preparation Overview")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- FULL COURSE JOURNEY PAGE ---
elif page == "🛤️ Full Course Journey":
    st.title("🛤️ 60-Day Full Course Journey")
    st.write("View your complete roadmap from Day 1 to Day 60 below.")
    
    # Filter by Status
    status_filter = st.multiselect("Filter by Status", options=["Planned", "Completed", "In Progress"], default=["Planned", "Completed", "In Progress"])
    
    filtered_journey = df[df["Status"].isin(status_filter)]
    
    # Timeline Styling
    for index, row in filtered_journey.iterrows():
        with st.expander(f"Day {row['Day']}: {row['Subject']} - {row['Status']}"):
            st.write(f"**Topic:** {row['Topic']}")
            if row['Status'] == "Completed":
                st.success("Target Achieved")
            else:
                st.info("Upcoming Objective")

# --- STUDY PLANNER PAGE ---
elif page == "📅 Study Planner":
    st.title("📅 Roadmap Management")
    if st.button("🚀 Re-Initialize Master Plan"):
        # Expanded 60-day plan template
        master_plan = pd.DataFrame([
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient Uttarakhand", "Status": "Planned"},
            {"Day": 2, "Subject": "Polity", "Topic": "Preamble & Fundamental Rights", "Status": "Planned"},
            {"Day": 3, "Subject": "Geography", "Topic": "Himalayan Rivers & Topography", "Status": "Planned"},
            {"Day": 4, "Subject": "Economy", "Topic": "Uttarakhand Budget & State Schemes", "Status": "Planned"},
            {"Day": 5, "Subject": "History", "Topic": "Katyuri & Chand Dynasty", "Status": "Planned"},
            {"Day": 6, "Subject": "General Science", "Topic": "Basic Physics & UK Environment", "Status": "Planned"},
            {"Day": 7, "Subject": "Revision", "Topic": "Week 1 Mock Test", "Status": "Planned"},
            # You can keep adding up to Day 60 here
        ])
        
        try:
            conn.update(worksheet="Tasks", data=master_plan)
            st.success("Roadmap Successfully Populated!")
            st.rerun()
        except Exception as e:
            st.error(f"Sync Error: {e}")

# --- SETTINGS PAGE ---
elif page == "⚙️ Settings":
    st.title("⚙️ System Configuration")
    st.write(f"**Cloud Project:** {st.secrets['connections']['gsheets']['project_id']}")
    st.write(f"**Data Source:** [UKPSC_Data](https://docs.google.com/spreadsheets/d/1JyYMAXrROq0P1FbwHbNag3aRUcEKD7ljJtttVwvPIZQ/edit)")