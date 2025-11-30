# Release Guide for Maintainers

## Creating a New Production Release

This application uses **Git tags** for versioning production releases. Users with auto-update enabled will automatically receive tagged releases.

---

## Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

**Format:** `vMAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0) - Breaking changes, incompatible API changes
- **MINOR** (v1.1.0) - New features, backwards compatible
- **PATCH** (v1.0.1) - Bug fixes, backwards compatible

**Examples:**
- `v1.0.0` - Initial release
- `v1.1.0` - Added settings page (new feature)
- `v1.1.1` - Fixed progress bar bug (bug fix)
- `v2.0.0` - Changed database format (breaking change)

---

## Release Process

### 1. Prepare the Release

Ensure all changes are committed and tested:

```bash
# Check status
git status

# Run tests (if available)
pytest

# Verify all features work
# - Create project
# - Generate flashcards
# - Study session
# - Settings work
```

### 2. Update Version Documentation

Update relevant files:

```bash
# Update README.md with new features
# Update CHANGELOG.md with release notes
# Update any version-specific documentation
```

### 3. Create the Release Tag

```bash
# Create annotated tag with message
git tag -a v1.1.0 -m "Release v1.1.0 - Settings page and auto-update"

# Verify tag was created
git tag -l

# Show tag details
git show v1.1.0
```

### 4. Push the Tag to Remote

```bash
# Push the tag to origin
git push origin v1.1.0

# Or push all tags
git push --tags
```

### 5. Create GitHub Release (Optional but Recommended)

If using GitHub:

1. Go to repository → Releases → Create new release
2. Choose the tag you just created (v1.1.0)
3. Title: "Release v1.1.0"
4. Description: Add release notes (features, fixes, breaking changes)
5. Attach binaries if needed
6. Publish release

---

## Release Notes Template

```markdown
## Release v1.1.0

### New Features
- ✨ Added settings page with gear icon in navbar
- ✨ API key management from UI
- ✨ Auto-update system for production releases
- ✨ Configurable default values

### Improvements  
- 🚀 Faster flashcard generation with progress tracking
- 🎨 Better UI for file upload with progress bar

### Bug Fixes
- 🐛 Fixed session persistence after exit
- 🐛 Fixed progress bar jumping to 90% immediately
- 🐛 Fixed flash message showing 0 flashcards

### Breaking Changes
- None

### Migration Notes
- Settings now stored in settings.json
- OpenAI key location unchanged
- All existing projects compatible
```

---

## What Happens When Users Update

### Auto-Update Enabled

```
1. User starts app (start_flashcards.bat)
2. Script fetches tags: git fetch --tags
3. Compares current tag vs latest tag
4. If new version: git checkout v1.1.0
5. App starts with new version
```

### Manual Update from Settings

```
1. User clicks "Check for Updates Now"
2. Frontend calls /check-updates
3. Backend compares current tag vs latest remote tag
4. Shows: "Update available: v1.0.0 → v1.1.0"
5. User clicks "Install Version v1.1.0"
6. Backend: git checkout v1.1.0
7. Success message shown
8. User restarts app
```

---

## Testing a Release

### Before Tagging

```bash
# 1. Test on a clean checkout
git clone <repo-url> test-release
cd test-release
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Test all features
python app.py
# - Create projects
# - Generate flashcards
# - Study sessions
# - Settings page
# - Update check

# 3. Test update process
git tag -a v1.0.1 -m "Test release"
# Try updating to this tag
```

### After Tagging

```bash
# 1. Test on fresh install
git clone <repo-url> prod-test
cd prod-test

# 2. Checkout the release tag
git checkout v1.1.0

# 3. Verify it works
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## Rolling Back a Release

If a release has issues:

### Delete a Bad Tag

```bash
# Delete local tag
git tag -d v1.1.0

# Delete remote tag
git push origin :refs/tags/v1.1.0

# OR
git push --delete origin v1.1.0
```

### Users Can Roll Back

```bash
# List available versions
git tag -l

# Checkout previous version
git checkout v1.0.0
```

---

## Version History Tracking

### View All Releases

```bash
# List all tags
git tag -l --sort=-v:refname

# Show details for a tag
git show v1.1.0

# Compare two versions
git diff v1.0.0..v1.1.0

# See commits between versions
git log v1.0.0..v1.1.0 --oneline
```

---

## Hotfix Releases

For urgent bug fixes:

```bash
# Create hotfix branch from tag
git checkout -b hotfix-1.1.1 v1.1.0

# Make fixes
# ... edit files ...
git commit -am "Fix critical bug"

# Create new patch version
git tag -a v1.1.1 -m "Hotfix: Critical bug fix"

# Push
git push origin hotfix-1.1.1
git push origin v1.1.1

# Merge back to main
git checkout main
git merge hotfix-1.1.1
git push origin main
```

---

## Best Practices

### DO:
- ✅ Test thoroughly before tagging
- ✅ Use semantic versioning
- ✅ Write clear release notes
- ✅ Tag from main/master branch
- ✅ Keep tags immutable (don't move them)
- ✅ Document breaking changes
- ✅ Update CHANGELOG.md

### DON'T:
- ❌ Tag unfinished features
- ❌ Tag directly from feature branches
- ❌ Delete tags that users might be on
- ❌ Force push after creating tags
- ❌ Skip version numbers
- ❌ Release without testing

---

## Example Release Workflow

```bash
# 1. Ensure you're on main with latest code
git checkout main
git pull origin main

# 2. Verify everything is committed
git status
# Should show "nothing to commit, working tree clean"

# 3. Test the application
python app.py
# Test all features thoroughly

# 4. Create the release tag
git tag -a v1.1.0 -m "Release v1.1.0 - Settings and Auto-Update

New Features:
- Settings page with API key management
- Auto-update system for production releases
- Configurable default values

Bug Fixes:
- Session persistence after exit
- Progress bar accuracy

See CHANGELOG.md for details."

# 5. Push the tag
git push origin v1.1.0

# 6. Verify on GitHub
# Check that the tag appears in Releases

# 7. Announce (if public)
# Post to discussions, social media, etc.

# Done! Users with auto-update will get it next startup.
```

---

## Monitoring Releases

### Check Who's Using What Version

Users can report their version from Settings page.

### Track Issues by Version

```bash
# Find commits that introduced a bug
git bisect start
git bisect bad v1.1.0
git bisect good v1.0.0
# Follow prompts to find problematic commit
```

---

## Questions?

- **When to release?** After significant features or important bug fixes
- **How often?** As needed - balance stability vs features
- **Who can release?** Repository maintainers with push access
- **Can I update a tag?** No - tags should be immutable. Create a new version instead.

---

**Remember:** Users trust that tagged releases are stable and production-ready!

