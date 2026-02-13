import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. PERSISTENCE ENGINE: Load & Save Functions
def load_data():
    # ttl=0 ensures we bypass the cache to get real-time data from the sheet
    return conn.read(worksheet="Tasks", ttl=0)

def save_data(data):
    # This pushes the entire dataframe back to your Google Sheet
    conn.update(worksheet="Tasks", data=data)
    st.cache_data.clear() 

df = load_data()

# Ensure critical columns exist in the dataframe
for col in ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]:
    if col not in df.columns:
        df[col] = ""

# 3. Sidebar Navigation
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "⏱️ Attendance Log", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- PAGE: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    today_task = df[pd.to_numeric(df["Day"], errors='coerce') == days_passed]
    
    if not today_task.empty:
        row = today_task.iloc[0]
        st.info(f"🚩 **Day {days_passed} Target**")
        st.header(f"{row['Subject']}: {row['Topic']}")
        
        # Split and display resources as a numbered sub-series
        res_str = str(row['Resources']).replace('nan', '').strip()
        links = [l.strip() for l in res_str.split(",") if l.strip().startswith("http")]
        
        if links:
            st.write("### 📖 Study Resources")
            for i, link in enumerate(links):
                char = chr(97 + i) # a, b, c...
                st.link_button[f"Resource {char}](http://googleusercontent.com/map_location_reference/0)...", link)
        else:
            st.warning("⚠️ No resources linked for today.")
    else:
        st.success("Target complete or Syllabus not deployed. Check the Engine Room.")

