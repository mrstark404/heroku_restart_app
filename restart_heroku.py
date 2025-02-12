import os
import subprocess
import time
import requests
from alive import keep_alive

# Set your Heroku API details
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

def restart_heroku_app():
    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/dynos"
    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {HEROKU_API_KEY}",
    }
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 202:
        print("✅ Heroku app restarted successfully!")
    else:
        print(f"❌ Failed to restart app. Error: {response.text}")

def monitor_heroku_logs():
    print(f"🔍 Monitoring logs for Heroku app: {HEROKU_APP_NAME}...\n")

    while True:
        try:
            process = subprocess.Popen(
                ["heroku", "logs", "--tail", "--app", HEROKU_APP_NAME],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Read logs line by line
            for line in iter(process.stdout.readline, ""):
                log_line = line.strip()
                print(f"📜 Log: {log_line}")  # Print log to confirm fetching
                
                if "OSError: Connection lost" in log_line:
                    print("⚠️ Detected 'OSError: Connection lost' in logs! Restarting Heroku app...")
                    restart_heroku_app()
                    time.sleep(60)  # Wait 60 seconds before restarting again

        except Exception as e:
            print(f"❌ Error in monitoring logs: {e}")
        
        # Restart log monitoring after 10 seconds if process fails
        print("🔄 Restarting log monitoring in 10 seconds...")
        time.sleep(10)

# Run the log monitoring function continuously
keep_alive()
monitor_heroku_logs()
