import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. System Configuration
st.set_page_config(page_title="UKPSC Sentinel", layout="wide", page_icon="🏔️")
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. PERSISTENCE ENGINE: THE SOURCE OF TRUTH
def load_data():
    # ttl=0 is mandatory to ensure real-time updates across all tabs
    data = conn.read(worksheet="Tasks", ttl=0)
    expected_cols = ["Day", "Subject", "Topic", "Status", "Notes", "Start_Time", "End_Time", "Resources"]
    for col in expected_cols:
        if col not in data.columns:
            data[col] = ""
    data["Day"] = pd.to_numeric(data["Day"], errors='coerce').fillna(0).astype(int)
    data["Topic"] = data["Topic"].astype(str).replace(['nan', 'None'], 'Empty Topic')
    data["Resources"] = data["Resources"].astype(str).replace(['nan', 'None'], '')
    return data

def save_data(data):
    # This physically writes the local changes back to your Google Sheet
    conn.update(worksheet="Tasks", data=data)
    st.cache_data.clear() 

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Sentinel Command")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

# --- PAGE: DASHBOARD (Includes Attendance & Agenda) ---
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
            
            # Sub-series Numbered Resources (a, b, c)
            res_list = [l.strip() for l in str(row['Resources']).split(",") if l.strip().startswith("http")]
            if res_list:
                st.write("### 📖 Study Resources")
                for i, link in enumerate(res_list):
                    st.link_button(f"({chr(97+i)}) {link[:40]}...", link)
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
                    save_data(df); st.success("Logged!"); st.rerun()
            
            if st.button("☕ Take Break (Shift Schedule)"):
                mask = df["Day"] >= days_passed
                df.loc[mask, "Day"] += 1
                save_data(df); st.success("Schedule Shifted!"); st.rerun()
    else:
        st.error("No topic assigned for today. Go to Engine Room and Deploy.")

    st.divider()
    st.subheader("📋 Upcoming Agenda (Full Topic List)")
    agenda = df[df["Day"] >= days_passed].sort_values("Day").head(10)
    if not agenda.empty:
        st.table(agenda[["Day", "Subject", "Topic", "Status"]])

# --- PAGE: DIGITAL LIBRARY (The Repository) ---
elif page == "📚 Digital Library":
    st.title("📚 Persistent Repository")
    # Using topic names for the selector
    topic_list = [t for t in df["Topic"].tolist() if t != "Empty Topic"]
    if topic_list:
        target = st.selectbox("Assign resource to topic:", topic_list)
        idx = df[df['Topic'] == target].index[0]
        
        new_url = st.text_input("Paste Resource URL:")
        if st.button("💾 Store in Repository"):
            if new_url.startswith("http"):
                curr = str(df.at[idx, "Resources"]).strip()
                updated = f"{curr}, {new_url}" if curr else new_url
                df.at[idx, "Resources"] = updated
                save_data(df); st.success("Saved to Cloud Repository!"); st.rerun()
        
        st.divider()
        st.subheader("📂 All Stored Books")
        active_lib = df[df["Resources"].str.contains("http", na=False)]
        for _, r in active_lib.iterrows():
            with st.expander(f"📚 {r['Topic']}"):
                for link in r['Resources'].split(","):
                    st.write(link.strip())
    else:
        st.warning("Please deploy the syllabus in the Engine Room first.")

# --- PAGE: STUDY NOTES ---
elif page == "📝 Study Notes":
    st.title("📝 Persistent Study Notes")
    topic_list = [t for t in df["Topic"].tolist() if t != "Empty Topic"]
    if topic_list:
        target = st.selectbox("Select Topic to Write Notes:", topic_list)
        idx = df[df['Topic'] == target].index[0]
        
        existing = str(df.at[idx, 'Notes']).replace('nan', '')
        txt = st.text_area("High-Yield Points:", value=existing, height=400)
        
        if st.button("💾 Sync Notes to Cloud"):
            df.at[idx, 'Notes'] = txt
            save_data(df); st.success("Notes permanently synced!")
    else:
        st.warning("Please deploy the syllabus in the Engine Room first.")

# --- PAGE: ROADMAP ---
elif page == "📅 60-Day Roadmap":
    st.title("📅 Master 60-Day Tracker")
    st.dataframe(df.sort_values("Day"), use_container_width=True, hide_index=True)

