import os
import time
import requests
from alive import keep_alive 
# Get Heroku API credentials from environment variables
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_OAUTH_TOKEN = os.getenv("HEROKU_OAUTH_TOKEN")

if not HEROKU_APP_NAME or not HEROKU_OAUTH_TOKEN:
    print("❌ Error: Missing HEROKU_APP_NAME or HEROKU_OAUTH_TOKEN.")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {HEROKU_OAUTH_TOKEN}",
    "Accept": "application/vnd.heroku+json; version=3",
    "Content-Type": "application/json"
}

def fetch_logs():
    """Fetch the latest logs from Heroku."""
    print("🔍 Fetching logs...")
    
    url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/log-sessions"
    payload = {
        "lines": 100,
        "source": "app",
        "tail": False
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        log_url = response.json().get("logplex_url")
        if log_url:
            log_response = requests.get(log_url)
            print("✅ Logs fetched successfully!")
            return log_response.text
    else:
        print(f"❌ Error fetching logs: {response.status_code}, {response.text}")
    
    return None

def restart_app():
    """Restart the Heroku app."""
    print("🔄 Restarting Heroku app...")
    
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
            print("📜 Logs Preview:")
            print(logs[:500])  # Print only the first 500 characters to avoid spam

            if "OSError: Connection lost" in logs or "socket.send() raised exception" in logs:
                print("⚠️ Detected 'Connection lost' or 'socket.send()' error. Restarting app...")
                restart_app()
        
        print("⏳ Waiting 120 seconds before checking logs again...")
        time.sleep(120)  # Wait before checking again

if __name__ == "__main__":
    print(f"🚀 Monitoring Heroku logs for '{HEROKU_APP_NAME}'...")
    keep_alive()
    monitor_logs()
    
