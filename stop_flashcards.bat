@echo off
REM Stop the Flashcards Application

echo Stopping Flashcards Server...

REM Find and kill Python processes running app.py
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo list ^| find "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%app.py%%'" call terminate >nul 2>&1
)

echo Server stopped.
timeout /t 2 /nobreak >nul

