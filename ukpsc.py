import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Connection
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🛡️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Loading & Self-Healing (Prevents KeyErrors)
try:
    df = conn.read(worksheet="Tasks", ttl=0)
    required_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    for col in required_cols:
        if col not in df.columns: 
            df[col] = ""
    # Ensure Day is numeric for the shifting logic
    df["Day"] = pd.to_numeric(df["Day"], errors='coerce').fillna(0).astype(int)
except Exception as e:
    st.error(f"Connection Error: {e}")
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- BREAK DAY LOGIC ---
def trigger_break_day(current_day_val):
    # Shift all tasks from today onwards by +1 day
    mask = df["Day"] >= current_day_val
    df.loc[mask, "Day"] = df.loc[mask, "Day"] + 1
    conn.update(worksheet="Tasks", data=df)
    st.toast(f"Schedule shifted! Day {current_day_val} is now a Break Day.", icon="☕")
    st.rerun()

# --- DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    
    # Calculate current day based on start date Feb 13, 2026
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    c1, c2 = st.columns([2, 1])
    with c1:
        today_task = df[df["Day"] == days_passed]
        if not today_task.empty:
            st.info(f"🚩 **Today's Duty (Day {days_passed}):** {today_task.iloc[0]['Subject']} — {today_task.iloc[0]['Topic']}")
            
            # --- FIXED LINK BUTTON LOGIC ---
            res_url = today_task.iloc[0].get('Resources', "")
            if pd.notna(res_url) and str(res_url).strip() != "" and str(res_url).lower() != "nan":
                st.link_button("📖 Open Today's Resource", str(res_url), type="primary")
            else:
                st.warning("⚠️ No resource linked for today. Add a URL in the 'Digital Library' tab!")
        else:
            st.success("You are ahead of schedule or have completed the 60 days!")

    with c2:
        st.write("### 🚨 Schedule Adjustment")
        if st.button("☕ Take a Break Today"):
            trigger_break_day(days_passed)
    
    st.divider()
    # Stats Section
    completed_count = len(df[df["Status"] == "Completed"])
    st.metric("Syllabus Completion", f"{(completed_count/60)*100:.1f}%" if not df.empty else "0%")

# --- ROADMAP PAGE ---
elif page == "📅 60-Day Roadmap":
    st.title("Tracks your 60-Day Progress")
    if not df.empty:
        # Show tasks sorted by Day
        st.dataframe(df.sort_values("Day")[['Day', 'Subject', 'Topic', 'Status']], use_container_width=True, hide_index=True)

