import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

def load_and_repair_data():
    try:
        data = conn.read(worksheet="Tasks", ttl=0)
        expected = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
        if "Topic" not in data.columns:
            if len(data.columns) >= len(expected):
                data.columns = expected[:len(data.columns)]
            else:
                return pd.DataFrame(columns=expected)
        data = data.dropna(subset=['Day'])
        data["Day"] = pd.to_numeric(data["Day"], errors='coerce').fillna(0).astype(int)
        return data
    except Exception:
        return pd.DataFrame(columns=expected)

df = load_and_repair_data()

# --- SIDEBAR ---
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- CORE FUNCTION: DYNAMIC SHIFT ---
def trigger_break_day(current_day_val):
    mask = df["Day"] >= current_day_val
    df.loc[mask, "Day"] = df.loc[mask, "Day"] + 1
    conn.update(worksheet="Tasks", data=df)
    st.toast(f"Schedule shifted!", icon="☕")
    st.rerun()

# --- DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    today_task = df[df["Day"] == days_passed]
    if not today_task.empty:
        row = today_task.iloc[0]
        st.info(f"🚩 **Day {days_passed} Target**")
        st.header(f"{row['Subject']}: {row['Topic']}")
        
        # Multi-link view
        res_str = str(row.get('Resources', ""))
        links = [l.strip() for l in res_str.split(",") if l.strip().startswith("http")]
        if links:
            st.write("### 📖 Books & Resources")
            cols = st.columns(len(links))
            for i, link in enumerate(links):
                cols[i].link_button(f"Resource {i+1}", link, use_container_width=True)
    else:
        st.success("Welcome! Go to Engine Room to deploy the full syllabus.")

