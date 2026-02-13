import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# --- 1. DATA PERSISTENCE LAYER ---
DATA_FILE = "ukpsc_study_vault.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "current_day": 1,
        "shift_days": 0,
        "logs": [],
        "notes": {},  
        "is_active": False,
        "start_time": None
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# --- 2. FULL 60-WORKING-DAY SYLLABUS ---
# Comprehensive UKPSC Prelims + Mains Syllabus
syllabus = [
    # ANCIENT & MEDIEVAL HISTORY
    "Day 1: Harappan Civilization - Town Planning, Seals, Trade & Urbanism (NCERT/NIOS Focus)",
    "Day 2: Vedic Age - Early vs Later Vedic Society, Rivers, Sabha/Samiti & Political Shift",
    "Day 3: Mahajanapadas, Buddhism & Jainism - Philosophy, Councils & Impact",
    "Day 4: Mauryan Empire - Administration, Ashokan Edicts & Mauryan Art",
    "Day 5: Post-Mauryan (Kushanas/Satvahanas) & Gupta Golden Age - Science & Literature",
    "Day 6: Early Medieval India - Harshavardhana, Cholas & Arrival of Islam",
    "Day 7: Delhi Sultanate - Administration, Market Reforms (Alauddin) & Architecture",
    "Day 8: Mughal Empire - Akbar's Mansabdari, Land Revenue & Cultural Synthesis",
    "Day 9: Maratha Empire - Shivaji's Administration (Ashtapradhan) & Decline of Mughals",
    # MODERN HISTORY
    "Day 10: British Expansion - Plassey, Buxar & Subsidiary Alliance/Doctrine of Lapse",
    "Day 11: 1857 Revolt - Causes, Nature & Impact in Uttarakhand (Kalu Mahara)",
    "Day 12: Social-Religious Reform Movements (Raja Ram Mohan Roy, Dayanand Saraswati)",
    "Day 13: Indian National Congress - Moderate Phase & Extremist Rise (1885-1905)",
    "Day 14: Gandhian Era I - NCM, Khilafat & Civil Disobedience Movement",
    "Day 15: Gandhian Era II - Quit India Movement, INA & Partition/Independence",
    # UTTARAKHAND SPECIAL (HISTORY & CULTURE)
    "Day 16: UK Special - Ancient Tribes (Kunindas, Yaudheyas) & Katyuri Dynasty",
    "Day 17: UK Special - Chand Dynasty (Kumaon) & Parmar Dynasty (Garhwal)",
    "Day 18: UK Special - Gorkha Rule (1790-1815) & British Kumaon/Garhwal Administration",
    "Day 19: UK Special - Uttarakhand Freedom Struggle & Statehood Movement",
    "Day 20: UK Special - Culture, Festivals, Folk Art & Tribes of Uttarakhand",
    # GEOGRAPHY (INDIA & WORLD)
    "Day 21: Physical Geography - Himalayas, Indo-Gangetic Plains & Peninsular Plateau",
    "Day 22: Climate - Indian Monsoon, Jet Streams & Western Disturbances",
    "Day 23: Drainage System - Himalayan Rivers (Ganga, Yamuna) vs Peninsular Rivers",
    "Day 24: Soil, Natural Vegetation & Agriculture in India",
    "Day 25: World Geography - Latitudes, Longitudes & Major Continents/Oceans",
    # UTTARAKHAND GEOGRAPHY
    "Day 26: UK Geography - River Systems (Alaknanda, Bhagirathi, Kali, Yamuna)",
    "Day 27: UK Geography - Glaciers, Mountain Peaks & Lakes of Uttarakhand",
    "Day 28: UK Geography - Disaster Management (Landslides, Flash Floods, Earthquake zones)",
    "Day 29: UK Geography - Forests, Wildlife (National Parks) & Mineral Resources",
    # POLITY & CONSTITUTION
    "Day 30: Constitutional Framework - Preamble, Citizenship & FRs/DPSPs/FDs",
    "Day 31: Union Executive - President, VP, PM & Council of Ministers",
    "Day 32: Parliament - Composition, Sessions, Bills & Committees",
    "Day 33: State Government - Governor, CM & State Legislature (Special UK focus)",
    "Day 34: Judiciary - Supreme Court, High Court & PIL/Judicial Activism",
    "Day 35: Local Governance - 73rd/74th Amendments & Panchayati Raj in Hills",
    "Day 36: Constitutional & Non-Constitutional Bodies (Election Commission, UPSC, UKPSC)",
    # ECONOMY
    "Day 37: Basic Economics - National Income, Inflation, Banking & Monetary Policy",
    "Day 38: Fiscal Policy - Budgeting Process, GST & Financial Relations",
    "Day 39: UK Economy - Tourism (Chardham), Horticulture & Hydro-power potential",
    "Day 40: UK Economy - Migration (Palayan) Issues & MSME Sector in Hills",
    # GENERAL SCIENCE & ENVIRONMENT
    "Day 41: Physics - Optics, Sound, Electricity & Nuclear Energy",
    "Day 42: Chemistry - Carbon, Polymers, Acids/Bases & Everyday Chemistry",
    "Day 43: Biology - Cell Structure, Human Systems, Nutrition & Diseases",
    "Day 44: Environment - Biodiversity, Climate Change & Himalayan Ecology",
    "Day 45: Tech - Space, Defense, Biotechnology & IT in Governance",
    # ETHICS (MAINS PAPER VI)
    "Day 46: Ethics - Human Values, Attitude & Aptitude for Civil Services",
    "Day 47: Emotional Intelligence - Concept & Application in Administration",
    "Day 48: Probity in Governance - RTI, Citizen Charters & Code of Ethics",
    "Day 49: Ethics Case Studies - Ethical Dilemmas in Public Service",
    # INTERNATIONAL RELATIONS & CURRENT AFFAIRS
    "Day 50: IR - India & Neighbors (Focus on Nepal Border & China Policy)",
    "Day 51: Global Groups - UN, G20, BRICS, SCO & QUAD",
    "Day 52: UK Current Affairs - State Govt Schemes & Current Budget Highlights",
    "Day 53: National/International Current Affairs Compilation",
    # REVISION & MOCKS
    "Day 54: Revision - Ancient & Medieval History + UK History",
    "Day 55: Revision - Modern History + Indian Polity",
    "Day 56: Revision - Geography (India/World) + UK Geography",
    "Day 57: Revision - Economy + Science/Environment",
    "Day 58: Mock Test 01 - General Studies Paper I (Prelims Style)",
    "Day 59: Mock Test 02 - CSAT & Ethics (Mains Paper VI)",
    "Day 60: Final Revision & Strategy Review"
]