# --- PAGE: ENGINE ROOM (THE FULL SYLLABUS) ---
elif page == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    if st.button("🚀 DEPLOY FULL 60-DAY MASTER SYLLABUS"):
        master_syllabus = [
            {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Seals, Trade. Vedic: Early/Later, Rivers, Sabha/Samiti."},
            {"Day": 2, "Sub": "History", "Top": "16 Mahajanapadas & Magadh Rise. Jainism & Buddhism Councils & Philosophy."},
            {"Day": 3, "Sub": "History", "Top": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas & Art Schools."},
            {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda (Amoghbhuti coins), Yaudheya, Katyuri Admin & Architecture."},
            {"Day": 5, "Sub": "History", "Top": "Guptas: Golden Age Admin, Literature, Science. Harshavardhana & South Dynasties."},
            {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave to Lodi. Market Reforms & Indo-Islamic Architecture."},
            {"Day": 7, "Sub": "REVISION", "Top": "Mock 1: Ancient & Medieval Comprehensive Revision."},
            {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand Dynasty (Kumaon), Parmar (Garhwal). Gorkha Rule (1790-1815)."},
            {"Day": 9, "Sub": "History", "Top": "Modern: European Arrival, Battle of Plassey/Buxar. Land Revenue Systems."},
            {"Day": 10, "Sub": "History", "Top": "1857 Revolt: UK's Role. Socio-Religious Reforms: Brahmo & Arya Samaj."},
            {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Sugauli Treaty, British Admin, Coolie Begar & Dola Palki."},
            {"Day": 12, "Sub": "History", "Top": "National Mov: Gandhi Era (Non-Coop, Civil Dis, Quit India)."},
            {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri Merger (1949), 1994 Muzaffarnagar Kand, Formation 2000."},
            {"Day": 14, "Sub": "REVISION", "Top": "Mock 2: Modern History & UK Statehood Mastery."},
            {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Lithosphere: Rocks. Atmosphere: Layers, Winds, Pressure."},
            {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents, Tides, Salinity."},
            {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon Mechanism."},
            {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soils, Vegetation."},
            {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali). Climate."},
            {"Day": 20, "Sub": "Geo (UK)", "Top": "Resources: UK Forest Policy, Jim Corbett Park, Minerals & 2011 Census."},
            {"Day": 21, "Sub": "REVISION", "Top": "Mock 3: World, India & UK Geography."},
            {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Rights, DPSP & Duties. Amendments (42/44)."},
            {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, Committees. Judiciary: SC/HC Writs."},
            {"Day": 24, "Sub": "Polity", "Top": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism."},
            {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly. Secretariat."},
            {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: 73rd/74th Amnds. UK Panchayati Raj Act & RTI."},
            {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Welfare Schemes, Human Rights, Citizen's Charter."},
            {"Day": 28, "Sub": "REVISION", "Top": "Mock 4: Indian Polity & UK Governance."},
            {"Day": 29, "Sub": "Economy", "Top": "Indian Economy Features, NITI Aayog. LPG Reforms 1991."},
            {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI (Monetary Policy), SEBI, NABARD. Stock Markets."},
            {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budget, GST, Finance Commission. Poverty."},
            {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism Policy."},
            {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy, Medicinal Herbs."},
            {"Day": 34, "Sub": "Economy", "Top": "SDG Goals, HDI Index, WTO & IMF."},
            {"Day": 35, "Sub": "REVISION", "Top": "Mock 5: Economy (India & UK)."},
            {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Nuclear Energy. Chemistry: Acids/Bases."},
            {"Day": 37, "Sub": "Science", "Top": "Biology: Cell, Genetics, Human Systems (Circulation/Digestion)."},
            {"Day": 38, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security. ISRO."},
            {"Day": 39, "Sub": "Science", "Top": "Environment: Ecology, Food Chain, Biodiversity Hotspots (UK)."},
            {"Day": 40, "Sub": "Science (UK)", "Top": "Disaster Mgmt: Earthquakes/Landslides, SDMA structure."},
            {"Day": 41, "Sub": "Science", "Top": "Space & Defense: Nuclear Power, DRDO, Recent Tech Updates."},
            {"Day": 42, "Sub": "REVISION", "Top": "Mock 6: General Science & Tech."},
            {"Day": 43, "Sub": "Culture (UK)", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari, Buxa, Raji. Folk Arts."},
            {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs & Festivals: Nanda Devi, Kumbh. Panch Kedar/Badri."},
            {"Day": 45, "Sub": "Current", "Top": "National: Awards, Sports, Summits, Appointments. Reports."},
            {"Day": 46, "Sub": "Current", "Top": "International: UN, BRICS, G20. World Indices."},
            {"Day": 47, "Sub": "Current (UK)", "Top": "UK State Current: Budget, CM Dashboards, Welfare Schemes."},
            {"Day": 48, "Sub": "Current", "Top": "Sports: Olympics, Cricket. Famous UK Personalities."},
            {"Day": 49, "Sub": "REVISION", "Top": "Mock 7: Culture & Year-long Current Affairs."},
            {"Day": 50, "Sub": "CSAT", "Top": "Reasoning: Coding-Decoding, Blood Relations, Direction Sense."},
            {"Day": 51, "Sub": "CSAT", "Top": "Reasoning: Syllogism, Venn Diagrams, Seating Arrangement."},
            {"Day": 52, "Sub": "CSAT", "Top": "Numerical: Number System, Ratio, Percentage, Average."},
            {"Day": 53, "Sub": "CSAT", "Top": "Numerical: Profit/Loss, Time & Work, Data Interpretation."},
            {"Day": 54, "Sub": "CSAT", "Top": "Comprehension: English Passage Reading & Vocabulary."},
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
        st.success("Full Syllabus Deployed! Go to Dashboard now."); st.rerun()