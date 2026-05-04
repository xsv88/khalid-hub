import streamlit as st
import psutil
import datetime
import requests

# Page Configuration
st.set_page_config(page_title="Khalid's Hub", layout="wide")

# Sidebar - Task Manager
st.sidebar.title("📌 Task Manager")
new_task = st.sidebar.text_input("Add a new task:")
if st.sidebar.button("Add"):
    st.sidebar.success(f"Task added: {new_task}")

# Main Header
st.title("🚀 Khalid's Personal Hub")
st.write(f"Dammam, Saudi Arabia | {datetime.date.today().strftime('%A, %d %B %Y')}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("🕌 Prayer Times")
    # Using Aladhan API for Dammam
    try:
        r = requests.get("http://api.aladhan.com/v1/timingsByCity?city=Dammam&country=Saudi+Arabia&method=4")
        times = r.json()['data']['timings']
        st.write(f"Fajr: **{times['Fajr']}**")
        st.write(f"Dhuhr: **{times['Dhuhr']}**")
        st.write(f"Asr: **{times['Asr']}**")
        st.write(f"Maghrib: **{times['Maghrib']}**")
        st.write(f"Isha: **{times['Isha']}**")
    except:
        st.error("Check internet connection for prayer times.")

with col2:
    st.header("🖥️ System Monitor")
    cpu_usage = psutil.cpu_percent()
    st.metric("CPU Usage", f"{cpu_usage}%")
    st.progress(cpu_usage / 100)
    
    # Simple Logic for Tomorrow's Classes
    st.subheader("📚 Tomorrow's Schedule")
    st.write("- Information Systems Analysis")
    st.write("- Network Security Lab")