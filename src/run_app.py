# run_app.py
import os
import subprocess
import sys
import webbrowser
import threading
import time
import socket

# Function to open the web browser
def open_browser():
    webbrowser.open_new("http://localhost:8501")

# Function to check if the server is running
def is_server_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8501))
    sock.close()
    return result == 0

# Start a thread to open the browser after the server is confirmed to be running
def start_browser_thread():
    while not is_server_running():
        time.sleep(1)
    open_browser()

threading.Thread(target=start_browser_thread).start()

# Run the Streamlit app
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])