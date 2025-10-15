# How to Update to the Latest Version

## Your Data is Safe! 🔒

All your important files are protected during updates:
- ✅ Your API key (`openaikey.txt`)
- ✅ Your session key (`secret_key.txt`)
- ✅ All your projects and flashcards (`projects/` folder)
- ✅ Your virtual environment (`.venv/`)
- ✅ Legacy data if migrating (`flashcards.json`, `history.json`, `mastery.json`)

---

## Method 1: Git Update (Recommended)

If you installed using Git:

```bash
# Stop the server first (Ctrl+C or run stop_flashcards.bat)

# Pull the latest changes
git pull

# Start the server again
# Double-click start_flashcards.bat (Windows)
# or run: python app.py
```

**That's it!** Git only updates application files and leaves your data untouched.

---

## Method 2: Manual Update (Download & Replace)

If you downloaded the files manually:

### Step 1: Backup Your Key Files (Optional but Recommended)
Copy these to a safe location:
- `openaikey.txt`
- `secret_key.txt` (if it exists)
- `projects/` folder (your entire project data)

### Step 2: Download Latest Version
- Download the latest release or clone the repository
- Extract to a temporary location

### Step 3: Update Files
**Option A - Replace Application Files Only (Safest):**
1. Stop the server
2. From the new download, copy ONLY these:
   - `app.py`
   - `project_manager.py`
   - `document_processor.py`
   - `migrate_to_projects.py`
   - `requirements.txt`
   - `start_flashcards.bat`
   - `stop_flashcards.bat`
   - `static/` folder
   - `templates/` folder
3. Do NOT copy: `openaikey.txt`, `secret_key.txt`, `projects/`, `.venv/`

**Option B - Full Replace (with backup):**
1. Rename your old folder to `flashcards-backup`
2. Extract the new version
3. Copy from backup to new folder:
   - `openaikey.txt`
   - `secret_key.txt`
   - `projects/` folder

### Step 4: Update Dependencies
```bash
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

# Mac/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Start the Server
- Double-click `start_flashcards.bat` (Windows)
- Or run: `python app.py`

---

## What Happens on First Run After Update

1. **Dependencies Install:** New packages (PDF/Word processors) install automatically
2. **Auto-Migration:** If you have old data, it migrates automatically to the new structure
3. **Backups Created:** Original files are backed up with `.backup` extension
4. **Ready to Use:** Your projects and data are preserved and ready!

---

## Verifying the Update

After updating and starting the server:

1. **Check Projects:**
   - Go to "Projects" in the header
   - You should see your existing project(s)
   - If migrating, look for your default project

2. **Check Data:**
   - Open a project
   - Your flashcards should all be there
   - Your mastery progress should be preserved
   - Your history should be intact

3. **Test New Features:**
   - Try creating a new project with "Create Project from Documents"
   - Drag and drop a PDF or Word file
   - See the AI-powered generation in action!

---

## Troubleshooting Updates

### "openaikey.txt not found"
- You need to recreate this file with your API key
- Check your backup if you made one

### "No projects found"
- The migration might not have run
- Check if `flashcards.json`, `history.json` exist in the root
- Restart the app to trigger migration

### "Import errors" or "Module not found"
- Delete the `.venv` folder
- Run `start_flashcards.bat` again to reinstall everything

### "My data is missing"
- Check the `projects/` folder - your data is there
- Check for `.backup` files in the root - these are your originals
- Look in `projects/<your-project-name>/` for flashcards, history, mastery

### Starting completely fresh
If you want to start over:
1. Backup your `openaikey.txt`
2. Delete: `.venv/`, `projects/`, `.flask_session/`
3. Keep: `openaikey.txt`
4. Run `start_flashcards.bat`

---

## Need Help?

1. Check the `INSTALLATION_GUIDE.md` for setup help
2. Check the `README.md` for feature documentation
3. Look for `.backup` files if you think data was lost
4. Your project data is in `projects/<project-id>/`

---

## Version History

### Latest Version Features:
- 🗂️ Multi-project management
- 📁 Drag-and-drop document upload
- 🤖 AI-powered project creation
- 📊 Per-project statistics and mastery
- 🎯 Enhanced mastery system with visual progress
- 📄 PDF, Word, and text file support

Happy studying! 🚀

