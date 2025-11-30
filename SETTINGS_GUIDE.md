# Settings Guide

## Overview

The Settings page provides a centralized location to configure your Flash Cards application, including API keys, default values, and automatic updates.

Access Settings by clicking the ⚙️ gear icon in the top-right corner of any page.

---

## Settings Sections

### 1. OpenAI API Configuration

**OpenAI API Key**
- Your API key for generating flashcards using GPT-4
- Get a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Securely stored in `openaikey.txt`
- Displayed with masking for security (shows only first 8 and last 4 characters)
- Click the eye icon (👁️) to toggle visibility when entering

**Security Note:** Your API key is stored locally on your machine and never transmitted anywhere except to OpenAI's API for flashcard generation.

---

### 2. Flashcard Generation Defaults

**Default Flashcards per Topic** (5-100)
- Default number of flashcards to generate for each topic
- Can be overridden when creating individual projects
- Recommended: 15-25 for most topics
- Default: 25

**Default Time per Card** (5-120 seconds)
- Time limit for studying each flashcard in study mode
- Affects the pace of your study sessions
- Recommended: 10-15 seconds
- Default: 10

**Default Total Exam Time** (5-180 minutes)
- Total time limit for exam mode sessions
- Can be adjusted when starting each exam
- Recommended: 30-60 minutes
- Default: 60

---

### 3. Software Updates

**Enable Automatic Updates**
- Automatically check for and install updates when starting the application
- Requires Git to be installed on your system
- Only works if you installed via `git clone`
- Updates are pulled from the main branch

**Check for Updates Now**
- Manually check if updates are available
- Shows number of commits behind the latest version
- Requires Git installation

**Install Update**
- Downloads and installs the latest version
- Preserves all your data (projects, settings, API key)
- May require application restart

**Last Update Check**
- Displays when updates were last checked
- Updated automatically if auto-update is enabled

---

## How Auto-Update Works

### Requirements
1. Git must be installed on your system
2. Application must be installed via `git clone` (not downloaded as ZIP)
3. Auto-update must be enabled in settings

### Update Process
1. **On Startup:**
   - Script checks `settings.json` for `auto_update_enabled`
   - If enabled, runs `git fetch origin`
   - Checks commits behind `origin/main`
   
2. **If Updates Found:**
   - Runs `git pull origin main`
   - Updates application files
   - Preserves user data (`openaikey.txt`, `settings.json`, `projects/`)
   - Reinstalls dependencies if `requirements.txt` changed

3. **What's Protected:**
   - ✅ Your API key (`openaikey.txt`)
   - ✅ Your settings (`settings.json`)
   - ✅ All projects (`projects/` folder)
   - ✅ Virtual environment (`.venv/`)

---

## Manual Updates

If you prefer to update manually:

1. **Disable auto-update** in Settings
2. **Check for updates** when convenient:
   ```bash
   git fetch origin
   git status
   ```
3. **Install updates:**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```
4. **Restart the application**

---

## Troubleshooting

### "Git is not installed"
**Solution:** Install Git from [git-scm.com](https://git-scm.com/)

### "Not a git repository"
**Cause:** Application was downloaded as ZIP instead of cloned
**Solution:** 
1. Back up your `openaikey.txt`, `settings.json`, and `projects/` folder
2. Clone the repository: `git clone <repository-url>`
3. Restore your backed-up files
4. Enable auto-update in settings

### "Failed to fetch updates"
**Possible causes:**
- No internet connection
- Git authentication required
- Repository URL changed

**Solution:**
```bash
git remote -v  # Check remote URL
git fetch origin --verbose  # See detailed error
```

### Updates don't apply
**Possible causes:**
- Local changes conflict with updates
- Dependencies not reinstalled

**Solution:**
```bash
# Stash local changes
git stash

# Pull updates
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt

# Restart application
```

---

## Settings File

Settings are stored in `settings.json`:

```json
{
    "openai_api_key_file": "openaikey.txt",
    "default_cards_per_topic": 25,
    "default_time_per_card": 10,
    "default_total_exam_time": 60,
    "auto_update_enabled": false,
    "last_update_check": "2025-11-30T12:00:00"
}
```

### Manual Editing

You can edit `settings.json` directly if needed:
1. Stop the application
2. Edit `settings.json` with a text editor
3. Ensure valid JSON syntax
4. Restart the application

---

## Best Practices

1. **API Key Security:**
   - Never share your API key
   - Don't commit `openaikey.txt` to version control
   - Regenerate if compromised

2. **Backups:**
   - Regularly backup `projects/` folder
   - Keep a copy of `settings.json`
   - Export important project data

3. **Updates:**
   - Enable auto-update for latest features and fixes
   - Check release notes before major updates
   - Test updates in a copy first if doing critical work

4. **Performance:**
   - Adjust time limits based on your learning pace
   - Balance flashcard count with quality (15-25 is optimal)
   - Use exam mode to test retention

---

## Need Help?

- Check `UPDATE_GUIDE.md` for update instructions
- Check `INSTALLATION_GUIDE.md` for setup help
- Check `README.md` for feature documentation
- Review error messages in the terminal/console

---

**Happy Studying! 🚀**

