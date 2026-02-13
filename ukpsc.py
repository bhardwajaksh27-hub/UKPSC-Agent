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
            st.warning("🌙 Review Mode: Consolidate your notes or plan ahead!")

# --- CALENDAR & JOURNEY PAGE ---
elif page == "📅 Calendar & Journey":
    st.title("📅 Study Schedule & Roadmap")
    
    # Dynamic Calendar Mapping
    start_date = datetime(2026, 2, 13).date()
    cal_list = []
    for i, row in df.iterrows():
        date_obj = start_date + timedelta(days=int(row['Day']) - 1)
        cal_list.append({"Date": date_obj, "Topic": row['Topic'], "Status": row['Status']})
    
    st.write("### 🗓️ Upcoming Schedule")
    st.dataframe(pd.DataFrame(cal_list), use_container_width=True, hide_index=True)

    st.divider()
    st.write("### 🛤️ Detailed Journey Expanders")
    for index, row in df.iterrows():
        with st.expander(f"Day {row['Day']}: {row['Subject']} ({row['Status']})"):
            st.write(f"**Detailed Objective:** {row['Topic']}")
            if row['Notes']:
                st.info(f"📝 **Note:** {row['Notes']}")

# --- STUDY NOTES PAGE ---
elif page == "📝 Study Notes":
    st.title("📝 Sentinel Study Notes")
    if not df.empty:
        selected_topic = st.selectbox("Select Topic to Edit", df['Topic'].unique())
        idx = df[df['Topic'] == selected_topic].index[0]
        
        note_text = st.text_area("Observations/Quick Facts", value=df.at[idx, 'Notes'])
        
        if st.button("💾 Save to Cloud"):
            df.at[idx, 'Notes'] = note_text
            conn.update(worksheet="Tasks", data=df)
            st.success("Notes synced!")
            st.rerun()

# --- SETTINGS / PLANNER ---
elif page == "⚙️ Settings":
    st.title("⚙️ Roadmap Management")
    if st.button("🚀 Initialize Full 60-Day Plan"):
        # THE EXPANDED SYLLABUS LIST
        full_roadmap = [
            {"Day": 1, "Subject": "History", "Topic": "Indus Valley & Ancient UK (Kuninda/Katyuri)", "Status": "Planned", "Notes": ""},
            {"Day": 2, "Subject": "Polity", "Topic": "Preamble & Constitution Parts/Schedules", "Status": "Planned", "Notes": ""},
            {"Day": 3, "Subject": "Geography", "Topic": "Himalayan Rivers & UK Topography", "Status": "Planned", "Notes": ""},
            {"Day": 4, "Subject": "UK GK", "Topic": "Garhwal District Profiles & History", "Status": "Planned", "Notes": ""},
            {"Day": 5, "Subject": "History", "Topic": "Chand & Panwar Dynasties", "Status": "Planned", "Notes": ""},
            {"Day": 6, "Subject": "Economy", "Topic": "UK Budget & Major State Schemes", "Status": "Planned", "Notes": ""},
            {"Day": 7, "Subject": "Revision", "Topic": "Week 1 Cumulative Mock Test", "Status": "Planned", "Notes": ""},
            {"Day": 8, "Subject": "History", "Topic": "Medieval India: Delhi Sultanate & Mughals", "Status": "Planned", "Notes": ""},
            {"Day": 9, "Subject": "Polity", "Topic": "Fundamental Rights & DPSP", "Status": "Planned", "Notes": ""},
            {"Day": 10, "Subject": "Geography", "Topic": "Climate & Forests of India/UK", "Status": "Planned", "Notes": ""},
            {"Day": 11, "Subject": "UK GK", "Topic": "Tribes of Uttarakhand & Culture", "Status": "Planned", "Notes": ""},
            {"Day": 12, "Subject": "History", "Topic": "Gorkha Rule & British Entry in UK", "Status": "Planned", "Notes": ""},
            {"Day": 13, "Subject": "General Science", "Topic": "Human Biology & State Environment", "Status": "Planned", "Notes": ""},
            {"Day": 14, "Subject": "Revision", "Topic": "Week 2 Revision & PYQ Analysis", "Status": "Planned", "Notes": ""},
            # You can simply keep adding rows here to reach Day 60!
        ]
        
        conn.update(worksheet="Tasks", data=pd.DataFrame(full_roadmap))
        st.success("Syllabus expanded to 14 days! (Continue adding rows in code for Day 60)")
        st.rerun()