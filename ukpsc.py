import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🛡️")

# 2. Cloud Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Defensive Data Loader
try:
    df = conn.read(worksheet="Tasks", ttl=0)
    # Ensure all required columns exist in the dataframe to avoid KeyErrors
    required_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
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

        # Calculation of Total Study Hours
        total_hours = 0.0
        for _, row in completed.iterrows():
            try:
                # Expecting format like "10:00 PM"
                fmt = "%I:%M %p"
                start = datetime.strptime(str(row["Start_Time"]), fmt)
                end = datetime.strptime(str(row["End_Time"]), fmt)
                # Handle late night sessions crossing midnight
                if end < start: end += timedelta(days=1)
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

# --- DIGITAL LIBRARY (Defensive Fix) ---
elif page == "📚 Digital Library":
    st.title("📚 Sentinel Digital Library")
    if not df.empty:
        topic_to_link = st.selectbox("Assign resource to topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == topic_to_link].index[0]
        
        # Use .get to safely access potential missing columns
        current_res = df.at[idx, "Resources"] if "Resources" in df.columns else ""
        url = st.text_input("Paste Drive/PDF Link:", value=str(current_res) if pd.notna(current_res) else "")
        
        if st.button("🔗 Update Library"):
            df.at[idx, "Resources"] = url
            conn.update(worksheet="Tasks", data=df)
            st.success("Resource successfully linked to topic!")

# --- SETTINGS (Full Force Reset) ---
elif page == "⚙️ Settings":
    st.title("⚙️ Engine Room")
    st.warning("Clicking Initialize will deploy the full 60-day roadmap and fix any column errors.")
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
        st.success("Sentinel system reset and fully deployed!"); st.rerun()

# (Include Roadmap, Attendance, and Notes tabs as previously designed)