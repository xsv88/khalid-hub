import streamlit as st
import requests
import datetime
import psutil
import json
import os

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="Khalid Hub", layout="wide")
TASK_FILE = "tasks.json"
SCHEDULE_FILE = "schedule.json"

# --- 2. DATA LOADING FUNCTIONS ---
def load_json_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

# --- 3. PRAYER API LOGIC ---
def get_prayers():
    # API for Dammam, KSA
    url = "http://api.aladhan.com/v1/timingsByCity?city=Dammam&country=Saudi+Arabia&method=4"
    try:
        r = requests.get(url)
        return r.json()['data']['timings']
    except:
        return None

def get_next_prayer(timings):
    now = datetime.datetime.now()
    prayer_order = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    for p in prayer_order:
        p_time = datetime.datetime.strptime(timings[p], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day)
        if p_time > now:
            diff = p_time - now
            return p, timings[p], diff
    return "Fajr tomorrow", timings["Fajr"], None

# --- 4. SIDEBAR: TASK MANAGER ---
st.sidebar.title("📌 Task Manager")
tasks_data = load_json_data(TASK_FILE)
tasks = tasks_data if isinstance(tasks_data, list) else []

new_task = st.sidebar.text_input("New Task:")
if st.sidebar.button("Add") and new_task:
    tasks.append({"item": new_task, "done": False})
    save_tasks(tasks)
    st.rerun()

for i, t in enumerate(tasks):
    st.sidebar.checkbox(t["item"], key=f"task_{i}")

# --- 5. MAIN DASHBOARD UI ---
st.title("🚀 Khalid's Smart Hub")
st.subheader(f"Dammam | {datetime.datetime.now().strftime('%A, %d %B %Y')}")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("🕌 Prayer Times & Countdown")
    timings = get_prayers()
    if timings:
        next_name, next_time, time_diff = get_next_prayer(timings)
        
        if time_diff:
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            st.success(f"**Next:** {next_name} at {next_time} (Remaining: {hours}h {minutes}m)")
        
        # Display all prayers in a grid
        p_cols = st.columns(5)
        prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
        for i, p in enumerate(prayers):
            p_cols[i].metric(p, timings[p])
    
    st.divider()
    
    # --- 6. SCHEDULE SECTION ---
    st.header("📅 Tomorrow's Academic Schedule")
    # Determine tomorrow's day name
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
    schedule = load_json_data(SCHEDULE_FILE)
    
    if tomorrow in schedule:
        st.write(f"Classes for **{tomorrow}**:")
        for lecture in schedule[tomorrow]:
            st.info(lecture)
    else:
        st.write(f"🎉 No classes scheduled for {tomorrow}. Enjoy your day!")

with col2:
    st.header("🖥️ System Monitor")
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    st.metric("CPU Usage", f"{cpu}%")
    st.progress(cpu / 100)
    
    st.metric("RAM Usage", f"{ram}%")
    st.progress(ram / 100)
    
    # Temperature (Works on Linux/RPi)
    try:
        temp_data = os.popen("vcgencmd measure_temp").readline()
        st.write(f"🌡️ **CPU Temp:** {temp_data.replace('temp=','')}")
    except:
        pass


# --- 7. WEATHER SECTION ---
    st.divider()
    st.header("🌤️ Dammam Weather")
    
    def get_weather():
        try:
            # Fetching weather for Dammam in a simpler way
            response = requests.get("https://wttr.in/Dammam?format=j1")
            data = response.json()['current_condition'][0]
            return {
                'temperature': data['temp_C'],
                'humidity': data['humidity'],
                'description': data['weatherDesc'][0]['value']
            }
        except:
            return None

    weather = get_weather()
    if weather:
        st.metric("Temperature", f"{weather['temperature']} °C")
        st.write(f"💧 **Humidity:** {weather['humidity']}%")
        st.write(f"☁️ **Condition:** {weather['description']}")