# --- 3. DATE & CALENDAR LOGIC ---
def get_date(working_day_num, shift):
    """Calculates date by skipping Sundays and adding carry-over shifts."""
    start_date = datetime(2026, 2, 16) # Reference start: Feb 16, 2026 (Monday)
    current_date = start_date
    count = 0
    target = working_day_num + shift
    
    while count < target:
        if current_date.weekday() != 6: # Skip Sundays
            count += 1
        if count < target:
            current_date += timedelta(days=1)
    return current_date

# --- 4. APP INTERFACE ---
st.set_page_config(page_title="UKPSC Warrior ERP", layout="wide")

# Sidebar: Monthly Calendar Dashboard
with st.sidebar:
    st.header("🗓️ Dashboard")
    today = datetime.now()
    st.write(f"**Today:** {today.strftime('%A, %d %b %Y')}")
    st.write(f"**Current Study Day:** {data['current_day']}")
    
    # Visual Monday-Start Table (Simplified representation)
    st.markdown("---")
    st.write("**Feb/Mar 2026 Grid**")
    st.caption("M T W T F S [S]")
    # Highlight logic
    st.markdown(f"<h1 style='color: #FF4B4B; text-align: center;'>DAY {data['current_day']}</h1>", unsafe_allow_html=True)
    st.progress(data['current_day'] / 60)

# Main Body
st.title("🏹 UKPSC 60-Working-Day Planner")

# TOP SECTION: Attendance & Carry Over
cur_day = data["current_day"]
st.subheader(f"📖 Active Topic: {syllabus[cur_day-1]}")

col1, col2, col3, col4 = st.columns(4)

if col1.button("▶️ Start Session"):
    data["is_active"] = True
    data["start_time"] = datetime.now().strftime("%I:%M %p")
    save_data(data)
    st.rerun()

if col2.button("⏹️ Stop (Record Break)"):
    # Limit to 5 breaks logic
    today_logs = [l for l in data["logs"] if l["day"] == cur_day]
    if data["is_active"] and len(today_logs) < 5:
        stop_time = datetime.now().strftime("%I:%M %p")
        data["logs"].append({
            "day": cur_day,
            "start": data["start_time"],
            "stop": stop_time,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        data["is_active"] = False
        data["start_time"] = None
        save_data(data)
        st.rerun()
    elif len(today_logs) >= 5:
        st.error("Max 5 break segments reached for today.")

if col3.button("🔄 Carry Over Topic"):
    data["shift_days"] += 1
    save_data(data)
    st.warning("Topic not finished. Schedule shifted by +1 Working Day.")
    st.rerun()

if col4.button("✅ Mark Day Complete"):
    data["current_day"] += 1
    save_data(data)
    st.success("Moving to next day!")
    st.rerun()

# ATTENDANCE LOGS DISPLAY
active_logs = [l for l in data["logs"] if l["day"] == cur_day]
if active_logs:
    with st.expander("🕒 View Today's Study Segments"):
        for i, log in enumerate(active_logs):
            st.write(f"**Segment {i+1}:** {log['start']} to {log['stop']}")

# --- 5. STUDY NOTES SECTION ---
st.divider()
st.subheader("📝 NCERT & NIOS Study Vault")
current_note_key = str(cur_day)
saved_note = data["notes"].get(current_note_key, "")

note_content = st.text_area(
    f"Draft your notes for Day {cur_day} (e.g., Harappan Town Planning or Vedic Rivers):",
    value=saved_note,
    height=250,
    placeholder="Paste your summaries from NCERT Class 12 and NIOS here..."
)

if st.button("💾 Save My Notes"):
    data["notes"][current_note_key] = note_content
    save_data(data)
    st.toast("Notes saved successfully!")

# --- 6. DYNAMIC ROADMAP TABLE ---
st.divider()
st.subheader("🗓️ Personalized Roadmap (Auto-Adjusted)")

roadmap_list = []
for i in range(1, 61):
    actual_date = get_date(i, data["shift_days"])
    status = "✅ Done" if i < data["current_day"] else ("🔥 ACTIVE" if i == data["current_day"] else "⏳ Pending")
    roadmap_list.append({
        "Status": status,
        "Day": i,
        "Date": actual_date.strftime("%d-%m-%Y (%a)"),
        "Syllabus Module": syllabus[i-1]
    })

df = pd.DataFrame(roadmap_list)

# Stylized Display
def color_status(val):
    if val == "🔥 ACTIVE": return 'background-color: #722f37; color: white'
    if val == "✅ Done": return 'color: #888888'
    return ''

st.dataframe(df.style.applymap(color_status, subset=['Status']), use_container_width=True, hide_index=True)

# FOOTER CAPABILITY
st.caption("Note: This system skips Sundays automatically. Using 'Carry Over' pushes all future dates forward without losing your progress history.")