# --- ENGINE ROOM: THE FULL DETAILED SYLLABUS ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ System Core")
    if st.button("🚀 DEPLOY FULL DETAILED 60-DAY SYLLABUS"):
        # COMPLETELY EXPANDED SYLLABUS MAPPING
        full_curriculum = [
            # WEEK 1: Ancient & Medieval (India & UK)
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Seals, Trade. Vedic: Early & Later, Rigvedic Rivers, Sabha/Samiti."},
            {"Day": 2, "Sub": "History", "Top": "Mahajanapadas (16), Magadh Rise. Jainism/Buddhism: Councils, Philosophy, Patronage."},
            {"Day": 3, "Sub": "History", "Top": "Mauryas: Chandragupta, Ashoka's Dhamma, Admin. Kushanas: Kanishka & Art Schools."},
            {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kunindas (Amoghbhuti coins), Yaudheya, Katyuri Admin & Jageshwar Architecture."},
            {"Day": 5, "Sub": "History", "Top": "Gupta: Admin, Golden Age Literature (Kalidasa), Science (Aryabhatta). Harshavardhana."},
            {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave, Khilji (Market reforms), Tughlaq (Admin), Lodi. Indo-Islamic Art."},
            {"Day": 7, "Sub": "REVISION", "Top": "Unit 1 Mock: Ancient & Medieval Comprehensive Revision."},
            
            # WEEK 2: Medieval UK & Modern India
            {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand Dynasty (Kumaon), Parmar (Garhwal). Gorkha Rule & Invasion (1790-1815)."},
            {"Day": 9, "Sub": "History", "Top": "Modern: European Arrival, Battle of Plassey/Buxar. Land Revenue: Zamindari, Ryotwari, Mahalwari."},
            {"Day": 10, "Sub": "History", "Top": "1857 Revolt: Causes, Centres & Leaders. Socio-Religious: Brahmo Samaj, Arya Samaj, Aligarh Mov."},
            {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Treaty of Sugauli, British Admin in UK, Coolie Begar & Dola Palki Movement."},
            {"Day": 12, "Sub": "History", "Top": "National Mov: Gandhi Era (Non-Cooperation, Civil Disobedience, Quit India). Cabinet Mission."},
            {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri State Merger (1949), 1994 Muzaffarnagar Kand, Formation of UK 2000."},
            {"Day": 14, "Sub": "REVISION", "Top": "Unit 1 Mock: Modern History & UK Statehood Mastery."},

            # WEEK 3: Geography (Unit 2)
            {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Lithosphere: Earth's Structure, Rocks. Atmosphere: Layers, Winds, Pressure."},
            {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents (Gulf, Kuroshio), Tides, Salinity."},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsular Plateau. Climate: Monsoon Mechanism, Seasons."},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soil Types, Natural Vegetation & Forests."},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali). Climate & Rainfall in UK."},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "UK Resources: Forest Policy, Minerals, Wildlife Sanctuaries & National Parks (Jim Corbett)."},
            {"Day": 21, "Sub": "REVISION", "Top": "Unit 2 Mock: World, India & UK Geography."},

            # WEEK 4: Polity (Unit 3)
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Features. Fundamental Rights, DPSP & Duties. Amendments (42/44)."},
            {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, LS/RS, Committees. Judiciary: SC/HC, Writ Jurisdiction."},
            {"Day": 24, "Sub": "Polity", "Top": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism: Centre-State Relations."},
            {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly. Secretariat, District Admin."},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: 73rd/74th Amendments. UK Panchayati Raj Act & RTI in UK."},
            {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Welfare Schemes, Human Rights, Citizen's Charter."},
            {"Day": 28, "Sub": "REVISION", "Top": "Unit 3 Mock: Indian Polity & UK Governance."},

            # WEEK 5: Economy (Unit 4)
            {"Day": 29, "Sub": "Economy", "Top": "Indian Economy: Features, Planning History (NITI Aayog). LPG Reforms 1991."},
            {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI (Monetary Policy), SEBI, NABARD. Stock Markets."},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budgeting, GST, Finance Commission. Poverty & Unemployment (MNREGA)."},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism Policy & Pilgrimage Impact."},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy, Medicinal Herbs & Forest Resources."},
            {"Day": 34, "Sub": "Economy", "Top": "Sustainable Dev Goals (SDG), Human Development Index (HDI), WTO & IMF."},
            {"Day": 35, "Sub": "REVISION", "Top": "Unit 4 Mock: Economy (India & UK)."},

            # WEEK 6: Science & Tech (Unit 5)
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Magnetism, Nuclear Energy. Daily Life Applications."},
            {"Day": 37, "Sub": "Science", "Top": "Chemistry: Matter, Polymers, Carbon & Compounds, Acids/Bases."},
            {"Day": 38, "Sub": "Science", "Top": "Biology: Cell, Genetics, Human Systems (Circulation, Digestion), Diseases."},
            {"Day": 39, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security, Cloud Computing. Space Tech (ISRO)."},
            {"Day": 40, "Sub": "Science", "Top": "Environment: Ecology, Food Chain, Biodiversity Hotspots (Valley of Flowers)."},
            {"Day": 41, "Sub": "Science (UK)", "Top": "Disaster Mgmt: UK Vulnerability (Earthquakes/Landslides), SDMA Structure."},
            {"Day": 42, "Sub": "REVISION", "Top": "Unit 5 Mock: General Science & Tech."},

            # WEEK 7: Culture & Current Affairs (Unit 6)
            {"Day": 43, "Sub": "Culture (UK)", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari, Buxa, Raji. Folk Art, Music, Dance."},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs & Festivals: Nanda Devi, Kumbh, Magh Mela. Religious Sites: Panch Kedar/Badri."},
            {"Day": 45, "Sub": "Current", "Top": "National Current Affairs: Awards, Sports, Summits, Appointments."},
            {"Day": 46, "Sub": "Current", "Top": "International Affairs: UN, BRICS, G20. World Reports/Indices."},
            {"Day": 47, "Sub": "Current (UK)", "Top": "UK State Current: Budget, CM Dashboards, New Welfare Schemes."},
            {"Day": 48, "Sub": "Current", "Top": "Sports: Olympics, Cricket, Commonwealth. Famous Personalities."},
            {"Day": 49, "Sub": "REVISION", "Top": "Unit 6 Mock: Culture & Year-long Current Affairs."},

            # WEEK 8: CSAT (Paper II)
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations, Direction Sense."},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams, Seating Arrangement."},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio, Percentage, Average."},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Profit/Loss, Time & Work, Data Interpretation (DI)."},
            {"Day": 54, "Sub": "CSAT", "Top": "Comprehension: English Passage Reading & Vocabulary."},
            {"Day": 55, "Sub": "CSAT", "Top": "General Hindi: Grammar, Tatsam-Tadbhav, Antonyms/Synonyms."},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Full Mock: Paper II Simulation."},

            # FINAL WEEK: MOCK MARATHON
            {"Day": 57, "Sub": "MOCK", "Top": "GS Full Mock 1: Entire Paper I Simulation."},
            {"Day": 58, "Sub": "MOCK", "Top": "CSAT Full Mock 2: Entire Paper II Simulation."},
            {"Day": 59, "Sub": "MOCK", "Top": "GS Full Mock 3: Revision of Weak Topics."},
            {"Day": 60, "Sub": "MOCK", "Top": "FINAL SIMULATION: Combined Paper I & II (D-Day Prep)."}
        ]
        new_df = pd.DataFrame(full_curriculum)
        new_df[["Status", "Notes", "Start_Time", "End_Time", "Resources"]] = ["Planned", "", "10:00 PM", "12:00 AM", ""]
        conn.update(worksheet="Tasks", data=new_df)
        st.success("100% Granular Syllabus Deployed!"); st.rerun()

# --- OTHER PAGES: LIBRARY, NOTES, ATTENDANCE (Keep same logic) ---
elif page == "📚 Digital Library":
    st.title("📚 Library Manager")
    target = st.selectbox("Select Topic:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    current_links = str(df.at[idx, "Resources"])
    new_link = st.text_input("Paste new Link:")
    if st.button("Add Link"):
        if new_link.startswith("http"):
            updated = f"{current_links}, {new_link}" if current_links and current_links != "nan" else new_link
            df.at[idx, "Resources"] = updated
            conn.update(worksheet="Tasks", data=df); st.success("Added!"); st.rerun()
    st.divider()
    st.subheader("Inventory")
    st.dataframe(df[df['Resources'].str.contains("http", na=False)][['Topic', 'Resources']], use_container_width=True)

elif page == "📝 Study Notes":
    st.title("📝 High-Yield Notes")
    target = st.selectbox("Topic:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    notes = st.text_area("Notes:", value=df.at[idx, 'Notes'], height=300)
    if st.button("Save"):
        df.at[idx, 'Notes'] = notes
        conn.update(worksheet="Tasks", data=df); st.success("Synced!")

elif page == "⏱️ Attendance Log":
    st.title("⏱️ Log")
    target = st.selectbox("Target:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    c1, c2 = st.columns(2)
    s_t, e_t = c1.text_input("Start", "10:00 PM"), c2.text_input("End", "12:00 AM")
    if st.button("Complete"):
        df.at[idx, "Status"], df.at[idx, "Start_Time"], df.at[idx, "End_Time"] = "Completed", s_t, e_t
        conn.update(worksheet="Tasks", data=df); st.success("Logged!"); st.rerun()