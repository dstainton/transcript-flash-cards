# Production Release Update System

## Overview

The Flash Cards application now uses **Git tags** for production releases, ensuring users only receive stable, tested versions.

---

## How It Works

### Release-Based Updates (Not Commit-Based)

**OLD Approach (❌ Removed):**
- Checked latest commit on main branch
- Users got untested code
- Unstable features could break app

**NEW Approach (✅ Current):**
- Uses Git tags for versions (e.g., `v1.0.0`, `v1.1.0`)
- Only tagged releases are installed
- Maintainers control what users receive
- Follows semantic versioning

---

## For Users

### Auto-Update

When enabled in Settings:

1. **Startup Check:**
   ```
   Application starts
   ↓
   Fetches release tags: git fetch --tags
   ↓
   Gets current version: git describe --tags
   ↓
   Gets latest version: git tag -l --sort=-v:refname
   ↓
   Compares versions
   ↓
   If newer release exists: git checkout v1.1.0
   ↓
   App runs on new version
   ```

2. **What You See:**
   ```
   ============================================
     New Release Available!
     Current: v1.0.0
     Latest:  v1.1.0
   ============================================
   Installing update...
   ✓ Updated to version v1.1.0!
   ```

### Manual Update from Settings

1. Click **⚙️ Settings** icon
2. See **Current Version** displayed
3. Click **"Check for Release Updates"**
4. If available: Click **"Install Version v1.1.0"**
5. Success message appears
6. Restart application

### Version Display

Settings page now shows:
```
Current Version: v1.0.0
[Update Available: v1.1.0] ← Yellow badge if newer exists
```

---

## For Maintainers

### Creating a Release

```bash
# 1. Test thoroughly
python app.py  # Verify all features work

# 2. Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0 - Settings and Auto-Update"

# 3. Push tag to remote
git push origin v1.1.0

# Done! Users will get this version next time they update.
```

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- `v1.0.0` → `v1.0.1` - Bug fix (PATCH)
- `v1.0.0` → `v1.1.0` - New feature (MINOR)
- `v1.0.0` → `v2.0.0` - Breaking change (MAJOR)

### Release Workflow

See `RELEASE_GUIDE.md` for detailed instructions.

---

## Technical Implementation

### Version Detection

**Current Version:**
```python
def get_current_version():
    # Try to get exact tag we're on
    result = subprocess.run(['git', 'describe', '--tags', '--exact-match'])
    if result.returncode == 0:
        return result.stdout.strip()
    
    # Fallback to latest tag we're based on
    result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'])
    return result.stdout.strip()
```

**Latest Version:**
```python
def get_latest_release_tag():
    # Fetch all tags
    subprocess.run(['git', 'fetch', '--tags'])
    
    # Get tags sorted by version (highest first)
    result = subprocess.run(['git', 'tag', '-l', '--sort=-v:refname'])
    
    # Return first tag (latest version)
    tags = result.stdout.split('\n')
    return tags[0] if tags else None
```

**Version Comparison:**
```python
def compare_versions(current, latest):
    # Parse version strings: v1.1.0 → (1, 1, 0)
    current_parts = parse_version(current)  # e.g., (1, 0, 0)
    latest_parts = parse_version(latest)    # e.g., (1, 1, 0)
    
    # Compare as tuples: (1, 1, 0) > (1, 0, 0) = True
    return latest_parts > current_parts
```

### Update Installation

```python
@app.route('/install-update', methods=['POST'])
def install_update():
    # Get latest release tag
    latest_tag = get_latest_release_tag()  # e.g., "v1.1.0"
    
    # Check for uncommitted user data
    result = subprocess.run(['git', 'status', '--porcelain'])
    # (Ignores openaikey.txt, settings.json, projects/, etc.)
    
    # Checkout the release tag
    subprocess.run(['git', 'checkout', latest_tag])
    
    # Update settings with new version
    settings['current_version'] = latest_tag
    save_settings(settings)
    
    return jsonify({
        'success': True,
        'version': latest_tag
    })
```

### Startup Auto-Update (Batch Script)

