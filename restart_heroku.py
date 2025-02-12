import os
import subprocess
import time
import requests

# Set your Heroku API details
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

# Function to restart the Heroku app
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

# Function to continuously monitor logs
def monitor_heroku_logs():
    while True:
        try:
            print("📡 Monitoring Heroku logs...")
            process = subprocess.Popen(
                ["heroku", "logs", "--tail", "--app", HEROKU_APP_NAME],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Read logs in real-time
            for line in iter(process.stdout.readline, ""):
                print(line.strip())  # Print logs live
                if "OSError: Connection lost" in line:
                    print("⚠️ Connection lost error detected! Restarting Heroku app...")
                    restart_heroku_app()
                    time.sleep(10)  # Wait before rechecking logs

            process.stdout.close()
            process.stderr.close()
            process.wait()

        except Exception as e:
            print(f"❌ Error in monitoring logs: {e}")

        print("🔄 Restarting log monitoring in 30 seconds...")
        time.sleep(30)  # Wait before restarting log monitoring

# Run the log monitoring function continuously
monitor_heroku_logs()
