import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. DATA ENGINE: Column repair & Type Safety
def load_and_repair_data():
    try:
        data = conn.read(worksheet="Tasks", ttl=0)
        expected = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
        
        # Repair column headers
        if "Topic" not in data.columns:
            if len(data.columns) >= len(expected):
                data.columns = expected[:len(data.columns)]
            else:
                return pd.DataFrame(columns=expected)
        
        # TYPE SAFETY: Ensure Resources is string to prevent str.contains crash
        data["Resources"] = data["Resources"].astype(str).replace('nan', '')
        data["Day"] = pd.to_numeric(data["Day"], errors='coerce').fillna(0).astype(int)
        return data
    except Exception:
        return pd.DataFrame(columns=["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"])

df = load_and_repair_data()

# --- SIDEBAR ---
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- CORE FUNCTION: DYNAMIC SHIFT ---
def trigger_break_day(current_day_val):
    mask = df["Day"] >= current_day_val
    df.loc[mask, "Day"] = df.loc[mask, "Day"] + 1
    conn.update(worksheet="Tasks", data=df)
    st.toast(f"Schedule shifted! Current day is now a break.", icon="☕")
    st.rerun()

# --- DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    today_task = df[df["Day"] == days_passed]
    if not today_task.empty:
        row = today_task.iloc[0]
        st.info(f"🚩 **Day {days_passed} Duty**")
        st.header(f"{row['Subject']}: {row['Topic']}")
        
        # Display multiple resources as buttons
        res_str = str(row.get('Resources', ""))
        links = [l.strip() for l in res_str.split(",") if l.strip().startswith("http")]
        if links:
            st.write("### 📖 Books & References")
            cols = st.columns(len(links))
            for i, link in enumerate(links):
                cols[i].link_button(f"Book {i+1}", link, use_container_width=True)
    else:
        st.success("Target complete or Engine Room needs Deployment.")

    with st.expander("🚨 Emergency Schedule Shift"):
        if st.button("☕ Take a Break Today"):
            trigger_break_day(days_passed)

