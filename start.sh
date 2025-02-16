#!/bin/bash

# Install Heroku CLI
echo "Installing Heroku CLI..."
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Verify installation
echo "Verifying Heroku installation..."
heroku --version

python3 restart_heroku.py
