import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. DATA ENGINE: Robust Loading & Column Repair
def load_and_repair_data():
    try:
        data = conn.read(worksheet="Tasks", ttl=0)
        
        # DEFINITIVE HEADER FIX: If 'Topic' is missing, re-map based on position
        expected = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
        
        if "Topic" not in data.columns:
            # Check if headers are merged or just named differently
            if len(data.columns) >= len(expected):
                data.columns = expected[:len(data.columns)]
            else:
                # If the sheet is empty or corrupted, create a fresh frame
                return pd.DataFrame(columns=expected)
        
        # Clean data: Remove empty rows and ensure 'Day' is a number
        data = data.dropna(subset=['Day'])
        data["Day"] = pd.to_numeric(data["Day"], errors='coerce').fillna(0).astype(int)
        return data
    except Exception:
        return pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

df = load_and_repair_data()

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- CORE FUNCTION: DYNAMIC SHIFT (Break Day) ---
def trigger_break_day(current_day_val):
    mask = df["Day"] >= current_day_val
    df.loc[mask, "Day"] = df.loc[mask, "Day"] + 1
    conn.update(worksheet="Tasks", data=df)
    st.toast(f"Schedule shifted! Day {current_day_val} is now a Break Day.", icon="☕")
    st.rerun()

# --- PAGE: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    col1, col2 = st.columns([2, 1])
    with col1:
        today_task = df[df["Day"] == days_passed]
        if not today_task.empty:
            row = today_task.iloc[0]
            st.info(f"🚩 **Current Target: Day {days_passed}**")
            st.header(f"{row['Subject']}: {row['Topic']}")
            
            res_url = str(row.get('Resources', ""))
            if res_url.startswith("http"):
                st.link_button("📖 Open Resource Link", res_url, type="primary")
            else:
                st.warning("⚠️ No resource linked for this topic.")
        else:
            st.success("No task scheduled. Use 'Engine Room' to deploy syllabus.")

    with col2:
        st.write("### 🚨 Schedule Shift")
        if st.button("☕ Take a Break Today"):
            trigger_break_day(days_passed)

