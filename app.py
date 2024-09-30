import streamlit as st
import time
from datetime import datetime
import random
import threading

# Set page configuration
st.set_page_config(page_title="Offline AV Pipeline", layout="wide")

# Custom CSS for improved UI with a darker grey background and enhanced UI elements
st.markdown("""
    <style>
        .stApp {
            background-color: #212121; /* Dark grey background */
        }
        .stProgress > div > div > div > div {
            background-color: #4CAF50; /* Progress bar color */
        }
        .stButton > button {
            background-color: #4CAF50; /* Button background color */
            color: white; /* Button text color */
            border-radius: 5px; /* Rounded corners for buttons */
        }
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
            color: #2c3e50; /* Dark grey text */
        }
        .card, .safe-card, .threat-card {
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for cards */
            padding: 20px;
            background-color: white;
            margin-bottom: 10px;
        }
        .threat-card {
            background-color: #ff6b6b; /* Red for threat card */
            color: white;
        }
        .safe-card {
            background-color: #4CAF50; /* Green for safe card */
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Function to display metrics in cards
def display_metric_card(col, label, value):
    with col:
        st.markdown(f"<div class='card'><p class='big-font'>{label}</p></div>", unsafe_allow_html=True)
        st.metric(label, value)

# Function to simulate AV engine scan
def simulate_av_scan(engine_name, progress_bar, engine_metric, file_metric, quick=False):
    files_scanned = 0
    threats_detected = 0
    max_files = 1000 if quick else 10000

    for i in range(100):
        time.sleep(random.uniform(0.05, 0.1))  # Simulating varied scan time
        files_scanned += max_files // 100
        if random.random() < 0.05:  # 5% chance of detecting a threat
            threats_detected += 1
        
        # Update AV engine progress bar, files scanned, and threats detected
        progress_bar.progress(i + 1)
        file_metric.text(f"{engine_name} Files Scanned: {files_scanned}")
        engine_metric.metric(f"{engine_name} Threats Detected", threats_detected)

# Function to run parallel AV engine scans
def perform_parallel_scan(quick=False):
    # Create columns for AV engines
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='safe-card'>Windows Defender</div>", unsafe_allow_html=True)
        defender_progress = st.progress(0)
        defender_metric = st.empty()
        defender_file_metric = st.empty()  # For showing number of files scanned
    
    with col2:
        st.markdown("<div class='safe-card'>Trend Micro</div>", unsafe_allow_html=True)
        trend_progress = st.progress(0)
        trend_metric = st.empty()
        trend_file_metric = st.empty()  # For showing number of files scanned

    with col3:
        st.markdown("<div class='safe-card'>Eset Security</div>", unsafe_allow_html=True)
        eset_progress = st.progress(0)
        eset_metric = st.empty()
        eset_file_metric = st.empty()  # For showing number of files scanned
    
    # Create threads for each AV engine
    defender_thread = threading.Thread(target=simulate_av_scan, args=("Windows Defender", defender_progress, defender_metric, defender_file_metric, quick))
    trend_thread = threading.Thread(target=simulate_av_scan, args=("Trend Micro", trend_progress, trend_metric, trend_file_metric, quick))
    eset_thread = threading.Thread(target=simulate_av_scan, args=("Eset Security", eset_progress, eset_metric, eset_file_metric, quick))

    # Start threads
    defender_thread.start()
    trend_thread.start()
    eset_thread.start()

    # Wait for all threads to complete
    defender_thread.join()
    trend_thread.join()
    eset_thread.join()

    st.success("All AV scans completed!")

# Sidebar for actions
st.sidebar.image("https://img.icons8.com/color/96/000000/shield.png", width=100)
st.sidebar.title("Offline AV")
scan_button = st.sidebar.button("Start Full Scan")
quick_scan_button = st.sidebar.button("Quick Scan")
update_button = st.sidebar.button("Update Virus Definitions")

# Main content title
st.title("Offline AV Pipeline Antivirus Dashboard")

# Create three columns for file metrics
col1, col2, col3 = st.columns(3)
files_scanned_metric = col1.empty()
threats_detected_metric = col2.empty()
last_scan_metric = col3.empty()

# Display placeholder metrics initially
display_metric_card(col1, "Files Scanned", 0)
display_metric_card(col2, "Threats Detected", 0)
display_metric_card(col3, "Last Scan", "Never")

# Recent threats section
st.subheader("Recent Threats")
threat_list = st.empty()  # Will populate this after scan

# System status section
st.subheader("System Status")
cols = st.columns(3)
cols[0].markdown("<div class='safe-card'>Real-time Protection: Active</div>", unsafe_allow_html=True)
cols[1].markdown("<div class='safe-card'>Firewall: Enabled</div>", unsafe_allow_html=True)
cols[2].markdown("<div class='safe-card'>Virus Definitions: Up to date</div>", unsafe_allow_html=True)

# Additional protection checkboxes
st.subheader("Additional Protection")
cols = st.columns(2)
with cols[0]:
    st.checkbox("Enable Web Shield", value=True)
    st.checkbox("Enable Email Shield", value=True)
    st.checkbox("Enable Behavior Shield", value=True)
with cols[1]:
    st.checkbox("Enable Ransomware Protection", value=True)
    st.checkbox("Enable Webcam Protection", value=False)
    st.checkbox("Enable Data Shredder", value=False)

# System performance
st.subheader("System Performance")
cpu_usage = random.randint(1, 100)
memory_usage = random.randint(1, 100)

st.progress(cpu_usage / 100)
st.text(f"CPU Usage: {cpu_usage}%")
st.progress(memory_usage / 100)
st.text(f"Memory Usage: {memory_usage}%")

# Check if scan buttons are pressed and trigger parallel AV scans
if scan_button:
    st.warning("Full Scan in Progress...")
    perform_parallel_scan()
    st.success("Full Scan Completed!")

if quick_scan_button:
    st.info("Quick Scan in Progress...")
    perform_parallel_scan(quick=True)
    st.success("Quick Scan Completed!")

# Update virus definitions
if update_button:
    with st.spinner("Updating virus definitions..."):
        time.sleep(2)  # Simulate update time
    st.success("Virus definitions updated successfully!")