# --- ENGINE ROOM: 100% COMPLETE GRANULAR SYLLABUS ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ System Core")
    if st.button("🚀 DEPLOY FULL SYLLABUS (60 DAYS)"):
        full_curriculum = [
            # UNIT 1: HISTORY (India & Uttarakhand)
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Trade, Religion. Vedic: Rigvedic Society vs Later Vedic transitions."},
            {"Day": 2, "Sub": "History", "Top": "16 Mahajanapadas & Rise of Magadh. Jainism & Buddhism: Councils, Philosophy, Patronage."},
            {"Day": 3, "Sub": "History", "Top": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas (Kanishka) & Satvahanas."},
            {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda Coins, Yaudheya, Katyuri Admin & Jageshwar/Adi-Badri temples."},
            {"Day": 5, "Sub": "History", "Top": "Guptas: Golden Age Admin, Literature (Kalidasa), Science. Harsha & South Indian Dynasties."},
            {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave, Khilji Market Reforms, Tughlaq Admin, Lodi. Bhakti & Sufi Movements."},
            {"Day": 7, "Sub": "REVISION", "Top": "Unit 1 Mock: Ancient & Medieval Comprehensive Analysis."},
            {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand (Kumaon) & Parmar (Garhwal) Dynasties. Gorkha Rule (1790-1815)."},
            {"Day": 9, "Sub": "History", "Top": "Mughals: Mansabdari, Art, Admin. Modern: European Arrival & Battles of Plassey/Buxar."},
            {"Day": 10, "Sub": "History", "Top": "1857 Revolt: UK's Role. Socio-Religious Reforms: Brahmo, Arya Samaj, Ramakrishna Mission."},
            {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Sugauli Treaty, British Kumaon/Garhwal Admin, Coolie Begar & Dola Palki."},
            {"Day": 12, "Sub": "History", "Top": "Freedom Struggle: Gandhi Era, Revolutionary Movements, Cabinet Mission & Independence."},
            {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri Merger (1949), 1994 Muzaffarnagar Kand, Formation 2000."},
            {"Day": 14, "Sub": "REVISION", "Top": "Unit 1 Mock: Modern History & UK Statehood Mastery."},

            # UNIT 2: GEOGRAPHY
            {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Lithosphere: Rocks & Volcanoes. Atmosphere: Layers, Winds, Pressure belts."},
            {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents (Gulf/Kuroshio), Salinity. World Maps."},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon Mechanism & Seasons."},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soils, Vegetation & Wildlife."},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga/Yamuna/Kali). Climate & Rainfall patterns."},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "Resources: UK Forest Policy, National Parks, Minerals & UK Demographics (2011)."},
            {"Day": 21, "Sub": "REVISION", "Top": "Unit 2 Mock: World, India & UK Geography."},

            # UNIT 3: POLITY & GOVERNANCE
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Rights, Duties, DPSP. Important Amendments (42, 44, 73, 74, 101)."},
            {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, LS/RS Procedures. Judiciary: SC/HC & Judicial Activism (PIL)."},
            {"Day": 24, "Sub": "Polity", "Top": "Federalism: Centre-State Relations. Constitutional Bodies: Election Comm, CAG, UPSC."},
            {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly, Secretariat & District Admin."},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: UK Panchayati Raj Act. RTI, Lokpal & Citizen Charters in UK."},
            {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Human Rights, Education, Health & Welfare Schemes (State & Central)."},
            {"Day": 28, "Sub": "REVISION", "Top": "Unit 3 Mock: Indian Polity & UK Governance."},

            # UNIT 4: ECONOMY
            {"Day": 29, "Sub": "Economy", "Top": "Indian Economy Features, NITI Aayog. LPG Reforms 1991 & GST."},
            {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI (Monetary Policy), SEBI, NABARD. Poverty & Unemployment (MNREGA)."},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budgeting Process, Finance Commission. WTO, IMF & World Bank."},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism Policy & Pilgrimage (Char Dham)."},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy, Medicinal Herbs & Forest Produce."},
            {"Day": 34, "Sub": "Economy", "Top": "Sustainable Development Goals (SDG) & Human Development Index (HDI) ranking."},
            {"Day": 35, "Sub": "REVISION", "Top": "Unit 4 Mock: Economy (India & UK)."},

            # UNIT 5: SCIENCE & TECH / ENVIRONMENT
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Electricity. Chemistry: Matter, Acids/Bases, Carbon Compounds."},
            {"Day": 37, "Sub": "Science", "Top": "Biology: Cell Structure, Human Systems, Genetics, Health & Nutrition."},
            {"Day": 38, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security, Artificial Intelligence."},
            {"Day": 39, "Sub": "Science", "Top": "Space & Defense: ISRO Missions, Nuclear Power, DRDO Programs."},
            {"Day": 40, "Sub": "Environment", "Top": "Ecology: Biodiversity, National Parks, Wetlands (Ramsar). Valley of Flowers."},
            {"Day": 41, "Sub": "Science (UK)", "Top": "Disaster Mgmt: Earthquakes, Landslides, SDMA Structure, Cloudbursts."},
            {"Day": 42, "Sub": "REVISION", "Top": "Unit 5 Mock: Science, Tech & Environment."},

            # UNIT 6: UK CULTURE & CURRENT AFFAIRS
            {"Day": 43, "Sub": "Culture (UK)", "Top": "Tribes: Bhotia, Tharu, Jaunsari, Buxa, Raji. Folk Arts, Music & Instruments."},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs: Nanda Devi, Kumbh. Religious Sites: Panch Kedar, Panch Badri, Temples."},
            {"Day": 45, "Sub": "Current", "Top": "National: Awards, Sports, Summits, Appointments. Indices & Reports."},
            {"Day": 46, "Sub": "Current", "Top": "International: UN, BRICS, G20, G7. World Conflicts & Diplomatic Relations."},
            {"Day": 47, "Sub": "Current (UK)", "Top": "UK State Current: Budget Highlights, New Schemes, CM Dashboard updates."},
            {"Day": 48, "Sub": "Current", "Top": "Sports: Olympics, Cricket. Famous UK Personalities & Recent Book Awards."},
            {"Day": 49, "Sub": "REVISION", "Top": "Unit 6 Mock: Culture & Year-long Current Affairs."},

            # PAPER II: CSAT
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations, Direction Sense."},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams, Analogies."},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio, Percentage, Average."},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Profit/Loss, Time & Work, Data Interpretation (DI)."},
            {"Day": 54, "Sub": "CSAT", "Top": "Comprehension: English Passage Skills & Vocabulary."},
            {"Day": 55, "Sub": "CSAT", "Top": "General Hindi: Grammar, Tatsam-Tadbhav, Synonyms (Varna-Vichyar)."},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Full Mock: Paper II Simulator."},

            # FINAL MARATHON
            {"Day": 57, "Sub": "MOCK", "Top": "GS Full Mock 1: Entire Paper I Simulation."},
            {"Day": 58, "Sub": "MOCK", "Top": "CSAT Full Mock 2: Entire Paper II Simulation."},
            {"Day": 59, "Sub": "MOCK", "Top": "GS Full Mock 3: All-India Test Series Level Paper."},
            {"Day": 60, "Sub": "MOCK", "Top": "Final Simulation: Combined Paper I & II Strategy."}
        ]
        new_df = pd.DataFrame(full_curriculum)
        for col in ["Status", "Notes", "Start_Time", "End_Time", "Resources"]:
            new_df[col] = ""
        new_df["Status"] = "Planned"
        conn.update(worksheet="Tasks", data=new_df)
        st.success("100% Granular Syllabus Deployed!"); st.rerun()

# --- DIGITAL LIBRARY (Multiple Links Fix) ---
elif page == "📚 Digital Library":
    st.title("📚 Library Manager")
    if not df.empty:
        target = st.selectbox("Select Topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        
        current_links = str(df.at[idx, "Resources"])
        new_link = st.text_input("Paste URL:")
        if st.button("Add to Topic"):
            if new_link.startswith("http"):
                # Append link logic
                updated = f"{current_links}, {new_link}" if current_links and current_links != "" else new_link
                df.at[idx, "Resources"] = updated
                conn.update(worksheet="Tasks", data=df)
                st.success("Link Saved!"); st.rerun()
        
        st.divider()
        st.subheader("Inventory")
        # Crash protection for search
        inv_df = df[df['Resources'].astype(str).str.contains("http", na=False)][['Topic', 'Resources']]
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

# --- STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 High-Yield Notes")
    if not df.empty:
        target = st.selectbox("Select Topic:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        notes = st.text_area("Bullet Points:", value=df.at[idx, 'Notes'], height=300)
        if st.button("Save Notes"):
            df.at[idx, 'Notes'] = notes
            conn.update(worksheet="Tasks", data=df); st.success("Notes Synced!")

# --- ATTENDANCE LOG ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Study Session Log")
    if not df.empty:
        target = st.selectbox("Log Session:", df['Topic'].tolist())
        idx = df[df['Topic'] == target].index[0]
        c1, c2 = st.columns(2)
        s_t, e_t = c1.text_input("Start", "10:00 PM"), c2.text_input("End", "12:00 AM")
        if st.button("Complete Day"):
            df.at[idx, "Status"], df.at[idx, "Start_Time"], df.at[idx, "End_Time"] = "Completed", s_t, e_t
            conn.update(worksheet="Tasks", data=df); st.success("Logged!"); st.rerun()

# --- ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 60-Day Roadmap")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)