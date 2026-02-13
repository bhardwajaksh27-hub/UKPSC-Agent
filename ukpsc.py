import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuration & Connection
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🛡️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Loading & Self-Healing
try:
    df = conn.read(worksheet="Tasks", ttl=0)
    required_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    for col in required_cols:
        if col not in df.columns: df[col] = ""
    df["Day"] = pd.to_numeric(df["Day"], errors='coerce')
except:
    df = pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- BREAK DAY LOGIC ---
def trigger_break_day(current_day_val):
    mask = df["Day"] >= current_day_val
    df.loc[mask, "Day"] = df.loc[mask, "Day"] + 1
    conn.update(worksheet="Tasks", data=df)
    st.toast(f"Plan shifted! Day {current_day_val} is now a Break Day.", icon="☕")
    st.rerun()

# --- DASHBOARD ---
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
            if today_task.iloc[0]['Resources']:
                st.link_button("📖 Open PDF", today_task.iloc[0]['Resources'])
        else:
            st.success("You are ahead of schedule or have completed the 60 days!")

    with c2:
        st.write("### 🚨 Schedule Adjustment")
        if st.button("☕ Take a Break Today"):
            trigger_break_day(days_passed)

# --- ENGINE ROOM (FULL 60-DAY SYLLABUS DATA) ---
elif page == "⚙️ Settings" or page == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    if st.button("🚀 Deploy COMPLETE 60-Day Syllabus"):
        # COMPLETE SYLLABUS MAPPING (Unit 1 to Unit 6 + CSAT)
        full_schedule = [
            # WEEK 1: Ancient & Medieval (India & UK)
            {"Day": 1, "Sub": "History", "Top": "Harappa, Vedic, Jainism & Buddhism"},
            {"Day": 2, "Sub": "History", "Top": "Mauryan, Kushan & Gupta Empire (Admin/Culture)"},
            {"Day": 3, "Sub": "History", "Top": "Ancient UK: Kuninda, Yaudheya & Katyuri Dynasties"},
            {"Day": 4, "Sub": "History", "Top": "Delhi Sultanate: Slave, Khilji, Tughlaq & Lodi"},
            {"Day": 5, "Sub": "History", "Top": "Medieval UK: Parmar Dynasty (Garhwal) & Chand (Kumaon)"},
            {"Day": 6, "Sub": "History", "Top": "Mughal Empire & Gorkha Rule in Uttarakhand"},
            {"Day": 7, "Sub": "REVISION", "Top": "Unit 1 Mock: Ancient & Medieval Mastery"},
            # WEEK 2: Modern History & UK Statehood
            {"Day": 8, "Sub": "History", "Top": "European Arrival & British Expansion (1758-1857)"},
            {"Day": 9, "Sub": "History", "Top": "1857 Revolt & Role of Uttarakhand in Early Resistance"},
            {"Day": 10, "Sub": "History", "Top": "National Movement: Gandhi Era (India-wide)"},
            {"Day": 11, "Sub": "History", "Top": "UK Public Movements: Coolie Begar & Chipko"},
            {"Day": 12, "Sub": "History", "Top": "Tehri State Movement & Merger with India"},
            {"Day": 13, "Sub": "History", "Top": "Separate Statehood Movement (1994 Muzaffarnagar)"},
            {"Day": 14, "Sub": "REVISION", "Top": "Unit 1 Mock: Modern History & UK Statehood"},
            # WEEK 3: Geography (Unit 2)
            {"Day": 15, "Sub": "Geo", "Top": "World Geo: Solar System, Rocks & Atmosphere Layers"},
            {"Day": 16, "Sub": "Geo", "Top": "World Geo: Hydrosphere & Ocean Currents"},
            {"Day": 17, "Sub": "Geo", "Top": "Indian Geo: Relief, Structure & Climate (Monsoon)"},
            {"Day": 18, "Sub": "Geo", "Top": "Indian Geo: Rivers, Soils & Natural Vegetation"},
            {"Day": 19, "Sub": "Geo", "Top": "UK Geography: Glaciers, Peaks & River Systems"},
            {"Day": 20, "Sub": "Geo", "Top": "UK Resources: Forests, Minerals & Population"},
            {"Day": 21, "Sub": "REVISION", "Top": "Unit 2 Mock: World, India & UK Geography"},
            # WEEK 4: Polity (Unit 3)
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Fundamental Rights & Duties"},
            {"Day": 23, "Sub": "Polity", "Top": "Parliamentary System: President, PM & Parliament"},
            {"Day": 24, "Sub": "Polity", "Top": "Judiciary: SC, HC & Local Courts"},
            {"Day": 25, "Sub": "Polity", "Top": "Constitutional Bodies: Election Comm, CAG, Lokpal"},
            {"Day": 26, "Sub": "Polity", "Top": "UK Administration: Governor, CM & Secretariat"},
            {"Day": 27, "Sub": "Polity", "Top": "Local Governance: 73/74 Amendments & UK Panchayati Raj"},
            {"Day": 28, "Sub": "REVISION", "Top": "Unit 3 Mock: Indian Polity & UK Admin"},
            # WEEK 5: Economy (Unit 4)
            {"Day": 29, "Sub": "Economy", "Top": "Economic Reforms: LPG, FDI & Indian RBI Policy"},
            {"Day": 30, "Sub": "Economy", "Top": "Socio-Economic: Poverty, Unemployment & HDI"},
            {"Day": 31, "Sub": "Economy", "Top": "Indian Agriculture: Green Rev & Food Security"},
            {"Day": 32, "Sub": "Economy", "Top": "UK Economy: Per Capita Income & Tourism Policy"},
            {"Day": 33, "Sub": "Economy", "Top": "UK Budget, MSME & Medicinal Herbs Industry"},
            {"Day": 34, "Sub": "Economy", "Top": "Human Development & Employment in UK"},
            {"Day": 35, "Sub": "REVISION", "Top": "Unit 4 Mock: Indian & UK Economy"},
            # WEEK 6: Science & Tech (Unit 5)
            {"Day": 36, "Sub": "Science", "Top": "Physics: Mechanics, Light, Sound & Magnetism"},
            {"Day": 37, "Sub": "Science", "Top": "Chemistry: Matter, Acids, Bases & Polymers"},
            {"Day": 38, "Sub": "Science", "Top": "Biology: Human Systems, Health & Vaccines"},
            {"Day": 39, "Sub": "Science", "Top": "ICT: Computers, Cloud Computing & E-Governance"},
            {"Day": 40, "Sub": "Science", "Top": "Environment: Ecology & Biodiversity Conservation"},
            {"Day": 41, "Sub": "Science", "Top": "Climate Change & UK Disaster Management"},
            {"Day": 42, "Sub": "REVISION", "Top": "Unit 5 Mock: Sci-Tech & Environment"},
            # WEEK 7: Current Affairs & UK Culture (Unit 6)
            {"Day": 43, "Sub": "Culture", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari, Buxa & Raji"},
            {"Day": 44, "Sub": "Culture", "Top": "UK Culture: Folk Music, Dance, Fairs & Festivals"},
            {"Day": 45, "Sub": "Culture", "Top": "Religious Sites: Panch Kedar, Badri & UK Temples"},
            {"Day": 46, "Sub": "Current", "Top": "National/International: Awards, Sports & Reports"},
            {"Day": 47, "Sub": "Current", "Top": "UK Specific Current Events & Govt Schemes"},
            {"Day": 48, "Sub": "Current", "Top": "International Orgs: UN, SAARC, ASEAN, BRICS"},
            {"Day": 49, "Sub": "REVISION", "Top": "Unit 6 Mock: Culture & Current Affairs"},
            # WEEK 8: CSAT (Paper II)
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams & Analogies"},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations & Series"},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio & Percentage"},
            {"Day": 53, "Sub": "CSAT", "Top": "Data Interpretation: Charts, Tables & Graphs"},
            {"Day": 54, "Sub": "CSAT", "Top": "English: Comprehension & Vocabulary"},
            {"Day": 55, "Sub": "CSAT", "Top": "Hindi: Grammar, Tatsam-Tadbhav & Usage"},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Mastery: Paper II Full Practice"},
            # WEEK 9: Final Mock Marathon
            {"Day": 57, "Sub": "MOCK", "Top": "Full Simulation: Paper I (GS) Mock 1"},
            {"Day": 58, "Sub": "MOCK", "Top": "Full Simulation: Paper II (CSAT) Mock 1"},
            {"Day": 59, "Sub": "MOCK", "Top": "Full Simulation: Paper I (GS) Mock 2"},
            {"Day": 60, "Sub": "MOCK", "Top": "Full Simulation: Paper II (CSAT) Mock 2"},
        ]
        new_df = pd.DataFrame(full_schedule)
        new_df[["Status", "Notes", "Start_Time", "End_Time", "Resources"]] = ["Planned", "", "10:00 PM", "12:00 AM", ""]
        conn.update(worksheet="Tasks", data=new_df)
        st.success("Full 60-Day Syllabus Integrated with Break-Day Logic!")