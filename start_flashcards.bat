@echo off
setlocal enabledelayedexpansion
REM Flashcards Application Launcher
REM This script creates a virtual environment and starts the Flask server

echo ============================================
echo        Drew's Flash Cards Application
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

REM Check for auto-updates if enabled (production releases only)
REM Note: Errors in this section are silently ignored to not break startup
if exist "settings.json" (
    python -c "import json; settings = json.load(open('settings.json')); exit(0 if settings.get('auto_update_enabled') else 1)" 2>nul
    if !errorlevel! equ 0 (
        if exist ".git\" (
            git --version >nul 2>&1
            if !errorlevel! equ 0 (
                echo Checking for updates...
                REM Simple check - just fetch tags and compare
                git fetch --tags >nul 2>&1
                
                REM If git commands work, try to update
                git describe --tags --abbrev=0 >temp_current.txt 2>nul
                git tag -l --sort=-v:refname >temp_latest.txt 2>nul
                
                if exist "temp_current.txt" if exist "temp_latest.txt" (
                    set /p CURRENT_VER=<temp_current.txt
                    set /p LATEST_VER=<temp_latest.txt
                    
                    if not "!CURRENT_VER!"=="!LATEST_VER!" (
                        echo New version available: !LATEST_VER!
                        echo Installing update...
                        git checkout !LATEST_VER! >nul 2>&1
                        if !errorlevel! equ 0 (
                            echo ✓ Updated to !LATEST_VER!
                        )
                    )
                )
                
                REM Clean up temp files
                if exist "temp_current.txt" del temp_current.txt >nul 2>&1
                if exist "temp_latest.txt" del temp_latest.txt >nul 2>&1
            )
        )
    )
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

