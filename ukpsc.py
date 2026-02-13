import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🛡️")

# 2. Cloud Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Defensive Data Loader (The Fix for your KeyError)
try:
    df = conn.read(worksheet="Tasks", ttl=0)
    # Ensure all required columns exist in the dataframe
    required_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = "" # Automatically creates the missing column
except Exception:
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

# 4. Sidebar Navigation
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Settings"])

# --- DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    if not df.empty:
        total = len(df)
        completed = df[df["Status"] == "Completed"]
        progress_val = len(completed) / total if total > 0 else 0
        
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.metric("Total Topics", total)
        c2.metric("Days Mastered", len(completed))
        with c3:
            st.write("**Overall Preparation Mastery**")
            st.progress(progress_val)
        
        st.divider()

        # Late Night Study Hours Calculation
        total_hours = 0.0
        for _, row in completed.iterrows():
            try:
                fmt = "%I:%M %p"
                start = datetime.strptime(str(row["Start_Time"]), fmt)
                end = datetime.strptime(str(row["End_Time"]), fmt)
                if end < start: end += timedelta(days=1) # Midnight logic
                total_hours += (end - start).total_seconds() / 3600
            except: continue
        
        st.subheader(f"📊 Discipline Score: {total_hours:.1f} Total Study Hours")

        st.divider()
        start_date = datetime(2026, 2, 13).date()
        days_since = (datetime.now().date() - start_date).days + 1
        df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
        current_duty = df[df["Day"] == days_since]
        
        if not current_duty.empty:
            st.info(f"🚩 **Today's Topic (Day {days_since}):** {current_duty.iloc[0]['Subject']} — {current_duty.iloc[0]['Topic']}")
            res_url = current_duty.iloc[0].get('Resources', "")
            if pd.notna(res_url) and str(res_url).strip() != "":
                st.link_button("🔓 Open Today's PDF", res_url, type="primary")

# --- FULL 60-DAY ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("🛤️ Full Syllabus Roadmap")
    if not df.empty:
        start_date = datetime(2026, 2, 13).date()
        df_view = df.copy()
        df_view['Day'] = pd.to_numeric(df_view['Day'])
        df_view['Date'] = df_view['Day'].apply(lambda x: (start_date + timedelta(days=int(x)-1)).strftime('%d %b %Y'))
        st.dataframe(df_view[['Day', 'Date', 'Subject', 'Topic', 'Status']], use_container_width=True, hide_index=True)

# --- ATTENDANCE LOG ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Attendance")
    if not df.empty:
        selected_topic = st.selectbox("Assign hours to topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == selected_topic].index[0]
        col1, col2 = st.columns(2)
        with col1: start_t = st.text_input("Start (10:00 PM)", value=str(df.at[idx, "Start_Time"]))
        with col2: end_t = st.text_input("End (12:00 AM)", value=str(df.at[idx, "End_Time"]))
        if st.button("🏁 Log Session & Complete"):
            df.at[idx, "Start_Time"], df.at[idx, "End_Time"], df.at[idx, "Status"] = start_t, end_t, "Completed"
            conn.update(worksheet="Tasks", data=df)
            st.success("Session saved!"); st.rerun()

# --- DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Digital Library")
    if not df.empty:
        topic_to_link = st.selectbox("Assign link to topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == topic_to_link].index[0]
        # Safe string conversion for Resources
        existing_val = df.at[idx, "Resources"]
        val_to_show = str(existing_val) if pd.notna(existing_val) else ""
        url = st.text_input("Paste Drive/PDF URL:", value=val_to_show if val_to_show != "nan" else "")
        if st.button("🔗 Save Link"):
            df.at[idx, "Resources"] = url
            conn.update(worksheet="Tasks", data=df); st.success("Resource Saved!")

# --- STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 Sentinel Study Notes")
    if not df.empty:
        selected = st.selectbox("Topic", df['Topic'].unique())
        idx = df[df['Topic'] == selected].index[0]
        note = st.text_area("Key Facts", value=df.at[idx, 'Notes'])
        if st.button("💾 Save"):
            df.at[idx, 'Notes'] = note
            conn.update(worksheet="Tasks", data=df); st.success("Notes Synced!")

# --- SETTINGS ---
elif page == "⚙️ Settings":
    st.title("⚙️ Engine Room")
    if st.button("🚀 Initialize FULL 60-Day Roadmap"):
        plan = []
        cycle = [("History", "Ancient UK"), ("Polity", "Constitution"), ("Geography", "Rivers"), ("UK GK", "Districts"), ("History", "Modern UK"), ("Economy", "Budget"), ("Science", "Environment")]
        for i in range(1, 61):
            if i % 7 == 0:
                plan.append({"Day": i, "Subject": "REVISION", "Topic": f"Week {i//7} Mock", "Status": "Planned", "Notes": "", "Start_Time": "10:00 PM", "End_Time": "12:00 AM", "Resources": ""})
            else:
                sub, top = cycle[(i-1) % 7]
                plan.append({"Day": i, "Subject": sub, "Topic": f"{top} (Part {i})", "Status": "Planned", "Notes": "", "Start_Time": "10:00 PM", "End_Time": "12:00 AM", "Resources": ""})
        conn.update(worksheet="Tasks", data=pd.DataFrame(plan))
        st.success("60-Day Roadmap Deployed!"); st.rerun()