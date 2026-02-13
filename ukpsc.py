import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide", page_icon="🛡️")

# 1. Connection Handshake
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Loader
try:
    df = conn.read(worksheet="Tasks", ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes"])

# Ensure Notes column exists
if "Notes" not in df.columns:
    df["Notes"] = ""

# 3. Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=80)
st.sidebar.title("Sentinel Control")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 Calendar & Journey", "📝 Study Notes", "⚙️ Settings"])

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
            st.info(f"🚩 **Sentinel Duty (Day {days_since_start}):** {current_duty.iloc[0]['Subject']} — *{current_duty.iloc[0]['Topic']}*")
        else:
            st.warning("🌙 Review Mode: Consolidate your notes!")

    st.subheader("📋 Preparation Overview")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- CALENDAR & JOURNEY PAGE ---
elif page == "📅 Calendar & Journey":
    st.title("📅 Study Schedule & Roadmap")
    
    # Simple Calendar View
    start_date = datetime(2026, 2, 13).date()
    cal_data = []
    for i, row in df.iterrows():
        date_obj = start_date + timedelta(days=int(row['Day']) - 1)
        cal_data.append({"Date": date_obj, "Topic": row['Topic'], "Status": row['Status']})
    
    st.write("### 🗓️ Upcoming Schedule")
    st.table(pd.DataFrame(cal_data).set_index("Date").head(14)) # Shows next 2 weeks

    st.divider()
    st.write("### 🛤️ Detailed Journey Expanders")
    for index, row in df.iterrows():
        with st.expander(f"Day {row['Day']}: {row['Subject']} ({row['Status']})"):
            st.write(f"**Topic:** {row['Topic']}")
            if row['Notes']:
                st.caption(f"📝 Quick Note: {row['Notes']}")

# --- STUDY NOTES PAGE ---
elif page == "📝 Study Notes":
    st.title("📝 Sentinel Study Notes")
    st.write("Select a topic to save quick facts or review pointers.")
    
    if not df.empty:
        selected_topic = st.selectbox("Choose a Topic", df['Topic'].tolist())
        current_note = df[df['Topic'] == selected_topic]['Notes'].values[0]
        
        new_note = st.text_area("Write your notes here:", value=str(current_note) if current_note else "")
        
        if st.button("💾 Save Note"):
            df.loc[df['Topic'] == selected_topic, 'Notes'] = new_note
            try:
                conn.update(worksheet="Tasks", data=df)
                st.success(f"Notes for '{selected_topic}' saved to Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Sync Error: {e}")
    else:
        st.warning("Please initialize your plan first.")

# --- SETTINGS PAGE ---
elif page == "⚙️ Settings":
    st.title("⚙️ System Configuration")
    if st.button("🚀 Re-Initialize Full 60-Day Plan"):
        # Initializing first 14 days of high-yield topics
        full_plan = [
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient UK", "Status": "Planned", "Notes": ""},
            {"Day": 2, "Subject": "Polity", "Topic": "Preamble & Constitution Parts", "Status": "Planned", "Notes": ""},
            {"Day": 3, "Subject": "Geography", "Topic": "Himalayan Rivers", "Status": "Planned", "Notes": ""},
            {"Day": 4, "Subject": "UK GK", "Topic": "Garhwal District Profiles", "Status": "Planned", "Notes": ""},
            {"Day": 5, "Subject": "History", "Topic": "Chand & Panwar Dynasties", "Status": "Planned", "Notes": ""},
            {"Day": 6, "Subject": "Economy", "Topic": "UK Budget Highlights", "Status": "Planned", "Notes": ""},
            {"Day": 7, "Subject": "Revision", "Topic": "Week 1 Cumulative Mock", "Status": "Planned", "Notes": ""},
        ]
        conn.update(worksheet="Tasks", data=pd.DataFrame(full_plan))
        st.success("Detailed Roadmap Initialized!")
        st.rerun()