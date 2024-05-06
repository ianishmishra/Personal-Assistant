#!/bin/bash

# Create a Python virtual environment
python3 -m venv chatbot-env

# Activate the environment
source chatbot-env/bin/activate

# Install the required packages
pip install -r requirements.txt

echo "Setup complete. Run the chatbot with 'python chatbot.py'"
