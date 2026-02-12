import streamlit as st
import pandas as pd
import datetime
import sqlite3

# --- DATABASE SETUP ---
conn = sqlite3.connect('ukpsc_prep.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, topic TEXT, status TEXT)')

# --- UI CONFIG ---
st.set_page_config(page_title="UKPSC Sentinel Agent", layout="wide")
st.title("🏔️ UKPSC Prep Command Center")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Daily Briefing", "Task Manager"])

# --- 1. DASHBOARD PAGE ---
if page == "Dashboard":
    st.subheader(f"Today's Session: 10:00 PM - 02:00 AM")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🎯 Current Focus: Indian Polity & Uttarakhand Geography")
        st.write("Countdown to Mains: **July 5, 2026**")
    
    with col2:
        st.success("✅ Tasks Completed Today: 0")
        st.warning("🟡 Tasks Pending: 3")

# --- 2. DAILY BRIEFING PAGE ---
elif page == "Daily Briefing":
    st.header("🗞️ Top 10 News Briefing")
    # Mock data - In a real app, this would be a function call to a scraper
    news = [
        "₹3,300 Cr Sharda River Corridor project launched in Champawat.",
        "1 Year of UCC: CM reports zero 'halala' cases.",
        "US Nagar rolls out AI-based grievance system.",
        "Ban on digital devices inside Char Dham temples.",
        "Asan Conservation Reserve: 5,000 birds recorded.",
        "UK & Germany sign pact for tech cooperation.",
        "India named 'Country of the Year' at BIOFACH 2026.",
        "16th Finance Commission retains State tax share at 41%.",
        "World Radio Day 2026: Focus on Himalayan communication.",
        "New organic farming clusters announced for Almora."
    ]
    for i, item in enumerate(news, 1):
        st.write(f"**{i}.** {item}")

# --- 3. TASK MANAGER PAGE ---
elif page == "Task Manager":
    st.header("📝 UKPSC Planner")
    
    new_task = st.text_input("Add a new task (e.g., Read Chand Dynasty)")
    if st.button("Add Task"):
        c.execute('INSERT INTO tasks (topic, status) VALUES (?, ?)', (new_task, 'Pending'))
        conn.commit()
    
    # Show Tasks
    data = pd.read_sql_query('SELECT * FROM tasks', conn)
    st.dataframe(data, use_container_width=True)