import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide", page_icon="🛡️")

# 1. Connection Handshake
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Loader
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
            st.warning("🌙 Review Mode: Check the Journey tab for your next objective.")

    st.subheader("📋 Preparation Overview")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- FULL COURSE JOURNEY PAGE ---
elif page == "🛤️ Full Course Journey":
    st.title("🛤️ 60-Day Roadmap")
    st.write("Below is your complete study timeline.")
    
    # Timeline Styling
    for index, row in df.iterrows():
        color = "green" if row['Status'] == "Completed" else "blue"
        with st.expander(f"Day {row['Day']}: {row['Subject']} ({row['Status']})"):
            st.write(f"**Topic:** {row['Topic']}")

# --- STUDY PLANNER PAGE ---
elif page == "📅 Study Planner":
    st.title("📅 Roadmap Management")
    if st.button("🚀 Initialize Detailed 60-Day Plan"):
        # Expanded UKPSC Core Syllabus
        full_plan = [
            # WEEK 1: FOUNDATIONS & ANCIENT HISTORY
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient UK (Kuninda/Katyuri)", "Status": "Planned"},
            {"Day": 2, "Subject