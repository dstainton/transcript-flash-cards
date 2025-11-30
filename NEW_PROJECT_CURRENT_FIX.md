# New Project Set as Current - Fix

## Issue Identified

When a new project was created, there were two related problems:

1. **Project WAS being set as current** ✓ (this was actually working)
2. **Flash message showed incorrect count** ❌ - "Project created with 0 flashcards"
3. **Timing issue** - Flash message was created before background generation completed

## Root Cause

The flow was:
1. User submits project configuration
2. Server creates project and sets it as current ✓
3. Background thread starts generating flashcards
4. Server returns immediately with `progress_id`
5. Server creates flash message with `flashcard_count: 0` ❌
6. Frontend waits for generation to complete
7. Frontend redirects to `/start`
8. User sees "Project created with 0 flashcards" (confusing!)

The project WAS set as current, but the flash message was misleading.

## Solution Implemented

### Backend Changes (`app.py`)

1. **Added final counts to progress data** when generation completes:
```python
creation_progress[progress_id]['project_name'] = project_name
creation_progress[progress_id]['flashcards_generated'] = total_flashcards_generated
creation_progress[progress_id]['topic_count'] = num_topics
```

2. **Removed premature flash message creation** - no longer create `creation_success` with 0 count

3. **Added new endpoint** `/update-creation-success` to update session with actual counts after generation:
```python
@app.route('/update-creation-success', methods=['POST'])
def update_creation_success():
    session['creation_success'] = {
        'project_name': data['project_name'],
        'flashcard_count': data['flashcard_count'],
        'topic_count': data['topic_count'],
        'progress_id': data['progress_id']
    }
```

### Frontend Changes (`templates/create_project.html`)

When generation completes (status === 'complete'):
1. **Fetch final counts** from progress data
2. **Update session** via `/update-creation-success` endpoint
3. **Then redirect** to `/start` page

```javascript
// Update session with final counts
fetch('/update-creation-success', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        project_name: progress.project_name,
        flashcard_count: progress.flashcards_generated,
        topic_count: progress.topic_count,
        progress_id: progressId
    })
}).then(() => {
    // Redirect after updating session
    setTimeout(() => {
        window.location.href = `/start`;
    }, 1500);
});
```

## User Experience Improvements

### Before:
```
[Progress completes]
✅ Project created successfully!
Generated 105 flashcards across 7 topics

[Redirects to /start page]

Flash message: "Project 'My Project' created with 0 flashcards across 7 topics!"
```

**User thinks:** "Wait, it said 105 but now it says 0? Is something wrong?"

### After:
```
[Progress completes]
✅ Project created successfully!
Generated 105 flashcards across 7 topics

[Updates session with correct counts]
[Redirects to /start page]

Flash message: "Project 'My Project' created with 105 flashcards across 7 topics!"
```

**User thinks:** "Perfect! My project is ready with all the flashcards."

## What's Confirmed Working

1. ✅ **New project IS set as current** - This was already working correctly
2. ✅ **Flash message shows correct count** - Now updated after generation completes
3. ✅ **Project loads with all flashcards** - Background generation completes before redirect
4. ✅ **User sees accurate information** - No more confusing "0 flashcards" message

## Files Modified

- `app.py`:
  - Updated `_generate_flashcards_background()` to store final counts in progress
  - Removed premature `creation_success` initialization
  - Added `/update-creation-success` endpoint

- `templates/create_project.html`:
  - Modified completion handler to update session before redirecting
  - Sends final counts to server for flash message

## Testing

1. Create a new project from documents
2. Wait for flashcard generation to complete
3. Verify flash message shows actual flashcard count (not 0)
4. Verify new project is selected as current
5. Verify all flashcards are visible in the project

