@echo off

REM Check if Python is installed and in PATH
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Attempting to install...

    REM Download Python installer
    PowerShell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python_installer.exe"

    REM Install Python
    echo Installing Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    echo Python installed successfully.

    REM Clean up installer
    del python_installer.exe
)
REM Assume Python is available or the user will handle it manually
REM Setup and activate virtual environment
python -m venv chatbot-env
call chatbot-env\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo Setup complete. Running the chatbot now...
python chatbot.py

echo Press any key to exit...
pause >nul