```batch
REM Fetch release tags
git fetch --tags

REM Get current version
for /f %%i in ('git describe --tags --abbrev=0') do set CURRENT_VER=%%i

REM Get latest version (first tag when sorted)
for /f %%i in ('git tag -l --sort=-v:refname') do (
    set LATEST_VER=%%i
    goto :found_latest
)
:found_latest

REM Compare and update if needed
if not "%CURRENT_VER%"=="%LATEST_VER%" (
    git checkout %LATEST_VER%
)
```

---

## Safety Features

### Data Protection

**Protected Files (Never Overwritten):**
- `openaikey.txt` - Your API key
- `settings.json` - Your settings
- `projects/` - All flashcard data
- `.venv/` - Python environment
- `secret_key.txt` - Session key

**How It's Protected:**
```bash
# These are in .gitignore
# Git checkout won't touch them
git checkout v1.1.0  # Safe - only updates tracked files
```

### Uncommitted Changes Check

Before updating, the system checks for uncommitted code changes:

```python
result = subprocess.run(['git', 'status', '--porcelain'])

uncommitted = [line for line in result.stdout.split('\n') 
              if line.strip() and not any(x in line for x in 
              ['openaikey.txt', 'settings.json', 'projects/'])]

if uncommitted:
    return error("Please commit or stash changes first")
```

### Rollback Capability

Users can roll back manually:

```bash
# List available versions
git tag -l

# Rollback to previous version
git checkout v1.0.0
```

---

## Comparison: Old vs New

### Checking for Updates

**OLD (Commit-Based):**
```bash
git fetch origin
git rev-list --count HEAD..origin/main
# Shows: "5 commits behind"
# ❌ Could include broken code
```

**NEW (Release-Based):**
```bash
git fetch --tags
git tag -l --sort=-v:refname
# Shows: "v1.1.0 available"
# ✅ Only stable releases
```

### Installing Updates

**OLD:**
```bash
git pull origin main
# ❌ Gets all commits (stable or not)
```

**NEW:**
```bash
git checkout v1.1.0
# ✅ Gets specific tested release
```

### User Experience

**OLD:**
```
"5 updates available"
User: "What changed? Is it safe?"
```

**NEW:**
```
"Update available: v1.0.0 → v1.1.0"
Release Notes: "Settings page, auto-update, bug fixes"
User: "Clear what I'm getting!"
```

---

## Example Scenarios

### Scenario 1: Normal Update

```
User on v1.0.0
Maintainer releases v1.1.0
User starts app → Auto-update
Now on v1.1.0 ✓
```

### Scenario 2: Skip a Version

```
User on v1.0.0
Maintainer releases v1.1.0 (user doesn't update)
Maintainer releases v1.2.0
User starts app → Auto-update
Jumps directly to v1.2.0 ✓
```

### Scenario 3: Hotfix

```
User on v1.1.0
Bug discovered
Maintainer releases v1.1.1 (hotfix)
User updates
Now on v1.1.1 ✓
```

### Scenario 4: Development Version

```
Developer on v1.1.0
Working on features for v1.2.0
Commits code but doesn't tag
Users still on v1.1.0 ✓
When ready: git tag v1.2.0
Then users can update ✓
```

---

## Benefits

### For Users
- ✅ Only receive stable, tested versions
- ✅ Clear version numbers
- ✅ Can see what changed
- ✅ Can roll back if needed
- ✅ No surprise breaking changes

### For Maintainers
- ✅ Control what users receive
- ✅ Test before releasing
- ✅ Clear version history
- ✅ Hotfix specific versions
- ✅ Track issues by version

---

## Troubleshooting

### "No release tags found"

**Cause:** Repository has no tags yet

**Solution:**
```bash
# Create first release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

### "Update check fails"

**Cause:** Not a git repository or no remote

**Solution:**
```bash
# Check git status
git remote -v  # Should show origin
ls -la .git    # Should exist

# If not a git repo, clone instead
```

### "Failed to checkout release"

**Cause:** Uncommitted changes or conflicts

**Solution:**
```bash
# Check status
git status

# Stash user code changes (not data!)
git stash

# Try update again
```

---

## Future Enhancements

Possible additions:
- [ ] Release notes in-app
- [ ] Beta channel (pre-release tags)
- [ ] Update scheduling (install tonight at 2am)
- [ ] Bandwidth-efficient updates (delta patches)
- [ ] Cryptographic signature verification

---

**Production releases ensure stability and user confidence!** 🚀