# --- ATTENDANCE PAGE ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Log")
    if not df.empty:
        target = st.selectbox("Select Topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        col1, col2 = st.columns(2)
        with col1: s_t = st.text_input("Start", value="10:00 PM")
        with col2: e_t = st.text_input("End", value="12:00 AM")
        if st.button("🏁 Complete Session"):
            df.at[idx, "Start_Time"], df.at[idx, "End_Time"], df.at[idx, "Status"] = s_t, e_t, "Completed"
            conn.update(worksheet="Tasks", data=df)
            st.success("Logged!"); st.rerun()

# --- DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Resource Linker")
    if not df.empty:
        topic_to_link = st.selectbox("Assign resource to topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == topic_to_link].index[0]
        url = st.text_input("Paste URL (Drive/PDF/Web):", value=str(df.at[idx, "Resources"]) if pd.notna(df.at[idx, "Resources"]) else "")
        if st.button("💾 Save Link"):
            df.at[idx, "Resources"] = url
            conn.update(worksheet="Tasks", data=df)
            st.success("Link saved successfully!")

# --- STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 High-Yield Notes")
    if not df.empty:
        topic_note = st.selectbox("Select Topic:", df['Topic'].unique())
        idx = df[df['Topic'] == topic_note].index[0]
        note_content = st.text_area("Bullet Points:", value=df.at[idx, 'Notes'])
        if st.button("💾 Save Notes"):
            df.at[idx, 'Notes'] = note_content
            conn.update(worksheet="Tasks", data=df)
            st.success("Notes Synced!")

# --- ENGINE ROOM (FULL SYLLABUS) ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    if st.button("🚀 Deploy Official 60-Day Syllabus"):
        full_schedule = [
            {"Day": 1, "Sub": "History", "Top": "Harappa, Vedic, Jainism & Buddhism"},
            {"Day": 2, "Sub": "History", "Top": "Mauryan, Kushan & Gupta Empire"},
            {"Day": 3, "Sub": "History", "Top": "Ancient UK: Kuninda, Yaudheya & Katyuri"},
            {"Day": 4, "Sub": "History", "Top": "Delhi Sultanate: Slave to Lodi"},
            {"Day": 5, "Sub": "History", "Top": "Medieval UK: Parmar & Chand Dynasties"},
            {"Day": 6, "Sub": "History", "Top": "Mughal Empire & Gorkha Rule in UK"},
            {"Day": 7, "Sub": "REVISION", "Top": "Unit 1 Mock: Ancient & Medieval"},
            {"Day": 8, "Sub": "History", "Top": "European Arrival & British Expansion"},
            {"Day": 9, "Sub": "History", "Top": "1857 Revolt & Role of UK Resistance"},
            {"Day": 10, "Sub": "History", "Top": "National Movement: Gandhi Era"},
            {"Day": 11, "Sub": "History", "Top": "UK Public Movements: Coolie Begar & Chipko"},
            {"Day": 12, "Sub": "History", "Top": "Tehri State Movement & Merger"},
            {"Day": 13, "Sub": "History", "Top": "Separate Statehood Movement (1994)"},
            {"Day": 14, "Sub": "REVISION", "Top": "Unit 1 Mock: Modern History & UK"},
            {"Day": 15, "Sub": "Geo", "Top": "World Geo: Lithosphere & Atmosphere"},
            {"Day": 16, "Sub": "Geo", "Top": "World Geo: Hydrosphere & Ocean Currents"},
            {"Day": 17, "Sub": "Geo", "Top": "Indian Geo: Relief, Structure & Climate"},
            {"Day": 18, "Sub": "Geo", "Top": "Indian Geo: Rivers, Soils & Vegetation"},
            {"Day": 19, "Sub": "Geo", "Top": "UK Geography: Glaciers & River Systems"},
            {"Day": 20, "Sub": "Geo", "Top": "UK Resources: Forests & Minerals"},
            {"Day": 21, "Sub": "REVISION", "Top": "Unit 2 Mock: Geography Mastery"},
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble & Rights"},
            {"Day": 23, "Sub": "Polity", "Top": "Parliamentary System: President & PM"},
            {"Day": 24, "Sub": "Polity", "Top": "Judiciary: SC, HC & Local Courts"},
            {"Day": 25, "Sub": "Polity", "Top": "Const. Bodies: Election Comm, CAG, Lokpal"},
            {"Day": 26, "Sub": "Polity", "Top": "UK Administration: Governor & CM"},
            {"Day": 27, "Sub": "Polity", "Top": "Local Governance: Panchayati Raj (UK)"},
            {"Day": 28, "Sub": "REVISION", "Top": "Unit 3 Mock: Polity & UK Admin"},
            {"Day": 29, "Sub": "Economy", "Top": "LPG Reforms & Indian RBI Policy"},
            {"Day": 30, "Sub": "Economy", "Top": "Poverty, Unemployment & HDI"},
            {"Day": 31, "Sub": "Economy", "Top": "Indian Agriculture & Food Security"},
            {"Day": 32, "Sub": "Economy", "Top": "UK Economy: Tourism & MSME Policy"},
            {"Day": 33, "Sub": "Economy", "Top": "UK Budget & Medicinal Herbs Industry"},
            {"Day": 34, "Sub": "Economy", "Top": "Human Development in UK"},
            {"Day": 35, "Sub": "REVISION", "Top": "Unit 4 Mock: Indian & UK Economy"},
            {"Day": 36, "Sub": "Science", "Top": "Physics: Mechanics & Light"},
            {"Day": 37, "Sub": "Science", "Top": "Chemistry: Matter, Acids & Bases"},
            {"Day": 38, "Sub": "Science", "Top": "Biology: Human Systems & Health"},
            {"Day": 39, "Sub": "Science", "Top": "ICT: Computers & E-Governance"},
            {"Day": 40, "Sub": "Science", "Top": "Environment: Ecology & Biodiversity"},
            {"Day": 41, "Sub": "Science", "Top": "Climate Change & UK Disaster Management"},
            {"Day": 42, "Sub": "REVISION", "Top": "Unit 5 Mock: Sci-Tech"},
            {"Day": 43, "Sub": "Culture", "Top": "UK Tribes & Folk Traditions"},
            {"Day": 44, "Sub": "Culture", "Top": "UK Culture: Fairs, Festivals & Dance"},
            {"Day": 45, "Sub": "Culture", "Top": "UK Religious Sites: Panch Kedar/Badri"},
            {"Day": 46, "Sub": "Current", "Top": "National & International Awards/Sports"},
            {"Day": 47, "Sub": "Current", "Top": "UK Current Events & Schemes"},
            {"Day": 48, "Sub": "Current", "Top": "International Orgs: UN, SAARC, BRICS"},
            {"Day": 49, "Sub": "REVISION", "Top": "Unit 6 Mock: Culture & Current"},
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Syllogism & Venn Diagrams"},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Coding & Blood Relations"},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System & Percentage"},
            {"Day": 53, "Sub": "CSAT", "Top": "Data Interpretation: Charts & Tables"},
            {"Day": 54, "Sub": "CSAT", "Top": "English: Comprehension & Vocab"},
            {"Day": 55, "Sub": "CSAT", "Top": "Hindi: Grammar & Tatsam-Tadbhav"},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Mastery Practice"},
            {"Day": 57, "Sub": "MOCK", "Top": "Full Simulation GS Mock 1"},
            {"Day": 58, "Sub": "MOCK", "Top": "Full Simulation CSAT Mock 1"},
            {"Day": 59, "Sub": "MOCK", "Top": "Full Simulation GS Mock 2"},
            {"Day": 60, "Sub": "MOCK", "Top": "Full Simulation CSAT Mock 2"}
        ]
        new_df = pd.DataFrame(full_schedule)
        new_df[["Status", "Notes", "Start_Time", "End_Time", "Resources"]] = ["Planned", "", "10:00 PM", "12:00 AM", ""]
        conn.update(worksheet="Tasks", data=new_df)
        st.success("Full Syllabus Deployed!"); st.rerun()