# --- PAGE: DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Persistent Library Manager")
    target = st.selectbox("Select Topic to Link Books:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    
    new_link = st.text_input("Paste URL to Save in Repository:")
    if st.button("➕ Add to Repository"):
        if new_link.startswith("http"):
            current = str(df.at[idx, "Resources"]).replace('nan', '')
            updated = f"{current}, {new_link}" if current else new_link
            df.at[idx, "Resources"] = updated
            save_data(df) # Write to Google Sheets
            st.success("Resource saved permanently!")
            st.rerun()

    st.divider()
    st.subheader("📂 All Saved Resources (By Topic)")
    active_lib = df[df['Resources'].astype(str).str.contains("http", na=False)]
    if not active_lib.empty:
        for _, row in active_lib.iterrows():
            with st.expander(f"📚 {row['Topic']}"):
                t_links = [l.strip() for l in str(row['Resources']).split(",") if l.strip()]
                for i, l in enumerate(t_links):
                    st.write(f"**({chr(97+i)})** {l}")
    else:
        st.info("Your repository is empty.")

# --- PAGE: STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 Persistent High-Yield Notes")
    target = st.selectbox("Select Topic:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    
    existing_notes = str(df.at[idx, 'Notes']).replace('nan', '')
    notes = st.text_area("Write/Edit Notes:", value=existing_notes, height=400)
    
    if st.button("💾 Sync Notes to Cloud"):
        df.at[idx, 'Notes'] = notes
        save_data(df)
        st.success("Notes saved and synced!")

# --- PAGE: ATTENDANCE LOG ---
elif page == "⏱️ Attendance Log":
    st.title("⏱️ Persistent Study Log")
    target = st.selectbox("Topic Completed:", df['Topic'].tolist())
    idx = df[df['Topic'] == target].index[0]
    
    c1, c2 = st.columns(2)
    s_t = c1.text_input("Start Time", "10:00 PM")
    e_t = c2.text_input("End Time", "12:00 AM")
    
    if st.button("✅ Mark Completed & Save"):
        df.at[idx, "Status"] = "Completed"
        df.at[idx, "Start_Time"] = s_t
        df.at[idx, "End_Time"] = e_t
        save_data(df)
        st.success("Progress logged in the cloud!")
        st.rerun()

# --- PAGE: ENGINE ROOM (FULL 60-DAY SYLLABUS) ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ System Core")
    if st.button("🚀 DEPLOY FULL 60-DAY SYLLABUS (MASTER VERSION)"):
        master_syllabus = [
            # WEEK 1: Ancient & Medieval
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Seals, Trade. Vedic: Early/Later, Rivers, Sabha/Samiti."},
            {"Day": 2, "Sub": "History", "Top": "16 Mahajanapadas & Magadh Rise. Jainism & Buddhism Councils & Philosophy."},
            {"Day": 3, "Sub": "History", "Top": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas & Art Schools."},
            {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda (Amoghbhuti coins), Yaudheya, Katyuri Admin & Architecture."},
            {"Day": 5, "Sub": "History", "Top": "Guptas: Golden Age Admin, Literature, Science. Harshavardhana & South Dynasties."},
            {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave to Lodi. Market Reforms & Indo-Islamic Architecture."},
            {"Day": 7, "Sub": "REVISION", "Top": "Mock 1: Ancient & Medieval Comprehensive Revision."},
            # WEEK 2: Medieval UK & Modern
            {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand Dynasty (Kumaon), Parmar (Garhwal). Gorkha Rule (1790-1815)."},
            {"Day": 9, "Sub": "History", "Top": "Modern: European Arrival, Battle of Plassey/Buxar. Land Revenue: Zamindari/Ryotwari."},
            {"Day": 10, "Sub": "History", "Top": "1857 Revolt: UK's Role. Socio-Religious Reforms: Brahmo & Arya Samaj."},
            {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Sugauli Treaty, British Admin, Coolie Begar & Dola Palki Movement."},
            {"Day": 12, "Sub": "History", "Top": "National Mov: Gandhi Era (Non-Coop, Civil Dis, Quit India). Cabinet Mission."},
            {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri Merger (1949), 1994 Muzaffarnagar Kand, Formation 2000."},
            {"Day": 14, "Sub": "REVISION", "Top": "Mock 2: Modern History & UK Statehood Mastery."},
            # WEEK 3: Geography
            {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Lithosphere: Earth's Structure. Atmosphere: Layers, Winds, Pressure."},
            {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents, Tides, Salinity."},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon Mechanism & Seasons."},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soils, Vegetation & Forests."},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali). Climate & Rainfall."},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "Resources: UK Forest Policy, Wildlife Sanctuaries & National Parks (Jim Corbett)."},
            {"Day": 21, "Sub": "REVISION", "Top": "Mock 3: World, India & UK Geography."},
            # WEEK 4: Polity
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Rights, DPSP & Duties. Amendments (42/44)."},
            {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, Committees. Judiciary: SC/HC & Writ Jurisdiction."},
            {"Day": 24, "Sub": "Polity", "Top": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism: Centre-State Relations."},
            {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly. Secretariat & District Admin."},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: 73rd/74th Amnds. UK Panchayati Raj Act & RTI in UK."},
            {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Welfare Schemes, Human Rights, Citizen's Charter."},
            {"Day": 28, "Sub": "REVISION", "Top": "Mock 4: Indian Polity & UK Governance."},
            # WEEK 5: Economy
            {"Day": 29, "Sub": "Economy", "Top": "Indian Economy Features, NITI Aayog. LPG Reforms 1991."},
            {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI (Monetary Policy), SEBI, NABARD. Stock Markets."},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budget, GST, Finance Commission. Poverty (MNREGA)."},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism & Pilgrimage Impact."},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy, Medicinal Herbs."},
            {"Day": 34, "Sub": "Economy", "Top": "SDG Goals, HDI Index, WTO & IMF."},
            {"Day": 35, "Sub": "REVISION", "Top": "Mock 5: Economy (India & UK)."},
            # WEEK 6: Science & Tech
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Nuclear Energy. Chemistry: Polymers, Acids/Bases."},
            {"Day": 37, "Sub": "Science", "Top": "Biology: Cell, Genetics, Human Systems (Circulation/Digestion)."},
            {"Day": 38, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security, Cloud Computing. ISRO."},
            {"Day": 39, "Sub": "Science", "Top": "Environment: Ecology, Food Chain, Biodiversity Hotspots (UK)."},
            {"Day": 40, "Sub": "Science (UK)", "Top": "Disaster Mgmt: UK Vulnerability (Earthquakes/Landslides), SDMA."},
            {"Day": 41, "Sub": "Science", "Top": "Space & Defense: Nuclear Power, DRDO, Recent Tech Updates."},
            {"Day": 42, "Sub": "REVISION", "Top": "Mock 6: General Science & Tech."},
            # WEEK 7: Culture & Current
            {"Day": 43, "Sub": "Culture (UK)", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari, Buxa, Raji. Folk Art, Music."},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs & Festivals: Nanda Devi, Kumbh. Sites: Panch Kedar/Badri."},
            {"Day": 45, "Sub": "Current", "Top": "National: Awards, Sports, Summits, Appointments. Reports."},
            {"Day": 46, "Sub": "Current", "Top": "International: UN, BRICS, G20. World Indices."},
            {"Day": 47, "Sub": "Current (UK)", "Top": "UK State Current: Budget, CM Dashboards, Welfare Schemes."},
            {"Day": 48, "Sub": "Current", "Top": "Sports: Olympics, Cricket. Famous Personalities."},
            {"Day": 49, "Sub": "REVISION", "Top": "Mock 7: Culture & Year-long Current Affairs."},
            # WEEK 8: CSAT
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations, Direction Sense."},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams, Seating Arrangement."},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio, Percentage, Average."},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Profit/Loss, Time & Work, Data Interpretation (DI)."},
            {"Day": 54, "Sub": "CSAT", "Top": "Comprehension: English Passage Reading & Vocabulary."},
            {"Day": 55, "Sub": "CSAT", "Top": "General Hindi: Grammar, Tatsam-Tadbhav, Antonyms."},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Full Mock Simulation."},
            # FINAL STRETCH
            {"Day": 57, "Sub": "MOCK", "Top": "GS Full Mock 1: Entire Paper I Simulation."},
            {"Day": 58, "Sub": "MOCK", "Top": "CSAT Full Mock 2: Entire Paper II Simulation."},
            {"Day": 59, "Sub": "MOCK", "Top": "GS Full Mock 3: Revision of Weak Topics."},
            {"Day": 60, "Sub": "MOCK", "Top": "FINAL SIMULATION: Combined Paper I & II (D-Day Prep)."}
        ]
        new_df = pd.DataFrame(master_syllabus)
        for col in ["Status", "Notes", "Start_Time", "End_Time", "Resources"]:
            new_df[col] = ""
        new_df["Status"] = "Planned"
        save_data(new_df)
        st.success("Master Syllabus Deployed & Synced to Cloud!"); st.rerun()

# --- PAGE: ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 Progress Tracker")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)