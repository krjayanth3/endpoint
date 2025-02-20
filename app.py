import os
import subprocess
from datetime import datetime
from flask import Flask
from pytz import timezone
import platform

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Replace with your actual name
    name = "Jayanth K R"

    # Get system username
    try:
        user = os.getlogin()
    except OSError:
        # Fallback for some environments
        user = subprocess.check_output(["whoami"]).decode().strip()

    # Get server time in IST
    ist = timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")

    # Get top/tasklist output (one snapshot)
    system_platform = platform.system()
    if system_platform == "Windows":
        try:
            top_output = subprocess.check_output(["tasklist"]).decode("utf-8")
        except Exception as e:
            top_output = f"Error running tasklist: {e}"
    else:
        try:
            top_output = subprocess.check_output(["top", "-b", "-n", "1"]).decode("utf-8")
        except Exception as e:
            top_output = f"Error running top command: {e}"

    # Build an HTML page
    html = f"""
    <html>
    <head><title>/htop</title></head>
    <body>
      <h1>Name: {name}</h1>
      <h2>Username: {user}</h2>
      <h3>Server Time (IST): {server_time}</h3>
      <pre>{top_output}</pre>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # Listen on all interfaces, port 5000
    app.run(host="0.0.0.0", port=5000)
