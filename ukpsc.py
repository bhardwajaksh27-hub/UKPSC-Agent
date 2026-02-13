import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# --- 1. STORAGE & REPOSITORY ENGINE ---
DATA_FILE = "ukpsc_permanent_storage.json"

REPOSITORIES = {
    "NCERT_12": "https://ncert.nic.in/textbook.php?fepy1=1-15",
    "NIOS_HISTORY": "https://nios.ac.in/online-course-material/sr-secondary-courses/history-(315).aspx",
    "UKPSC_PYQ": "https://psc.uk.gov.in/previous-year-question-paper"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "current_day": 1,
        "shift_days": 0,
        "logs": [],      # List of {day, start, stop}
        "notes": {},     # Dict of {day_index: text}
        "is_active": False,
        "start_time": None
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# --- 2. THE COMPLETE 60-WORKING-DAY SYLLABUS ---
syllabus = [
    "Day 1: Harappan Civilization - Town Planning, Seals & Trade (NCERT Ch 1)",
    "Day 2: Vedic Age - Early vs Later, Rivers (Sapta-Sindhu) & Sabha/Samiti",
    "Day 3: Mahajanapadas, Buddhism & Jainism - Philosophy & UKPSC PYQs",
    "Day 4: Mauryan Empire - Administration & Ashokan Edicts",
    "Day 5: Gupta Period - Science, Literature & Golden Age",
    "Day 6: Medieval India - Delhi Sultanate (Slave & Khalji Dynasties)",
    "Day 7: Mughal Empire - Administration, Revenue & Architecture",
    "Day 8: Maratha Empire & Rise of Regional Powers",
    "Day 9: British Expansion - Plassey to Buxar & Land Revenue Policy",
    "Day 10: 1857 Revolt - Impact in Uttarakhand (Kalu Mahara's Role)",
    "Day 11: INC Formation & Moderate vs Extremist phase",
    "Day 12: Gandhian Era - NCM, CDM & Quit India Movement",
    "Day 13: UK Special History - Katyuri & Chand Dynasties",
    "Day 14: UK Special History - Parmar Dynasty & Gorkha Rule",
    "Day 15: UK Special History - British Rule & Statehood Movement",
    "Day 16: Geography - Physical Features of India (Himalayas & Plains)",
    "Day 17: Geography - Drainage Systems (Ganga, Yamuna, Brahmaputra)",
    "Day 18: Geography - Climate, Monsoons & Western Disturbances",
    "Day 19: UK Geography - Rivers (Alaknanda, Bhagirathi, Kali)",
    "Day 20: UK Geography - Glaciers, Lakes & Natural Disasters",
    "Day 21: Polity - Preamble, Fundamental Rights & DPSPs",
    "Day 22: Polity - Union Executive (President, PM, Parliament)",
    "Day 23: Polity - Judiciary (SC, HC & Subordinate Courts)",
    "Day 24: Polity - Panchayati Raj & 73rd/74th Amendments",
    "Day 25: Economy - Basic Concepts, GDP, Inflation & Monetary Policy",
    "Day 26: Economy - Budgeting & Fiscal Policy (Central/State)",
    "Day 27: UK Economy - Tourism, Horticulture & Hydro-power",
    "Day 28: UK Economy - Migration (Palayan) & MSME Policy",
    "Day 29: Science - Physics (Light, Sound, Gravity) & PYQs",
    "Day 30: Science - Chemistry (Everyday Life) & Biology (Human Systems)",
    "Day 31: Environment - Biodiversity & Himalayan Ecology",
    "Day 32: Ethics - Human Values & Attitude (Mains Paper VI)",
    "Day 33: Ethics - Emotional Intelligence & Probity in Governance",
    "Day 34: Ethics - Case Studies (Disaster Management Scenarios)",
    "Day 35: International Relations - India & Neighbors (China, Nepal)",
    "Day 36: IR - Global Bodies (UN, G20, BRICS, SCO)",
    "Day 37: UK Special - Culture, Festivals, Tribes & Folk Art",
    "Day 38: UK Special - Important Personalities & Welfare Schemes",
    "Day 39: General Science - Space, Defense & IT in Governance",
    "Day 40: Current Affairs - Uttarakhand State Schemes (Last 1 Year)",
    "Day 41: Current Affairs - National/International (Feb 2025-Feb 2026)",
    "Day 42: Quantitative Aptitude - Number System, Ratio & Proportion",
    "Day 43: Quantitative Aptitude - Percentage, Profit & Loss",
    "Day 44: Reasoning - Coding-Decoding, Blood Relations",
    "Day 45: Reasoning - Syllogism, Seating Arrangement",
    "Day 46: Mains Writing Practice - History & Culture (Paper II)",
    "Day 47: Mains Writing Practice - Polity & IR (Paper III)",
    "Day 48: Mains Writing Practice - Geography (Paper IV)",
    "Day 49: Mains Writing Practice - Economy (Paper V)",
    "Day 50: Mains Writing Practice - Ethics (Paper VI)",
    "Day 51: Revision - Ancient & Medieval History",
    "Day 52: Revision - Modern History & UK History",
    "Day 53: Revision - Geography & Environment",
    "Day 54: Revision - Polity & Governance",
    "Day 55: Revision - Economy & General Science",
    "Day 56: Mock Test - GS Paper I (Prelims)",
    "Day 57: Mock Test - CSAT Paper II (Prelims)",
    "Day 58: Full Length Mock - UK Special Focus",
    "Day 59: Data Interpretation & Chart Analysis",
    "Day 60: Final Strategy & Current Affairs Round-up"
]

# --- 3. THE DATE ENGINE (Mon-Start, Sunday Skip, Carry Over) ---
def get_adjusted_date(day_idx, shift):
    start_date = datetime(2026, 2, 16) # Reference Monday
    curr = start_date
    count = 1
    target = day_idx + shift
    while count < target:
        curr += timedelta(days=1)
        if curr.weekday() != 6: # 6 is Sunday
            count += 1
    return curr

# --- 4. APP INTERFACE ---
st.set_page_config(page_title="UKPSC ERP", layout="wide")
st.title("🛡️ UKPSC 60-Working-Day Master Planner")

# Sidebar: Repositories & Calendar Dashboard
with st.sidebar:
    st.header("📚 Resource Repositories")
    st.link_button("NCERT Class 12", REPOSITORIES["NCERT_12"])
    st.link_button("NIOS History (315)", REPOSITORIES["NIOS_HISTORY"])
    st.link_button("UKPSC PYQ Portal", REPOSITORIES["UKPSC_PYQ"])
    st.divider()
    st.header("📊 Progress Dashboard")
    st.metric("Working Day", f"{data['current_day']}/60")
    st.progress(data['current_day'] / 60)
    st.markdown("---")
    st.caption("M T W T F S [S]")
    st.markdown(f"<h1 style='color:red; text-align:center;'>Day {data['current_day']}</h1>", unsafe_allow_html=True)

# Main Section: Attendance & Attendance HH:MM
cur_day = data["current_day"]
st.subheader(f"Current Module: {syllabus[cur_day-1]}")

col1, col2, col3, col4 = st.columns(4)

if col1.button("▶️ START SESSION"):
    data["is_active"] = True
    data["start_time"] = datetime.now().strftime("%I:%M %p")
    save_data(data)
    st.rerun()

if col2.button("⏹️ STOP (MAX 5)"):
    today_logs = [l for l in data["logs"] if l["day"] == cur_day]
    if data["is_active"] and len(today_logs) < 5:
        stop_time = datetime.now().strftime("%I:%M %p")
        data["logs"].append({"day": cur_day, "start": data["start_time"], "stop": stop_time})
        data["is_active"] = False
        data["start_time"] = None
        save_data(data)
        st.rerun()

if col3.button("🔄 CARRY OVER"):
    data["shift_days"] += 1
    save_data(data)
    st.rerun()

if col4.button("✅ DAY COMPLETE"):
    data["current_day"] += 1
    save_data(data)
    st.rerun()

# Notes & Attendance Display
tab1, tab2 = st.tabs(["📝 Study Notes (NCERT/NIOS)", "🕒 Attendance Logs"])

with tab1:
    key = str(cur_day)
    notes = st.text_area("Record key points for today's topic:", value=data["notes"].get(key, ""), height=300)
    if st.button("💾 Save Progress"):
        data["notes"][key] = notes
        save_data(data)
        st.success("Progress Saved to Local Storage.")

with tab2:
    today_logs = [l for l in data["logs"] if l["day"] == cur_day]
    if not today_logs: st.info("No logs for today yet.")
    for i, log in enumerate(today_logs):
        st.write(f"**Segment {i+1}:** {log['start']} - {log['stop']}")

# Dynamic Roadmap
st.divider()
st.subheader("🗓️ Automated 60-Working-Day Schedule")
roadmap = []
for i in range(1, 61):
    d = get_adjusted_date(i, data["shift_days"])
    status = "✅" if i < data["current_day"] else ("🔥 ACTIVE" if i == data["current_day"] else "⏳")
    roadmap.append({
        "Day": i, 
        "Date": d.strftime("%d-%m-%Y (%a)"), 
        "Syllabus Module": syllabus[i-1], 
        "Status": status
    })

st.table(pd.DataFrame(roadmap))