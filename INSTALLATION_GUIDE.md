# Scrum Flashcards - Windows Installation Guide

## What You Need
- **Python 3.7+** installed from [python.org](https://www.python.org/)
  - ⚠️ Make sure "Add Python to PATH" is checked during installation
- **OpenAI API Key** from [platform.openai.com](https://platform.openai.com/)

## First-Time Setup (5 minutes)

### Step 1: Add Your OpenAI API Key
1. Open the application folder
2. Create a new text file named `openaikey.txt`
3. Paste your OpenAI API key into this file
4. Save and close

### Step 2: Start the Application
**Option A - Quick Start:**
- Simply double-click `start_flashcards.bat`
- Wait while it sets up (only happens once)
- Your browser will open automatically

**Option B - Desktop Shortcut:**
1. Double-click `CREATE_SHORTCUT.vbs`
2. Click "OK" when the confirmation appears
3. A shortcut named "Scrum Flashcards" appears on your desktop
4. Use this shortcut to start the app anytime

### Step 3: You're Done!
The application is now running at http://localhost:5000

## What Happens on First Run

The `start_flashcards.bat` script automatically:
1. ✅ Creates an isolated Python environment (`.venv` folder)
2. ✅ Installs all required packages (Flask, OpenAI, flask-session)
3. ✅ Starts the web server
4. ✅ Opens your browser

**This setup only happens once!** Future runs start immediately.

## Daily Use

### Starting the Application
- Double-click `start_flashcards.bat`, OR
- Use the desktop shortcut (if created), OR
- Navigate to the folder and run the batch file

### Stopping the Application
- Press `Ctrl+C` in the command window, OR
- Close the command window, OR  
- Double-click `stop_flashcards.bat`

## Understanding the Files

### Files You Interact With
- `start_flashcards.bat` - Start the application
- `stop_flashcards.bat` - Stop the application
- `CREATE_SHORTCUT.vbs` - Create desktop shortcut
- `openaikey.txt` - Your API key (you create this)

### Files Created Automatically
- `.venv/` - Isolated Python environment (safe to delete to reset)
- `.flask_session/` - Session storage
- `flashcards.json` - Generated flashcards cache
- `history.json` - Your study/exam history
- `secret_key.txt` - Security key for sessions

### Application Files (Don't Modify)
- `app.py` - Main application code
- `requirements.txt` - List of dependencies
- `static/` - CSS styling
- `templates/` - HTML pages
- `transcripts/` - Your transcript files

## Troubleshooting

### "Python is not installed or not in PATH"
- Install Python from [python.org](https://www.python.org/)
- During installation, check "Add Python to PATH"
- Restart your computer

### "openaikey.txt not found"
- Create the file `openaikey.txt` in the same folder as `start_flashcards.bat`
- Paste your API key into this file
- Make sure it's named exactly `openaikey.txt` (not `.txt.txt`)

### Server won't start
- Make sure no other Flask app is running on port 5000
- Try running `stop_flashcards.bat` first
- Delete the `.venv` folder and run again (forces reinstall)

### Browser doesn't open automatically
- Manually open your browser
- Go to http://localhost:5000

### Starting fresh
1. Run `stop_flashcards.bat`
2. Delete `.venv` folder
3. Optionally delete `flashcards.json` and `history.json`
4. Run `start_flashcards.bat` again

## Advanced: Virtual Environment Benefits

The `.venv` folder is a **virtual environment** that:
- ✅ Keeps this app's packages separate from your system Python
- ✅ Prevents conflicts with other Python projects
- ✅ Makes the app portable and reproducible
- ✅ Can be safely deleted if you need to start fresh

**You never need to manually activate it** - the batch file does this automatically!

## Need Help?

If you encounter issues:
1. Check the command window for error messages
2. Ensure Python 3.7+ is installed and in PATH
3. Verify `openaikey.txt` exists and contains your API key
4. Try deleting `.venv` and running again
5. Check the README.md for more detailed information

## Enjoy Your Flashcards! 🎓

The application is designed to help you learn Scrum concepts through:
- **Study Mode** - Practice with immediate feedback
- **Exam Mode** - Test yourself with timed questions
- **Statistics** - Track your progress over time

Good luck with your Scrum certification! 🚀

