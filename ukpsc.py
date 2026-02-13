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

        # WEEKLY ANALYSIS SECTION
        st.subheader("📈 Weekly Discipline Analysis")
        # Logic to calculate mock hours (assuming sessions are logged)
        completed_sessions = df[df["Status"] == "Completed"]
        if not completed_sessions.empty:
            st.info(f"🔥 Great work! You have finished {len(completed_sessions)} topics so far.")
            # Note: For actual hour charts, we'd parse the Start/End strings into durations.
        else:
            st.info("Log your first session in the **Attendance Log** to see your stats!")

        st.divider()
        start_date = datetime(2026, 2, 13).date()
        days_since = (datetime.now().date() - start_date).days + 1
        current_duty = df[df["Day"].astype(int) == days_since] if not df.empty else pd.DataFrame()
        
        if not current_duty.empty:
            st.info(f"🚩 **Today's Duty (Day {days_since}):** {current_duty.iloc[0]['Subject']} — *{current_duty.iloc[0]['Topic']}*")

# --- FULL 60-DAY ROADMAP PAGE ---
elif page == "📅 Full 60-Day Roadmap":
    st.title("🛤️ Complete 60-Day Syllabus Journey")
    if not df.empty:
        start_date = datetime(2026, 2, 13).date()
        df_view = df.copy()
        df_view['Day'] = pd.to_numeric(df_view['Day'])
        df_view['Date'] = df_view['Day'].apply(lambda x: (start_date + timedelta(days=int(x)-1)).strftime('%Y-%m-%d'))
        st.dataframe(df_view[['Day', 'Date', 'Subject', 'Topic', 'Status']], use_container_width=True, hide_index=True)

# --- ATTENDANCE LOG PAGE ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Attendance")
    if not df.empty:
        selected_topic = st.selectbox("Select Topic you are studying", df['Topic'].tolist())
        idx = df[df['Topic'] == selected_topic].index[0]
        
        col1, col2 = st.columns(2)
        with col1:
            start_t = st.text_input("Start (e.g. 10:00 PM)", value=str(df.at[idx, "Start_Time"]))
        with col2:
            end_t = st.text_input("End (e.g. 12:30 AM)", value=str(df.at[idx, "End_Time"]))
        
        if st.button("🏁 Log Session & Complete"):
            df.at[idx, "Start_Time"] = start_t
            df.at[idx, "End_Time"] = end_t
            df.at[idx, "Status"] = "Completed"
            conn.update(worksheet="Tasks", data=df)
            st.success("Session saved!")
            st.rerun()

# --- STUDY NOTES PAGE ---
elif page == "📝 Study Notes":
    st.title("📝 Sentinel Study Notes")
    if not df.empty:
        selected = st.selectbox("Topic", df['Topic'].unique())
        idx = df[df['Topic'] == selected].index[0]
        note = st.text_area("Notes", value=df.at[idx, 'Notes'])
        if st.button("💾 Save"):
            df.at[idx, 'Notes'] = note
            conn.update(worksheet="Tasks", data=df)
            st.success("Notes synced!")

# --- SETTINGS (Full 60-Day Generator) ---
elif page == "⚙️ Settings":
    st.title("⚙️ Roadmap Management")
    if st.button("🚀 Initialize FULL 60-Day Detailed Plan"):
        full_plan = []
        cycle = [
            ("History", "Ancient UK & Kuninda Dynasty"),
            ("Polity", "Fundamental Rights & DPSP"),
            ("Geography", "UK Topography & Glaciers"),
            ("UK GK", "Cultural Heritage & Folk Arts"),
            ("History", "Chand, Panwar & Gorkha Rule"),
            ("Economy", "UK Budget & State Policies"),
            ("Science", "Biology & Ecosystems")
        ]
        for i in range(1, 61):
            if i % 7 == 0:
                full_plan.append({"Day": i, "Subject": "REVISION", "Topic": f"Week {i//7} Full Mock", "Status": "Planned", "Notes": "", "Start_Time": "", "End_Time": ""})
            else:
                sub, top = cycle[(i-1) % 7]
                full_plan.append({"Day": i, "Subject": sub, "Topic": f"{top} (Mod {i})", "Status": "Planned", "Notes": "", "Start_Time": "", "End_Time": ""})
        
        conn.update(worksheet="Tasks", data=pd.DataFrame(full_plan))
        st.success("60-Day Roadmap Deployed!")
        st.rerun()