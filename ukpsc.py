import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. THE COMPLETE 60-DAY SYLLABUS (Hard-coded for stability)
MASTER_SYLLABUS = [
    {"Day": 1, "Subject": "History", "Topic": "Harappa: Town Planning, Seals, Trade. Vedic: Early/Later, Rivers, Sabha/Samiti."},
    {"Day": 2, "Subject": "History", "Topic": "16 Mahajanapadas & Magadh Rise. Jainism & Buddhism Councils & Philosophy."},
    {"Day": 3, "Subject": "History", "Topic": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas & Art Schools."},
    {"Day": 4, "Subject": "History (UK)", "Topic": "Ancient UK: Kuninda (Amoghbhuti coins), Yaudheya, Katyuri Admin & Architecture."},
    {"Day": 5, "Subject": "History", "Topic": "Guptas: Golden Age Admin, Literature, Science. Harshavardhana & South Dynasties."},
    {"Day": 6, "Subject": "History", "Topic": "Delhi Sultanate: Slave to Lodi. Market Reforms & Indo-Islamic Architecture."},
    {"Day": 7, "Subject": "REVISION", "Topic": "Mock 1: Ancient & Medieval Comprehensive Revision."},
    {"Day": 8, "Subject": "History (UK)", "Topic": "Medieval UK: Chand Dynasty (Kumaon), Parmar (Garhwal). Gorkha Rule (1790-1815)."},
    {"Day": 9, "Subject": "History", "Topic": "Modern: European Arrival, Battle of Plassey/Buxar. Land Revenue Systems."},
    {"Day": 10, "Subject": "History", "Topic": "1857 Revolt: UK's Role. Socio-Religious Reforms: Brahmo & Arya Samaj."},
    {"Day": 11, "Subject": "History (UK)", "Topic": "Modern UK: Sugauli Treaty, British Admin, Coolie Begar & Dola Palki Movement."},
    {"Day": 12, "Subject": "History", "Topic": "National Mov: Gandhi Era (Non-Coop, Civil Dis, Quit India). Cabinet Mission."},
    {"Day": 13, "Subject": "History (UK)", "Topic": "UK Statehood: Tehri Merger (1949), 1994 Muzaffarnagar Kand, Formation 2000."},
    {"Day": 14, "Subject": "REVISION", "Topic": "Mock 2: Modern History & UK Statehood Mastery."},
    {"Day": 15, "Subject": "Geo (World)", "Topic": "Solar System, Lithosphere: Rocks. Atmosphere: Layers, Winds, Pressure."},
    {"Day": 16, "Subject": "Geo (World)", "Topic": "Hydrosphere: Ocean Relief, Currents, Tides, Salinity."},
    {"Day": 17, "Subject": "Geo (India)", "Topic": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon Mechanism."},
    {"Day": 18, "Subject": "Geo (India)", "Topic": "Drainage: Himalayan vs Peninsular Rivers. Soils, Vegetation."},
    {"Day": 19, "Subject": "Geo (UK)", "Topic": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali). Climate."},
    {"Day": 20, "Subject": "Geo (UK)", "Topic": "Resources: UK Forest Policy, Jim Corbett Park, Minerals & 2011 Census."},
    {"Day": 21, "Subject": "REVISION", "Topic": "Mock 3: Geography (World, India, UK)."},
    {"Day": 22, "Subject": "Polity", "Topic": "Constitution: Preamble, Rights, DPSP & Duties. Amendments (42/44)."},
    {"Day": 23, "Subject": "Polity", "Topic": "Parliament: President, PM, Committees. Judiciary: SC/HC Writs."},
    {"Day": 24, "Subject": "Polity", "Topic": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism."},
    {"Day": 25, "Subject": "Polity (UK)", "Topic": "UK Admin: Governor, CM, Legislative Assembly. Secretariat."},
    {"Day": 26, "Subject": "Polity (UK)", "Topic": "Local Gov: 73rd/74th Amnds. UK Panchayati Raj Act & RTI."},
    {"Day": 27, "Subject": "Polity", "Topic": "Public Policy: Welfare Schemes, Human Rights, Citizen's Charter."},
    {"Day": 28, "Subject": "REVISION", "Topic": "Mock 4: Indian Polity & UK Governance."},
    {"Day": 29, "Subject": "Economy", "Topic": "Indian Economy Features, NITI Aayog. LPG Reforms 1991."},
    {"Day": 30, "Subject": "Economy", "Topic": "Banking: RBI (Monetary Policy), SEBI, NABARD. Stock Markets."},
    {"Day": 31, "Subject": "Economy", "Topic": "Public Finance: Budget, GST, Finance Commission. Poverty."},
    {"Day": 32, "Subject": "Economy (UK)", "Topic": "UK Economy: Per Capita Income, Budget. Tourism Policy."},
    {"Day": 33, "Subject": "Economy (UK)", "Topic": "Agriculture in UK: Horticulture, MSME Policy, Medicinal Herbs."},
    {"Day": 34, "Subject": "Economy", "Topic": "SDG Goals, HDI Index, WTO & IMF."},
    {"Day": 35, "Subject": "REVISION", "Topic": "Mock 5: Economy (India & UK)."},
    {"Day": 36, "Subject": "Science", "Topic": "Physics: Light, Sound, Nuclear Energy. Chemistry: Acids/Bases."},
    {"Day": 37, "Subject": "Science", "Topic": "Biology: Cell, Genetics, Human Systems (Circulation/Digestion)."},
    {"Day": 38, "Subject": "Science", "Topic": "ICT: E-Governance, Internet, Cyber Security. ISRO."},
    {"Day": 39, "Subject": "Science", "Topic": "Environment: Ecology, Food Chain, Biodiversity Hotspots (UK)."},
    {"Day": 40, "Subject": "Science (UK)", "Topic": "Disaster Mgmt: Earthquakes/Landslides, SDMA structure."},
    {"Day": 41, "Subject": "Science", "Topic": "Space & Defense: Nuclear Power, DRDO, Recent Tech Updates."},
    {"Day": 42, "Subject": "REVISION", "Topic": "Mock 6: General Science & Tech."},
    {"Day": 43, "Subject": "Culture (UK)", "Topic": "UK Tribes: Bhotia, Tharu, Jaunsari, Buxa, Raji. Folk Arts."},
    {"Day": 44, "Subject": "Culture (UK)", "Topic": "Fairs & Festivals: Nanda Devi, Kumbh. Panch Kedar/Badri."},
    {"Day": 45, "Subject": "Current", "Topic": "National: Awards, Sports, Summits, Appointments. Reports."},
    {"Day": 46, "Subject": "Current", "Topic": "International: UN, BRICS, G20. World Indices."},
    {"Day": 47, "Subject": "Current (UK)", "Topic": "UK State Current: Budget, CM Dashboards, Welfare Schemes."},
    {"Day": 48, "Subject": "Current", "Topic": "Sports: Olympics, Cricket. Famous UK Personalities."},
    {"Day": 49, "Subject": "REVISION", "Topic": "Mock 7: Culture & Year-long Current Affairs."},
    {"Day": 50, "Subject": "CSAT", "Topic": "Reasoning: Coding-Decoding, Blood Relations, Direction Sense."},
    {"Day": 51, "Subject": "CSAT", "Topic": "Reasoning: Syllogism, Venn Diagrams, Seating Arrangement."},
    {"Day": 52, "Subject": "CSAT", "Topic": "Numerical: Number System, Ratio, Percentage, Average."},
    {"Day": 53, "Subject": "CSAT", "Topic": "Numerical: Profit/Loss, Time & Work, Data Interpretation."},
    {"Day": 54, "Subject": "CSAT", "Topic": "Comprehension: English Passage Reading & Vocabulary."},
    {"Day": 55, "Subject": "CSAT", "Topic": "General Hindi: Grammar, Tatsam-Tadbhav, Antonyms."},
    {"Day": 56, "Subject": "REVISION", "Topic": "CSAT Full Mock Simulation."},
    {"Day": 57, "Subject": "MOCK", "Topic": "GS Full Mock 1: Entire Paper I Simulation."},
    {"Day": 58, "Subject": "MOCK", "Topic": "CSAT Full Mock 2: Entire Paper II Simulation."},
    {"Day": 59, "Subject": "MOCK", "Topic": "GS Full Mock 3: Revision of Weak Topics."},
    {"Day": 60, "Subject": "MOCK", "Topic": "FINAL SIMULATION: Combined Paper I & II prep."}
]

# 3. PERSISTENCE ENGINE
def load_data():
    try:
        data = conn.read(worksheet="Tasks", ttl=0)
    except:
        data = pd.DataFrame()
        
    master_df = pd.DataFrame(MASTER_SYLLABUS)
    
    # Merge cloud data if it exists
    if not data.empty:
        for col in ["Status", "Notes", "Start_Time", "End_Time", "Resources"]:
            if col in data.columns:
                mapping = dict(zip(data["Day"], data[col]))
                master_df[col] = master_df["Day"].map(mapping).fillna("")
            else:
                master_df[col] = ""
    else:
        for col in ["Status", "Notes", "Start_Time", "End_Time", "Resources"]:
            master_df[col] = ""
    return master_df

def save_data(data):
    conn.update(worksheet="Tasks", data=data)
    st.cache_data.clear() 

df = load_data()

# 4. SIDEBAR
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- PAGE: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    today_task = df[df["Day"] == days_passed]
    
    if not today_task.empty:
        row = today_task.iloc[0]
        idx = today_task.index[0]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.info(f"🚩 **Current Duty: Day {days_passed}**")
            st.header(f"{row['Subject']}: {row['Topic']}")
            
            # Resources
            res_links = [l.strip() for l in str(row['Resources']).split(",") if "http" in l]
            if res_links:
                st.write("### 📖 Study Resources")
                for i, link in enumerate(res_links):
                    st.link_button(f"({chr(97+i)}) Open Resource", link)
            else:
                st.warning("⚠️ No links saved for this topic yet.")
        
        with c2:
            st.write("### ⚡ Quick Actions")
            with st.expander("✅ Log Completion", expanded=True):
                s = st.text_input("Start Time", "10:00 PM")
                e = st.text_input("End Time", "12:00 AM")
                if st.button("Save To Roadmap"):
                    df.at[idx, "Status"] = "Completed"
                    df.at[idx, "Start_Time"] = s
                    df.at[idx, "End_Time"] = e
                    save_data(df); st.rerun()
            
            if st.button("☕ Take Break (Shift Schedule)"):
                mask = df["Day"] >= days_passed
                df.loc[mask, "Day"] += 1
                save_data(df); st.rerun()
    else:
        st.error("Schedule out of bounds. Check the 60-Day Roadmap.")

    st.divider()
    st.subheader("📋 Upcoming Agenda (Next 10 Days)")
    agenda = df[df["Day"] >= days_passed].sort_values("Day").head(10)
    st.table(agenda[["Day", "Subject", "Topic", "Status"]])

# --- PAGE: DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Persistent Repository")
    target = st.selectbox("Assign resource to topic:", df["Topic"].tolist())
    idx = df[df['Topic'] == target].index[0]
    url = st.text_input("Paste Resource URL:")
    if st.button("💾 Store in Repository"):
        curr = str(df.at[idx, "Resources"]).replace('nan', '').strip()
        df.at[idx, "Resources"] = f"{curr}, {url}" if curr else url
        save_data(df); st.success("Saved to Cloud!"); st.rerun()
    
    st.divider()
    st.subheader("📂 All Stored Books")
    active_lib = df[df["Resources"].str.contains("http", na=False)]
    for _, r in active_lib.iterrows():
        with st.expander(f"📚 {r['Topic']}"):
            for link in r['Resources'].split(","):
                st.write(link.strip())

# --- PAGE: STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 High-Yield Notes")
    target = st.selectbox("Note for:", df["Topic"].tolist())
    idx = df[df['Topic'] == target].index[0]
    txt = st.text_area("Write Notes:", value=str(df.at[idx, 'Notes']).replace('nan', ''), height=400)
    if st.button("💾 Sync to Cloud"):
        df.at[idx, 'Notes'] = txt
        save_data(df); st.success("Synced!")

# --- PAGE: ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 Master Tracker")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)

# --- PAGE: ENGINE ROOM ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    if st.button("🚀 SYNC LOCAL SYLLABUS TO CLOUD"):
        save_data(df)
        st.success("Cloud data aligned with Master Syllabus!")