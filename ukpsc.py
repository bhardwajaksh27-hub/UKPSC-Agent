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
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Control")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 Full 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Settings"])

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
        start_date = datetime(2026, 2, 13).date()
        days_since = (datetime.now().date() - start_date).days + 1
        current_duty = df[df["Day"].astype(int) == days_since] if not df.empty else pd.DataFrame()
        
        if not current_duty.empty:
            st.info(f"🚩 **Today's Duty (Day {days_since}):** {current_duty.iloc[0]['Subject']} — *{current_duty.iloc[0]['Topic']}*")
            if current_duty.iloc[0]['Resources']:
                st.link_button("📖 Open Resource", current_duty.iloc[0]['Resources'])

# --- DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Sentinel Digital Library")
    st.write("Attach PDF links or Drive URLs to specific topics for 1-click access.")
    
    if not df.empty:
        target_topic = st.selectbox("Assign Resource to:", df['Topic'].tolist())
        idx = df[df['Topic'] == target_topic].index[0]
        res_link = st.text_input("Paste URL (Google Drive/PDF link):", value=str(df.at[idx, "Resources"]) if "Resources" in df.columns else "")
        
        if st.button("🔗 Update Library"):
            df.at[idx, "Resources"] = res_link
            conn.update(worksheet="Tasks", data=df)
            st.success(f"Resource linked to {target_topic}!")

# --- FULL 60-DAY ROADMAP ---
elif page == "📅 Full 60-Day Roadmap":
    st.title("🛤️ 60-Day Integrated Roadmap")
    if not df.empty:
        start_date = datetime(2026, 2, 13).date()
        df_view = df.copy()
        df_view['Day'] = pd.to_numeric(df_view['Day'])
        df_view['Date'] = df_view['Day'].apply(lambda x: (start_date + timedelta(days=int(x)-1)).strftime('%Y-%m-%d'))
        st.dataframe(df_view[['Day', 'Date', 'Subject', 'Topic', 'Status', 'Resources']], use_container_width=True, hide_index=True)

# --- ATTENDANCE & NOTES (Standard Sentinel Logic) ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Attendance")
    selected_topic = st.selectbox("Select Topic", df['Topic'].tolist())
    idx = df[df['Topic'] == selected_topic].index[0]
    col1, col2 = st.columns(2)
    with col1: s_time = st.text_input("Start", value=str(df.at[idx, "Start_Time"]))
    with col2: e_time = st.text_input("End", value=str(df.at[idx, "End_Time"]))
    if st.button("🏁 Log Session"):
        df.at[idx, "Start_Time"], df.at[idx, "End_Time"], df.at[idx, "Status"] = s_time, e_time, "Completed"
        conn.update(worksheet="Tasks", data=df); st.rerun()

elif page == "📝 Study Notes":
    st.title("📝 Sentinel Study Notes")
    selected = st.selectbox("Topic", df['Topic'].unique())
    idx = df[df['Topic'] == selected].index[0]
    note = st.text_area("Notes", value=df.at[idx, 'Notes'])
    if st.button("💾 Save"):
        df.at[idx, 'Notes'] = note
        conn.update(worksheet="Tasks", data=df); st.success("Notes synced!")

# --- SETTINGS (The 60-Day Engine) ---
elif page == "⚙️ Settings":
    st.title("⚙️ Roadmap Management")
    if st.button("🚀 Initialize FULL 60-Day Resource-Ready Plan"):
        plan = []
        cycle = [("History", "Ancient UK"), ("Polity", "Constitutional Core"), ("Geography", "UK Topography"), ("UK GK", "Cultural Heritage"), ("History", "Modern UK"), ("Economy", "State Budget"), ("Science", "Environment")]
        for i in range(1, 61):
            if i % 7 == 0:
                plan.append({"Day": i, "Subject": "REVISION", "Topic": f"Week {i//7} Mock", "Status": "Planned", "Notes": "", "Start_Time": "", "End_Time": "", "Resources": ""})
            else:
                sub, top = cycle[(i-1) % 7]
                plan.append({"Day": i, "Subject": sub, "Topic": f"{top} (Mod {i})", "Status": "Planned", "Notes": "", "Start_Time": "", "End_Time": "", "Resources": ""})
        conn.update(worksheet="Tasks", data=pd.DataFrame(plan))
        st.success("60-Day Integrated Roadmap Deployed!"); st.rerun()