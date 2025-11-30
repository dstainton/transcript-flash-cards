# Session Persistence Fix - Current Project Selection

## Problem Identified

After creating a new project and using it in a study session:
1. User creates new project → Project is set as current ✓
2. User starts session with new project → Works correctly ✓
3. User answers flashcards → Works correctly ✓
4. User clicks "Exit Session" → Session cleared ❌
5. User returns to start page → **Previous project is now selected instead of the new one!**

## Root Cause

The `exit()` function (line 2048) was calling `session.clear()` which cleared **ALL** session data, including:
- `current_project_id` - The user's selected project
- `creation_success` - Success message for newly created projects
- `pending_project` - Temporary data during project creation

**Before:**
```python
@app.route('/exit', methods=['POST'])
def exit():
    # ... save history ...
    
    session.clear()  # ❌ Clears EVERYTHING including current_project_id
    return redirect(url_for('index'))
```

When the user returned to the start page, `get_current_project()` couldn't find a `current_project_id` in the session, so it defaulted to the first project in the list (alphabetically).

## Solution Implemented

Modified the `exit()` function to preserve persistent session data while clearing temporary session data:

**After:**
```python
@app.route('/exit', methods=['POST'])
def exit():
    # ... save history ...
    
    # Preserve current project selection and other persistent session data
    current_project_id = session.get('current_project_id')
    creation_success = session.get('creation_success')
    pending_project = session.get('pending_project')
    
    # Clear session data
    session.clear()
    
    # Restore persistent data
    if current_project_id:
        session['current_project_id'] = current_project_id
    if creation_success:
        session['creation_success'] = creation_success
    if pending_project:
        session['pending_project'] = pending_project
    
    return redirect(url_for('index'))
```

## What Gets Cleared

Session data that SHOULD be cleared when exiting a study session:
- ✅ `mode` - Study or exam mode
- ✅ `flashcards` - Current session's flashcards
- ✅ `current_card_index` - Progress through cards
- ✅ `score` - Current session score
- ✅ `user_answers` - Answers given in this session
- ✅ `exam_questions` - Exam questions for this session
- ✅ `completed_cards` - Cards completed in this session
- ✅ `start_time` - Session start time
- ✅ `topics` - Selected topics for this session

## What Gets Preserved

Session data that should PERSIST across study sessions:
- ✅ `current_project_id` - User's selected project
- ✅ `creation_success` - Success message for newly created projects
- ✅ `pending_project` - Temporary data during project creation workflow

## User Experience Improvements

### Before:
```
1. Create "Scrum Certification" project
2. Start session with "Scrum Certification" ✓
3. Answer 5 flashcards ✓
4. Exit session
5. Return to start page
   Current project: "My Flash Cards" (old project) ❌
```

**User thinks:** "Where did my new project go? I have to select it again every time!"

### After:
```
1. Create "Scrum Certification" project
2. Start session with "Scrum Certification" ✓
3. Answer 5 flashcards ✓
4. Exit session
5. Return to start page
   Current project: "Scrum Certification" ✓
```

**User thinks:** "Perfect! My project selection is remembered."

## Benefits

1. ✅ **Persistent project selection** - User's chosen project remains selected across sessions
2. ✅ **Better UX** - Users don't have to re-select their project every time
3. ✅ **Logical behavior** - Project selection is independent of study sessions
4. ✅ **Preserves workflow** - New project creation flow isn't interrupted

## Testing

1. Create a new project from documents
2. Start a study session with the new project
3. Answer a few flashcards
4. Click "Exit Session"
5. Click "Get Started" or return to start page
6. ✅ Verify new project is still selected in dropdown
7. ✅ Verify you can start another session with the same project without re-selecting

## Files Modified

- `app.py`: Updated `exit()` function to preserve persistent session data

## Related Issues

This fix also ensures that:
- Users who switch projects during use maintain their selection
- Project creation workflow isn't interrupted by session management
- Success messages for newly created projects are preserved

