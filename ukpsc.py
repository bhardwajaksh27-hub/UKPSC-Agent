import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import calendar

# 1. DATABASE ENGINE (Hard Persistence)
DB_FILE = "ukpsc_permanent_storage.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "start_date": "2026-02-13",
        "attendance": {}, # Date: {start, stop, breaks: []}
        "notes": {},      # Topic: Text
        "resources": {},  # Topic: String of links
        "carry_over_count": 0
    }

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
    st.cache_data.clear()

db = load_db()

# 2. THE FULL 60-WORKING-DAY SYLLABUS
FULL_SYLLABUS = [
    {"Day": 1, "Sub": "History", "Top": "Harappa: Town Planning, Seals, Trade. Vedic: Early/Later, Rivers."},
    {"Day": 2, "Sub": "History", "Top": "16 Mahajanapadas & Magadh Rise. Jainism & Buddhism Councils."},
    {"Day": 3, "Sub": "History", "Top": "Mauryas: Admin & Ashoka's Dhamma. Post-Mauryan: Kushanas."},
    {"Day": 4, "Sub": "History (UK)", "Top": "Ancient UK: Kuninda (Amoghbhuti coins), Yaudheya, Katyuri Admin."},
    {"Day": 5, "Sub": "History", "Top": "Guptas: Golden Age. Harshavardhana & South Dynasties."},
    {"Day": 6, "Sub": "History", "Top": "Delhi Sultanate: Slave to Lodi. Market Reforms & Architecture."},
    {"Day": 7, "Sub": "REVISION", "Top": "Mock 1: Ancient & Medieval Comprehensive Revision."},
    {"Day": 8, "Sub": "History (UK)", "Top": "Medieval UK: Chand Dynasty (Kumaon), Parmar (Garhwal). Gorkha Rule."},
    {"Day": 9, "Sub": "History", "Top": "Modern: European Arrival, Battle of Plassey/Buxar. Land Revenue."},
    {"Day": 10, "Sub": "History", "Top": "1857 Revolt: UK's Role. Socio-Religious Reforms: Brahmo & Arya Samaj."},
    {"Day": 11, "Sub": "History (UK)", "Top": "Modern UK: Sugauli Treaty, British Admin, Coolie Begar Movement."},
    {"Day": 12, "Sub": "History", "Top": "National Mov: Gandhi Era (Non-Coop, Civil Dis, Quit India)."},
    {"Day": 13, "Sub": "History (UK)", "Top": "UK Statehood: Tehri Merger, 1994 Muzaffarnagar Kand, Formation 2000."},
    {"Day": 14, "Sub": "REVISION", "Top": "Mock 2: Modern History & UK Statehood Mastery."},
    {"Day": 15, "Sub": "Geo (World)", "Top": "Solar System, Lithosphere: Rocks. Atmosphere: Layers, Winds."},
    {"Day": 16, "Sub": "Geo (World)", "Top": "Hydrosphere: Ocean Relief, Currents, Tides, Salinity."},
    {"Day": 17, "Sub": "Geo (India)", "Top": "Relief: Himalayas, Plains, Peninsula. Climate: Monsoon."},
    {"Day": 18, "Sub": "Geo (India)", "Top": "Drainage: Himalayan vs Peninsular Rivers. Soils, Vegetation."},
    {"Day": 19, "Sub": "Geo (UK)", "Top": "UK Relief: Glaciers, River Systems (Ganga, Yamuna, Kali)."},
    {"Day": 20, "Sub": "Geo (UK)", "Top": "Resources: UK Forest Policy, Jim Corbett Park, 2011 Census."},
    {"Day": 21, "Sub": "REVISION", "Top": "Mock 3: World, India & UK Geography."},
    {"Day": 22, "Sub": "Polity", "Top": "Constitution: Preamble, Rights, DPSP & Duties. Amendments."},
    {"Day": 23, "Sub": "Polity", "Top": "Parliament: President, PM, Committees. Judiciary: SC/HC Writs."},
    {"Day": 24, "Sub": "Polity", "Top": "Bodies: Election Comm, CAG, UPSC, Lokpal. Federalism."},
    {"Day": 25, "Sub": "Polity (UK)", "Top": "UK Admin: Governor, CM, Legislative Assembly. Secretariat."},
    {"Day": 26, "Sub": "Polity (UK)", "Top": "Local Gov: 73rd/74th Amnds. UK Panchayati Raj Act."},
    {"Day": 27, "Sub": "Polity", "Top": "Public Policy: Welfare Schemes, Human Rights, Citizen's Charter."},
    {"Day": 28, "Sub": "REVISION", "Top": "Mock 4: Indian Polity & UK Governance."},
    {"Day": 29, "Sub": "Economy", "Top": "Indian Economy Features, NITI Aayog. LPG Reforms 1991."},
    {"Day": 30, "Sub": "Economy", "Top": "Banking: RBI (Monetary Policy), SEBI, NABARD. Stock Markets."},
    {"Day": 31, "Sub": "Economy", "Top": "Public Finance: Budget, GST, Finance Commission. Poverty."},
    {"Day": 32, "Sub": "Economy (UK)", "Top": "UK Economy: Per Capita Income, Budget. Tourism Policy."},
    {"Day": 33, "Sub": "Economy (UK)", "Top": "Agriculture in UK: Horticulture, MSME Policy."},
    {"Day": 34, "Sub": "Economy", "Top": "SDG Goals, HDI Index, WTO & IMF."},
    {"Day": 35, "Sub": "REVISION", "Top": "Mock 5: Economy (India & UK)."},
    {"Day": 36, "Sub": "Science", "Top": "Physics: Light, Sound, Nuclear. Chemistry: Acids/Bases."},
    {"Day": 37, "Sub": "Science", "Top": "Biology: Cell, Genetics, Human Systems (Circulation)."},
    {"Day": 38, "Sub": "Science", "Top": "ICT: E-Governance, Internet, Cyber Security. ISRO."},
    {"Day": 39, "Sub": "Science", "Top": "Environment: Ecology, Food Chain, Biodiversity (UK)."},
    {"Day": 40, "Sub": "Science (UK)", "Top": "Disaster Mgmt: Earthquakes/Landslides, SDMA."},
    {"Day": 41, "Sub": "Science", "Top": "Space & Defense: Nuclear Power, DRDO, Tech Updates."},
    {"Day": 42, "Sub": "REVISION", "Top": "Mock 6: General Science & Tech."},
    {"Day": 43, "Sub": "Culture (UK)", "Top": "UK Tribes: Bhotia, Tharu, Jaunsari. Folk Art, Music."},
    {"Day": 44, "Sub": "Culture (UK)", "Top": "Fairs & Festivals: Nanda Devi, Kumbh. Panch Kedar/Badri."},
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

# 3. DATE LOGIC (The Sunday-Skipper)
def get_working_date(target_day, start_str, carry_count):
    curr = datetime.strptime(start_str, "%Y-%m-%d")
    days_found = 0
    total_needed = target_day + carry_count
    
    loop_date = curr
    while days_found < total_needed:
        if loop_date.weekday() != 6: # Skip Sunday
            days_found += 1
        if days_found < total_needed:
            loop_date += timedelta(days=1)
    return loop_date

# 4. APP INTERFACE
st.set_page_config(page_title="UKPSC Sentinel", layout="wide")
st.sidebar.title("🏔️ Sentinel Command")
nav = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 60-Day Roadmap", "📚 Digital Library", "📝 Study Notes", "⚙️ Engine Room"])

today_dt = datetime.now()
today_str = today_dt.strftime("%Y-%m-%d")

# --- DASHBOARD ---
if nav == "📊 Dashboard":
    st.title("🏔️ UKPSC Sentinel Dashboard")
    
    # Calendar Highlight
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("📅 Calendar")
        cal = calendar.monthcalendar(today_dt.year, today_dt.month)
        cols = st.columns(7)
        for i, d in enumerate(["M", "T", "W", "T", "F", "S", "S"]): cols[i].write(f"**{d}**")
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0: cols[i].write(" ")
                elif day == today_dt.day: cols[i].markdown(f":red[**{day}**]")
                else: cols[i].write(str(day))

    # Attendance Engine (Stopwatch Style)
    with c2:
        st.subheader("⏱️ Session Logs")
        if today_str not in db["attendance"]:
            db["attendance"][today_str] = {"start": None, "stop": None, "breaks": []}
        
        att = db["attendance"][today_str]
        col_a, col_b, col_c = st.columns(3)
        
        if col_a.button("▶️ Start"):
            att["start"] = datetime.now().strftime("%I:%M %p")
            save_db(db); st.rerun()
            
        if col_b.button("⏸️ Break"):
            if len(att["breaks"]) < 5:
                att["breaks"].append(datetime.now().strftime("%I:%M %p"))
                save_db(db); st.rerun()
            else: st.warning("Limit: 5 Breaks")
            
        if col_c.button("⏹️ Stop"):
            att["stop"] = datetime.now().strftime("%I:%M %p")
            save_db(db); st.rerun()
            
        st.write(f"**Session:** {att['start'] or '--'} to {att['stop'] or '--'}")
        if att["breaks"]: st.write(f"**Breaks:** {', '.join(att['breaks'])}")

    st.divider()

    # Current Task
    # Logic: Find which working day today is
    start_dt = datetime.strptime(db["start_date"], "%Y-%m-%d")
    current_working_day = 0
    temp_date = start_dt
    while temp_date.date() <= today_dt.date():
        if temp_date.weekday() != 6: current_working_day += 1
        temp_date += timedelta(days=1)
    
    target_idx = current_working_day - db["carry_over_count"]
    if 1 <= target_idx <= 60:
        task = FULL_SYLLABUS[target_idx-1]
        st.info(f"🚩 **Current Duty: Working Day {target_idx}**")
        st.header(f"{task['Sub']}: {task['Top']}")
        
        # Sub-series Resources (a, b, c)
        res_str = db["resources"].get(task['Top'], "")
        links = [l.strip() for l in res_str.split(",") if "http" in l]
        if links:
            st.write("### 📖 Resources")
            for i, l in enumerate(links): st.link_button(f"({chr(97+i)}) {l[:30]}...", l)
        
        if st.button("⏭️ Carry Over (Topic Unfinished)"):
            db["carry_over_count"] += 1
            save_db(db); st.success("Schedule Shifted!"); st.rerun()
    else:
        st.success("Sunday Break or Course Complete!")

    # Upcoming Agenda Table at Bottom
    st.divider()
    st.subheader("📋 Upcoming Agenda")
    agenda = []
    for i in range(target_idx, target_idx + 7):
        if i <= 60:
            d = get_working_date(i, db["start_date"], db["carry_over_count"])
            agenda.append({"Day": i, "Date": d.strftime("%d %b"), "Topic": FULL_SYLLABUS[i-1]["Top"]})
    st.table(agenda)

# --- ROADMAP ---
elif nav == "📅 60-Day Roadmap":
    st.title("📅 Master 60-Working-Day Marathon")
    roadmap = []
    for i in range(1, 61):
        dt = get_working_date(i, db["start_date"], db["carry_over_count"])
        roadmap.append({
            "Working Day": i,
            "Calendar Date": dt.strftime("%Y-%m-%d (%a)"),
            "Subject": FULL_SYLLABUS[i-1]["Sub"],
            "Topic": FULL_SYLLABUS[i-1]["Top"]
        })
    st.dataframe(roadmap, use_container_width=True, hide_index=True)

# --- DIGITAL LIBRARY ---
elif nav == "📚 Digital Library":
    st.title("📚 Repository & Persistence")
    topic_list = [t["Top"] for t in FULL_SYLLABUS]
    target = st.selectbox("Assign resource to:", topic_list)
    new_url = st.text_input("Paste URL:")
    if st.button("💾 Store Link"):
        curr = db["resources"].get(target, "")
        db["resources"][target] = f"{curr}, {new_url}" if curr else new_url
        save_db(db); st.success("Saved to Repository!")
    
    st.divider()
    for top, urls in db["resources"].items():
        with st.expander(f"📚 {top}"):
            for l in urls.split(","): st.write(l.strip())

# --- STUDY NOTES ---
elif nav == "📝 Study Notes":
    st.title("📝 Persistent Notes")
    target = st.selectbox("Topic:", [t["Top"] for t in FULL_SYLLABUS])
    note_val = db["notes"].get(target, "")
    txt = st.text_area("High-Yield Points:", value=note_val, height=400)
    if st.button("💾 Sync Notes"):
        db["notes"][target] = txt
        save_db(db); st.success("Cloud-Synced!")

# --- ENGINE ROOM ---
elif nav == "⚙️ Engine Room":
    st.title("⚙️ Engine Room")
    st.write("System Status: **Active**")
    st.write(f"Database File: `{DB_FILE}`")
    if st.button("🧹 Factory Reset (Caution!)"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.cache_data.clear()
        st.rerun()