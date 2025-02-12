#!/bin/bash

# Update and install required dependencies
echo "Updating system and installing dependencies..."
apt update && apt upgrade -y
apt install curl wget software-properties-common -y

# Install Heroku CLI
echo "Installing Heroku CLI..."
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Verify installation
echo "Verifying Heroku installation..."
heroku --version

python3 restart_heroku.py
