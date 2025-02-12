import os
import subprocess
import time
import requests
from alive import keep_alive

# Set your Heroku API details
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_OAUTH_TOKEN = os.getenv("HEROKU_OAUTH_TOKEN")



HEADERS = {
    "Authorization": f"Bearer {HEROKU_OAUTH_TOKEN}",
    "Accept": "application/vnd.heroku+json; version=3"
}

def fetch_logs():
    """Fetch the latest logs from Heroku."""
    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/log-sessions"
    payload = {
        "dyno": None,
        "lines": 100,
        "source": "app",
        "tail": False
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        log_url = response.json().get("logplex_url")
        if log_url:
            log_response = requests.get(log_url)
            return log_response.text
    print(f"❌ Error fetching logs: {response.status_code}, {response.text}")
    return None

def restart_app():
    """Restart the Heroku app."""
    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/dynos"
    response = requests.delete(url, headers=HEADERS)
    
    if response.status_code == 202:
        print("✅ App restarted successfully!")
    else:
        print(f"❌ Error restarting app: {response.status_code}, {response.text}")

def monitor_logs():
    """Continuously check logs and restart on error."""
    while True:
        logs = fetch_logs()
        if logs:
            print("📜 Logs fetched successfully!")  # Confirm logs are received
            print(logs)  # Print logs for debugging
            
            if "OSError: Connection lost" in logs:
                print("⚠️ Detected 'Connection lost' error. Restarting app...")
                restart_app()
        
        time.sleep(30)  # Wait before checking again

if __name__ == "__main__":
    print(f"🚀 Monitoring Heroku logs for '{HEROKU_APP_NAME}'...")
    keep_alive()
    monitor_logs()
