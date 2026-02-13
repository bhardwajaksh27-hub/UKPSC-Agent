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
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time"])

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Control")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 Full 60-Day Roadmap", "⏱️ Attendance Log", "📝 Study Notes", "⚙️ Settings"])

# --- DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    if not df.empty:
        # Progress Calculations
        total = len(df)
        completed = len(df[df["Status"] == "Completed"])
        progress_val = completed / total if total > 0 else 0
        
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.metric("Total Days", total)
        c2.metric("Days Completed", completed)
        with c3:
            st.write("**Overall Preparation Progress**")
            st.progress(progress_val)
        
        st.divider()
        # Today's Specific Task
        start_date = datetime(2026, 2, 13).date()
        days_since = (datetime.now().date() - start_date).days + 1
        current_duty = df[df["Day"].astype(int) == days_since]
        
        if not current_duty.empty:
            st.info(f"🚩 **Today's Sentinel Duty (Day {days_since}):** {current_duty.iloc[0]['Subject']} — *{current_duty.iloc[0]['Topic']}*")
        else:
            st.warning("🌙 Review Mode: Full 60-day plan loaded. Check the Roadmap to see upcoming topics!")

# --- FULL 60-DAY ROADMAP PAGE ---
elif page == "📅 Full 60-Day Roadmap":
    st.title("🛤️ Complete 60-Day Syllabus Journey")
    st.write("This view always displays your full 60-day plan.")
    
    start_date = datetime(2026, 2, 13).date()
    df_full = df.copy()
    df_full['Date'] = df_full['Day'].apply(lambda x: (start_date + timedelta(days=int(x)-1)).strftime('%Y-%m-%d'))
    
    # Visual Highlights for the Roadmap
    st.dataframe(
        df_full[['Day', 'Date', 'Subject', 'Topic', 'Status']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status", options=["Planned", "Completed", "In Progress"]
            )
        }
    )

# --- ATTENDANCE LOG PAGE ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Attendance")
    selected_topic = st.selectbox("Select Topic to Log Hours", df['Topic'].tolist())
    idx = df[df['Topic'] == selected_topic].index[0]
    
    col1, col2 = st.columns(2)
    with col1:
        s_time = st.text_input("Start Time", value=df.at[idx, "Start_Time"] if "Start_Time" in df.columns else "10:00 PM")
    with col2:
        e_time = st.text_input("End_Time", value=df.at[idx, "End_Time"] if "End_Time" in df.columns else "12:00 AM")
    
    if st.button("🏁 Clock Out & Mark Done"):
        df.at[idx, "Start_Time"] = s_time
        df.at[idx, "End_Time"] = e_time
        df.at[idx, "Status"] = "Completed"
        conn.update(worksheet="Tasks", data=df)
        st.success("Attendance Logged!")
        st.rerun()

# --- STUDY NOTES PAGE ---
elif page == "📝 Study Notes":
    st.title("📝 Sentinel Quick Facts")
    selected = st.selectbox("Topic", df['Topic'].unique())
    idx = df[df['Topic'] == selected].index[0]
    note = st.text_area("Notes", value=df.at[idx, 'Notes'] if "Notes" in df.columns else "")
    if st.button("💾 Save"):
        df.at[idx, 'Notes'] = note
        conn.update(worksheet="Tasks", data=df)
        st.success("Cloud Updated!")

# --- SETTINGS (The 60-Day Engine) ---
elif page == "⚙️ Settings":
    st.title("⚙️ Engine Room")
    if st.button("🚀 Re-Initialize FULL 60-Day Syllabus"):
        # COMPREHENSIVE 60-DAY PLAN
        plan = []
        subjects = [
            ("History", "Ancient & Medieval Foundations"),
            ("Polity", "Constitutional Framework"),
            ("Geography", "Physical & UK Geography"),
            ("UK GK", "State Cultural Heritage"),
            ("History", "Modern Indian Movement"),
            ("Economy", "Indian & State Economic Surveys"),
            ("Science", "General Science & Environment")
        ]
        
        # Generating 60 detailed entries
        for i in range(1, 61):
            sub, top = subjects[(i-1) % len(subjects)]
            # Add logic for Revision every 7th day
            if i % 7 == 0:
                plan.append({"Day": i, "Subject": "REVISION", "Topic": f"Week {i//7} Comprehensive Mock Test", "Status": "Planned"})
            else:
                plan.append({"Day": i, "Subject": sub, "Topic": f"{top} - Detailed Study Part {i}", "Status": "Planned"})
        
        conn.update(worksheet="Tasks", data=pd.DataFrame(plan))
        st.success("The full 60-day roadmap is now live!")
        st.rerun()