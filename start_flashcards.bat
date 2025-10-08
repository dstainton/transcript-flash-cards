@echo off
REM Flashcards Application Launcher
REM This script creates a virtual environment and starts the Flask server

echo ============================================
echo    Scrum Flashcards Application
echo ============================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Checking dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may not have installed correctly
    echo.
)

REM Check if OpenAI API key exists
if not exist "openaikey.txt" (
    echo.
    echo WARNING: openaikey.txt not found!
    echo Please create openaikey.txt with your OpenAI API key
    echo.
    pause
)

REM Start Flask server and open browser
echo.
echo ============================================
echo Starting Flashcards Server...
echo ============================================
echo.
echo Server will start at: http://localhost:5000
echo Opening browser in 3 seconds...
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Wait 3 seconds then open browser
timeout /t 3 /nobreak >nul
start http://localhost:5000

REM Start the Flask application
python app.py

REM If Flask exits, pause so user can see any error messages
echo.
echo Server stopped.
pause

