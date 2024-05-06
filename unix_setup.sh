#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Attempting to install..."
    # Using apt-get to install Python3; adapt the installer command for different Linux distributions if necessary
    sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3."
        exit 1
    fi
    echo "Python 3 installed successfully."
fi

# Assume Python3 is available or the user will handle it manually
# Setup and activate virtual environment
python3 -m venv chatbot-env
source chatbot-env/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete. Running the chatbot now..."
python3 chatbot.py

echo "Press any key to exit..."
read -rsn1
