import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. PERSISTENCE ENGINE
def load_data():
    # ttl=0 is critical to see changes immediately after clicking Deploy
    data = conn.read(worksheet="Tasks", ttl=0)
    expected_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    
    # If sheet is totally empty, create a dummy row so the app doesn't crash
    if data.empty:
        return pd.DataFrame(columns=expected_cols)
        
    for col in expected_cols:
        if col not in data.columns:
            data[col] = ""
            
    # Clean data types for reliable display
    data["Day"] = pd.to_numeric(data["Day"], errors='coerce').fillna(0).astype(int)
    data["Subject"] = data["Subject"].astype(str).replace(['nan', 'None', ''], 'N/A')
    data["Topic"] = data["Topic"].astype(str).replace(['nan', 'None', ''], 'Pending Deployment')
    return data

def save_data(data):
    # This pushes the entire dataframe to the cloud
    conn.update(worksheet="Tasks", data=data)
    st.cache_data.clear() 

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- PAGE: DASHBOARD ---
if page == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    # Using 2026-02-13 as start date based on your context
    start_date = datetime(2026, 2, 13).date()
    days_passed = (datetime.now().date() - start_date).days + 1
    
    today_task = df[df["Day"] == days_passed]
    
    if not today_task.empty and today_task.iloc[0]["Topic"] != "Pending Deployment":
        row = today_task.iloc[0]
        idx = today_task.index[0]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.info(f"🚩 **Current Duty: Day {days_passed}**")
            st.header(f"{row['Subject']}: {row['Topic']}")
            
            # Display Resources
            links = [l.strip() for l in str(row['Resources']).split(",") if "http" in l]
            if links:
                st.write("### 📖 Study Resources")
                for i, link in enumerate(links):
                    st.link_button(f"({chr(97+i)}) Open Resource", link)
            else:
                st.warning("⚠️ No resources linked. Use 'Digital Library' to add books.")
        
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
        st.error("⚠️ Syllabus not found for today. Please go to 'Engine Room' and click Deploy.")

    st.divider()
    st.subheader("📋 Upcoming Agenda")
    # Filter out empty/dummy rows for the agenda view
    agenda = df[df["Day"] >= days_passed].sort_values("Day").head(10)
    st.table(agenda[["Day", "Subject", "Topic", "Status"]])

# --- PAGE: DIGITAL LIBRARY ---
elif page == "📚 Digital Library":
    st.title("📚 Persistent Repository")
    valid_topics = df[df["Topic"] != "Pending Deployment"]["Topic"].tolist()
    if valid_topics:
        target = st.selectbox("Select Topic:", valid_topics)
        idx = df[df['Topic'] == target].index[0]
        url = st.text_input("Paste Resource URL:")
        if st.button("💾 Store Permanently"):
            curr = str(df.at[idx, "Resources"]).replace('nan', '').strip()
            df.at[idx, "Resources"] = f"{curr}, {url}" if curr else url
            save_data(df); st.success("Saved!"); st.rerun()
            
        st.divider()
        st.subheader("📂 Repository Books")
        for _, r in df[df["Resources"].str.contains("http", na=False)].iterrows():
            with st.expander(f"📚 {r['Topic']}"):
                for link in r['Resources'].split(","):
                    st.write(link.strip())
    else:
        st.warning("Deploy syllabus first.")

# --- PAGE: STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 Persistent Notes")
    valid_topics = df[df["Topic"] != "Pending Deployment"]["Topic"].tolist()
    if valid_topics:
        target = st.selectbox("Topic:", valid_topics)
        idx = df[df['Topic'] == target].index[0]
        txt = st.text_area("Notes:", value=str(df.at[idx, 'Notes']).replace('nan', ''), height=400)
        if st.button("💾 Sync to Cloud"):
            df.at[idx, 'Notes'] = txt
            save_data(df); st.success("Synced!")
    else:
        st.warning("Deploy syllabus first.")

# --- PAGE: ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 Master 60-Day Tracker")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)

