# Transcript Flashcards - Windows Installation Guide

## What You Need
- **Python 3.7+** installed from [python.org](https://www.python.org/)
  - ⚠️ Make sure "Add Python to PATH" is checked during installation
- **OpenAI API Key** from [platform.openai.com](https://platform.openai.com/)

## ✅ Upgrading from a Previous Version?

**Good news!** Your existing data is 100% safe:
- ✅ Your API key (`openaikey.txt`) will never be overwritten
- ✅ Your session security key (`secret_key.txt`) is preserved
- ✅ Existing flashcards, history, and transcripts are automatically migrated
- ✅ Original files are backed up with `.backup` extension
- ✅ Migration happens automatically on first run - no action needed!

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
2. ✅ Installs all required packages (Flask, OpenAI, flask-session, PDF/Word processors)
3. ✅ **Migrates existing data** to new project structure (if you're upgrading)
   - Creates a default project with your existing flashcards
   - Preserves all your history and mastery progress
   - Backs up original files for safety
4. ✅ Starts the web server
5. ✅ Opens your browser

**This setup only happens once!** Future runs start immediately.

### New Features Available After Migration
- 📁 **Multi-Project Support** - Create separate projects for different topics
- 🤖 **AI Project Creation** - Drag & drop documents to auto-generate flashcards
- 📊 **Per-Project Statistics** - Each project tracks its own progress
- 🎯 **Enhanced Mastery System** - Better tracking of learned cards

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
- `openaikey.txt` - Your API key (you create this - **never overwritten**)

### Files Created Automatically (Never Overwritten)
- `.venv/` - Isolated Python environment (safe to delete to reset)
- `.flask_session/` - Session storage (temporary)
- `temp_uploads/` - Temporary document uploads
- `secret_key.txt` - Security key for sessions (**preserved**)
- `projects/` - Multi-project data folder
  - `<project-id>/` - Each project has its own folder
    - `project.json` - Project metadata
    - `flashcards.json` - Project's flashcards
    - `history.json` - Project's session history
    - `mastery.json` - Project's mastery tracking
    - `documents/` - Original source documents

### Legacy Files (Auto-Migrated on First Run)
If upgrading from an older version:
- `flashcards.json` → Moved to `projects/<default-project>/`
- `history.json` → Moved to `projects/<default-project>/`
- `mastery.json` → Moved to `projects/<default-project>/`
- `transcripts/` → Moved to `projects/<default-project>/documents/`
- **Originals backed up** with `.backup` extension

### Application Files (Don't Modify)
- `app.py` - Main application code
- `project_manager.py` - Project management logic
- `document_processor.py` - Document text extraction
- `migrate_to_projects.py` - Auto-migration script
- `requirements.txt` - List of dependencies
- `static/` - CSS styling
- `templates/` - HTML pages

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
3. Optionally delete `projects/` folder to remove all project data
4. Keep `openaikey.txt` and `secret_key.txt`
5. Run `start_flashcards.bat` again

### After migrating, where is my data?
- Your existing flashcards are in `projects/<default-project-name>/flashcards.json`
- Your history is in `projects/<default-project-name>/history.json`
- Your mastery data is in `projects/<default-project-name>/mastery.json`
- Your original transcripts are in `projects/<default-project-name>/documents/`
- Original root-level files are backed up with `.backup` extension

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

The application is now more powerful than ever with:
- **📁 Multi-Project Support** - Create separate projects for different topics
- **🤖 AI-Powered Creation** - Drag & drop documents to auto-generate flashcards
  - Supports PDF, Word (.docx), and text files
  - AI analyzes content and suggests project names
  - Smart topic extraction and flashcard generation
- **📚 Study Mode** - Practice with immediate feedback and mastery tracking
- **📝 Exam Mode** - Test yourself with timed questions
- **📊 Statistics** - Track your progress per project over time
- **🎯 Mastery System** - Visual progress tracking for each flashcard

### Quick Start with Your First Project:
1. Click "Projects" → "Create Project from Documents"
2. Drag and drop your PDF, Word, or text files
3. Review AI suggestions and create your project
4. Start studying immediately!

Good luck with your learning journey! 🚀