# --- PAGE: ENGINE ROOM (COMPLETE GRANULAR SYLLABUS) ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ System Core")
    if st.button("🚀 DEPLOY FULL GRANULAR 60-DAY SYLLABUS"):
        # Mapping micro-topics from the 2024 PDF Syllabus
        full_curriculum = [
            # UNIT 1: History, Culture & National Movement
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Trade & Religion | Vedic: Rigvedic vs Later Society"},
            {"Day": 2, "Sub": "History", "Top": "Mahajanapadas, Jainism, Buddhism | Mauryan Admin & Ashoka's Dhamma"},
            {"Day": 3, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda Coins, Katyuri Admin & Kalsi Ashoka Inscription"},
            {"Day": 4, "Sub": "History", "Top": "Gupta Empire: Science & Art | Delhi Sultanate: Admin, Khilji & Tughlaq"},
            {"Day": 5, "Sub": "History (UK)", "Top": "Medieval UK: Chand (Kumaon) & Parmar (Garhwal) Dynasties | Gorkha Invasion"},
            {"Day": 6, "Sub": "History", "Top": "Mughal Empire: Mansabdari System | Maratha Rise & Sikh Movement"},
            {"Day": 7, "Sub": "REVISION", "Top": "Mock 1: Ancient & Medieval Comprehensive"},
            {"Day": 8, "Sub": "History", "Top": "British Expansion (1758-1857) | Economic Policy & Land Revenue"},
            {"Day": 9, "Sub": "History", "Top": "1857 Revolt: UK's Role & National Impact | Socio-Religious Reforms"},
            {"Day": 10, "Sub": "History", "Top": "Gandhi Era: Non-Cooperation, Civil Disobedience & Quit India"},
            {"Day": 11, "Sub": "History (UK)", "Top": "UK Resistance: Coolie Begar, Dola-Palki & Salt Satyagraha"},
            {"Day": 12, "Sub": "History (UK)", "Top": "Tehri State Movement | Sridev Suman | Merger with India 1949"},
            {"Day": 13, "Sub": "History (UK)", "Top": "Separate State Movement: 1994 Muzaffarnagar Kand | Formation 2000"},
            {"Day": 14, "Sub": "REVISION", "Top": "Mock 2: Modern India & UK Statehood"},
            # UNIT 2: Geography
            {"Day": 15, "Sub": "Geo (World)", "Top": "Lithosphere: Earth's Structure & Plate Tectonics | Atmosphere Layers"},
            {"Day": 16, "Sub": "Geo (India)", "Top": "Relief & Structure | Himalayas, Plains & Peninsula | Climate Zones"},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Drainage Systems: Himalayan vs Peninsular Rivers | Soils & Vegetation"},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Agriculture: Crops & Productivity | Mineral Resources & Industries"},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Geography: Glaciers, River Basins & Natural Disasters (SDMA)"},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "UK Forests, Minerals & Demographics | Tourism & Pilgrimage"},
            {"Day": 21, "Sub": "REVISION", "Top": "Mock 3: World, India & UK Geography"},
            # UNIT 3: Polity
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Fundamental Rights, DPSP & Duties"},
            {"Day": 23, "Sub": "Polity", "Top": "Parliamentary System: President, PM & Parliamentary Committees"},
            {"Day": 24, "Sub": "Polity", "Top": "Judiciary: Supreme Court, High Courts & Judicial Activism (PIL)"},
            {"Day": 25, "Sub": "Polity", "Top": "Constitutional Bodies: Election Commission, CAG & Lokpal"},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "UK Administration: Governor, CM, Council & State Secretariat"},
            {"Day": 27, "Sub": "Polity (UK)", "Top": "Local Governance: UK Panchayati Raj & Municipalities (73/74 Amendments)"},
            {"Day": 28, "Sub": "REVISION", "Top": "Mock 4: Indian Polity & UK Administration"},
            # UNIT 4: Economy
            {"Day": 29, "Sub": "Economy", "Top": "LPG Reforms (1991) | Monetary Policy & RBI Functions"},
            {"Day": 30, "Sub": "Economy", "Top": "Poverty, Unemployment & Human Development Indicators (HDI)"},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budget, GST & Finance Commission"},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK MSME Policy, Tourism Economy & Medicinal Herbs Industry"},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "UK State Budget | Employment Trends & Rural Dev Schemes"},
            {"Day": 34, "Sub": "Economy (UK)", "Top": "Education & Health Indicators in Uttarakhand | Food Security"},
            {"Day": 35, "Sub": "REVISION", "Top": "Mock 5: Economic Development India & UK"},
            # UNIT 5: General Science & Environment
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Electricity & Nuclear Energy"},
            {"Day": 37, "Sub": "Science", "Top": "Chemistry: Acids, Bases, Polymers & Daily Life Application"},
            {"Day": 38, "Sub": "Science", "Top": "Biology: Human Systems, Diseases, Health & Nutrition"},
            {"Day": 39, "Sub": "Science", "Top": "ICT: E-Governance, Cyber Security & Cloud Computing"},
            {"Day": 40, "Sub": "Science", "Top": "Environmental Ecology: Biodiversity, National Parks & Sanctuaries"},
            {"Day": 41, "Sub": "Science", "Top": "Climate Change: IPCC, IUCN & UK Disaster Management Structure"},
            {"Day": 42, "Sub": "REVISION", "Top": "Mock 6: Science, Tech & Environment"},
            # UNIT 6: UK Culture & Current Affairs
            {"Day": 43, "Sub": "Culture (UK)", "Top": "Tribes of UK: Bhotia, Tharu, Jaunsari, Buxa & Raji"},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Folk Arts: Jhora, Chhapeli, Pandav Nritya | Fairs & Festivals"},
            {"Day": 45, "Sub": "Culture (UK)", "Top": "Religious Heritage: Panch Kedar, Panch Badri & Temples"},
            {"Day": 46, "Sub": "Current", "Top": "International: UN, SAARC, BRICS & G20 Events"},
            {"Day": 47, "Sub": "Current", "Top": "National: Govt Schemes, Awards & Sports 2024-25"},
            {"Day": 48, "Sub": "Current", "Top": "UK Current: State Schemes, Awards & Recent Legislation"},
            {"Day": 49, "Sub": "REVISION", "Top": "Mock 7: Culture & Current Affairs Full"},
            # PAPER II: Aptitude (CSAT)
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Syllogisms, Venn Diagrams & Analogies"},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations & Directions"},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio & Percentage"},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Average, Time & Work, Profit & Loss"},
            {"Day": 54, "Sub": "CSAT", "Top": "Data Interpretation: Charts, Tables & Graphs Mastery"},
            {"Day": 55, "Sub": "CSAT", "Top": "General Hindi: Grammar, Vocabulary & Comprehension"},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Full Mock: Paper II Qualifying Test"},
            # FINAL MARATHON
            {"Day": 57, "Sub": "MOCK", "Top": "Full GS Mock Test 1 (Paper I Simulation)"},
            {"Day": 58, "Sub": "MOCK", "Top": "Full CSAT Mock Test 1 (Paper II Simulation)"},
            {"Day": 59, "Sub": "MOCK", "Top": "Full GS Mock Test 2 (Paper I Simulation)"},
            {"Day": 60, "Sub": "MOCK", "Top": "Final UKPSC Simulator: Papers I & II Combined"}
        ]
        new_df = pd.DataFrame(full_curriculum)
        new_df[["Status", "Notes", "Start_Time", "End_Time", "Resources"]] = ["Planned", "", "10:00 PM", "12:00 AM", ""]
        conn.update(worksheet="Tasks", data=new_df)
        st.success("100% Granular Syllabus Deployed! Refresh Dashboard."); st.rerun()

# --- OTHER PAGES: ROADMAP, LOG, LIBRARY, NOTES (All with KeyError protection) ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 Progress Tracker")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)

elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Log")
    if not df.empty:
        topic_list = df['Topic'].tolist()
        target = st.selectbox("Log Session For:", topic_list)
        idx = df[df['Topic'] == target].index[0]
        c1, c2 = st.columns(2)
        s_t = c1.text_input("Start", "10:00 PM")
        e_t = c2.text_input("End", "12:00 AM")
        if st.button("Complete Day"):
            df.at[idx, "Status"], df.at[idx, "Start_Time"], df.at[idx, "End_Time"] = "Completed", s_t, e_t
            conn.update(worksheet="Tasks", data=df)
            st.success("Session Logged!"); st.rerun()

elif page == "📚 Digital Library":
    st.title("📚 Resource Linker")
    if not df.empty:
        target = st.selectbox("Assign PDF/Link to:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        url = st.text_input("URL:", value=str(df.at[idx, "Resources"]))
        if st.button("Save Link"):
            df.at[idx, "Resources"] = url
            conn.update(worksheet="Tasks", data=df); st.success("Linked!")

elif page == "📝 Study Notes":
    st.title("📝 High-Yield Notes")
    if not df.empty:
        target = st.selectbox("Select Topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        notes = st.text_area("Bullet Points:", value=df.at[idx, 'Notes'])
        if st.button("Save Notes"):
            df.at[idx, 'Notes'] = notes
            conn.update(worksheet="Tasks", data=df); st.success("Notes Synced!")