# --- PAGE: ENGINE ROOM ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    if st.button("🚀 FORCE DEPLOY FULL SYLLABUS"):
        master_syllabus = [
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Seals, Trade. Vedic: Early/Later, Rivers."},
            {"Day": 2, "Sub": "History", "Top": "16 Mahajanapadas & Magadh Rise. Jainism & Buddhism Philosophy."},
            {"Day": 3, "Sub": "History", "Top": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas."},
            {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda, Yaudheya, Katyuri Admin."},
            {"Day": 5, "Sub": "History", "Top": "Guptas: Golden Age. Harshavardhana & South Dynasties."},
            {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave to Lodi. Market Reforms."},
            {"Day": 7, "Sub": "REVISION", "Top": "Mock 1: Ancient & Medieval Comprehensive Revision."},
            {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand Dynasty, Parmar Dynasty. Gorkha Rule."},
            {"Day": 9, "Sub": "History", "Top": "Modern: European Arrival, Land Revenue Systems."},
            {"Day": 10, "Sub": "History", "Top": "1857 Revolt: UK's Role. Socio-Religious Reforms."},
            {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Sugauli Treaty, British Admin, Coolie Begar."},
            {"Day": 12, "Sub": "History", "Top": "National Mov: Gandhi Era (Non-Coop, Civil Dis, Quit India)."},
            {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri Merger, Muzaffarnagar Kand, Formation."},
            {"Day": 14, "Sub": "REVISION", "Top": "Mock 2: Modern History & UK Statehood."},
            {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Earth Structure. Atmosphere: Layers."},
            {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents, Tides."},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon."},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soils."},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali)."},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "Resources: UK Forest Policy, Wildlife, 2011 Census."},
            {"Day": 21, "Sub": "REVISION", "Top": "Mock 3: Geography (World, India, UK)."},
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Rights, DPSP & Duties. Amendments."},
            {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, Committees. Judiciary: SC/HC."},
            {"Day": 24, "Sub": "Polity", "Top": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism."},
            {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly."},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: 73rd/74th Amnds. UK Panchayati Raj Act."},
            {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Welfare Schemes, Human Rights."},
            {"Day": 28, "Sub": "REVISION", "Top": "Mock 4: Indian Polity & UK Governance."},
            {"Day": 29, "Sub": "Economy", "Top": "Indian Economy Features, NITI Aayog. LPG Reforms 1991."},
            {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI, SEBI, NABARD. Stock Markets."},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budget, GST, Finance Commission."},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism Policy."},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy."},
            {"Day": 34, "Sub": "Economy", "Top": "SDG Goals, HDI Index, WTO & IMF."},
            {"Day": 35, "Sub": "REVISION", "Top": "Mock 5: Economy (India & UK)."},
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound. Chemistry: Polymers, Acids/Bases."},
            {"Day": 37, "Sub": "Science", "Top": "Biology: Cell, Genetics, Human Systems."},
            {"Day": 38, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security. ISRO."},
            {"Day": 39, "Sub": "Science", "Top": "Environment: Ecology, Food Chain, Biodiversity (UK)."},
            {"Day": 40, "Sub": "Science (UK)", "Top": "Disaster Mgmt: Earthquakes/Landslides, SDMA."},
            {"Day": 41, "Sub": "Science", "Top": "Space & Defense: Nuclear Power, DRDO, Recent Tech."},
            {"Day": 42, "Sub": "REVISION", "Top": "Mock 6: General Science & Tech."},
            {"Day": 43, "Sub": "Culture (UK)", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari. Folk Art, Music."},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs & Festivals: Nanda Devi, Kumbh. Panch Kedar."},
            {"Day": 45, "Sub": "Current", "Top": "National: Awards, Sports, Summits, Appointments."},
            {"Day": 46, "Sub": "Current", "Top": "International: UN, BRICS, G20. World Indices."},
            {"Day": 47, "Sub": "Current (UK)", "Top": "UK State Current: Budget, CM Dashboards, Welfare."},
            {"Day": 48, "Sub": "Current", "Top": "Sports: Olympics, Cricket. Famous UK Personalities."},
            {"Day": 49, "Sub": "REVISION", "Top": "Mock 7: Culture & Year-long Current Affairs."},
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations, Directions."},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams, Seating."},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio, Percentage."},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Profit/Loss, Time & Work, DI."},
            {"Day": 54, "Sub": "CSAT", "Top": "Comprehension: English Passage & Vocabulary."},
            {"Day": 55, "Sub": "CSAT", "Top": "General Hindi: Grammar, Tatsam-Tadbhav, Antonyms."},
            {"Day": 56, "Sub": "REVISION", "Top": "CSAT Full Mock Simulation."},
            {"Day": 57, "Sub": "MOCK", "Top": "GS Full Mock 1: Entire Paper I Simulation."},
            {"Day": 58, "Sub": "MOCK", "Top": "CSAT Full Mock 2: Entire Paper II Simulation."},
            {"Day": 59, "Sub": "MOCK", "Top": "GS Full Mock 3: Revision of Weak Topics."},
            {"Day": 60, "Sub": "MOCK", "Top": "FINAL SIMULATION: Combined Paper I & II prep."}
        ]
        new_df = pd.DataFrame(master_syllabus)
        for col in ["Status", "Notes", "Start_Time", "End_Time", "Resources"]:
            new_df[col] = ""
        new_df["Status"] = "Planned"
        save_data(new_df)
        st.success("Syllabus Live! Refreshing now..."); st.rerun()