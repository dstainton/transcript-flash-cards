# Settings System Implementation

## What Was Added

A complete settings system with UI, backend routes, and auto-update functionality.

---

## Files Created

1. **`settings.json`** - Settings storage file
   - OpenAI API key file path
   - Default flashcards per topic (25)
   - Default time per card (10 seconds)
   - Default exam time (60 minutes)
   - Auto-update enabled flag
   - Last update check timestamp

2. **`templates/settings.html`** - Settings page UI
   - OpenAI API key management with visibility toggle
   - Flashcard generation defaults configuration
   - Auto-update settings
   - Manual update check button
   - Responsive design with validation

3. **`SETTINGS_GUIDE.md`** - Comprehensive documentation
   - Feature explanations
   - Troubleshooting guide
   - Best practices
   - Manual update instructions

---

## Files Modified

### 1. `templates/base.html`
**Added:**
- Gear icon (⚙️) in navbar for settings access
- SVG settings icon with hover effect
- Link to `/settings` route

### 2. `app.py`
**Added:**
- `load_settings()` - Load settings from JSON file
- `save_settings()` - Save settings to JSON file
- `get_app_settings()` - Get settings with defaults on startup
- `@app.route('/settings')` - Settings page (GET/POST)
- `@app.route('/check-updates')` - Check for updates via Git
- `@app.route('/install-update')` - Install updates via Git pull

**Modified:**
- Global constants now load from settings file
- `CARDS_PER_TRANSCRIPT`, `TIME_PER_CARD`, `TOTAL_EXAM_TIME` use settings

### 3. `start_flashcards.bat`
**Added:**
- GitPython installation for update support
- Auto-update check on startup
- Git fetch and pull if updates available
- Conditional update based on settings.json

---

## Features

### 1. API Key Management
- ✅ Update OpenAI API key from UI
- ✅ Masked display for security
- ✅ Toggle visibility with eye icon
- ✅ Saves to `openaikey.txt`

### 2. Default Configuration
- ✅ Set default flashcards per topic
- ✅ Set default study time per card
- ✅ Set default exam duration
- ✅ Values used across the app
- ✅ Can be overridden per session

### 3. Auto-Update System
- ✅ Enable/disable automatic updates
- ✅ Check for updates manually
- ✅ Install updates with one click
- ✅ Preserves all user data
- ✅ Works with Git repositories

---

## How It Works

### Settings Flow
```
User opens Settings (⚙️ icon)
  ↓
Settings page loads current values
  ↓
User updates values and saves
  ↓
Backend saves to settings.json and openaikey.txt
  ↓
Flash message confirms save
  ↓
Settings take effect immediately
```

### Auto-Update Flow
```
User starts app (start_flashcards.bat)
  ↓
Script checks settings.json for auto_update_enabled
  ↓
If enabled: git fetch origin
  ↓
Check commits behind origin/main
  ↓
If updates found: git pull origin main
  ↓
Reinstall dependencies if needed
  ↓
App starts with latest code
```

### Manual Update Flow
```
User clicks "Check for Updates Now"
  ↓
Frontend calls /check-updates
  ↓
Backend runs: git fetch && git rev-list --count HEAD..origin/main
  ↓
Returns number of updates available
  ↓
User clicks "Install Now"
  ↓
Backend runs: git pull origin main
  ↓
Success message shown
  ↓
User restarts app for changes
```

---

## Security

### API Key Protection
- Stored in `openaikey.txt` (excluded from git via `.gitignore`)
- Masked in UI display (only shows first 8 and last 4 characters)
- Toggle visibility only while editing
- Never transmitted except to OpenAI API

### Update Security
- Only pulls from configured `origin/main`
- User data files are git-ignored
- No destructive operations (no force push/reset)
- Updates only code, not data

---

## User Experience

### Before
- ❌ No way to update API key without editing file
- ❌ Default values hardcoded in app.py
- ❌ Manual git commands required for updates
- ❌ No visibility into update availability

### After
- ✅ Settings page accessible from any page
- ✅ Update API key with UI
- ✅ Configure defaults easily
- ✅ One-click updates
- ✅ Auto-update on startup option
- ✅ Clear update status and history

---

## Testing Checklist

### API Key Management
- [ ] Open settings page (⚙️ icon works)
- [ ] Current API key is masked
- [ ] Toggle visibility works
- [ ] Enter new API key
- [ ] Save settings
- [ ] Verify `openaikey.txt` updated
- [ ] Create new flashcards (API key works)

### Default Values
- [ ] Change default flashcards per topic
- [ ] Change default time per card
- [ ] Change default exam time
- [ ] Save settings
- [ ] Verify `settings.json` updated
- [ ] Start new session (defaults apply)

### Auto-Update
- [ ] Enable auto-update
- [ ] Save settings
- [ ] Restart application
- [ ] Verify update check runs
- [ ] Verify no errors if up-to-date

### Manual Update
- [ ] Click "Check for Updates Now"
- [ ] Verify status shows correctly
- [ ] If updates available, click "Install Now"
- [ ] Verify success message
- [ ] Restart application
- [ ] Verify changes applied

---

## Requirements

### For Settings Page
- ✅ Python 3.x
- ✅ Flask
- ✅ Write access to app directory

### For Auto-Update
- ✅ Git installed on system
- ✅ App installed via `git clone`
- ✅ Internet connection
- ✅ Read/write access to `.git/` folder

---

## Troubleshooting

### "Settings not saving"
**Check:** File permissions on `settings.json` and `openaikey.txt`

### "Auto-update not working"
**Check:**
1. Git installed: `git --version`
2. Is git repository: check `.git/` folder exists
3. Auto-update enabled in settings
4. Internet connection

### "Update check fails"
**Check:**
1. Git installed
2. Repository has `origin` remote: `git remote -v`
3. Can access remote: `git fetch origin`

---

## Future Enhancements

Possible additions:
- [ ] Update branch selection (stable vs beta)
- [ ] Backup before update
- [ ] Rollback to previous version
- [ ] Update notifications in UI
- [ ] Custom API endpoint configuration
- [ ] Import/export settings
- [ ] Theme selection (light/dark mode)

---

## Files Protected During Updates

These files are in `.gitignore` and won't be overwritten:
- `openaikey.txt` - Your API key
- `settings.json` - Your settings
- `secret_key.txt` - Session encryption key
- `projects/` - All your flashcard projects
- `.venv/` - Virtual environment
- `temp_uploads/` - Temporary files
- `.flask_session/` - Session data
- `*.backup` - Backup files

---

**Implementation Complete! ✅**

Users now have full control over their configuration and can easily keep the application up-to-date.

