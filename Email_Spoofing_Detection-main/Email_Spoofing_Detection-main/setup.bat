@echo off
echo Setting up Email Spoofing Detection Web Application...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or later.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Check for credentials.json
if not exist credentials.json (
    echo WARNING: credentials.json not found!
    echo Please follow these steps:
    echo 1. Go to Google Cloud Console
    echo 2. Create a project or select existing one
    echo 3. Enable Gmail API
    echo 4. Configure OAuth consent screen
    echo 5. Create OAuth client ID credentials
    echo 6. Download and rename the file to 'credentials.json'
    echo 7. Place it in this directory
)

echo Setup complete! Run 'python app.py' to start the application.
pause 