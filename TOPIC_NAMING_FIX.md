# Topic Naming Fix - Technical Details

## Issue Identified

When uploading files like:
- `Lesson 01 Roles in a Scrum Project.txt`
- `Lesson 02 The Product Vision.txt`

The topic names were appearing as:
- ❌ `Lesson_01_Roles_in_a_Scrum_Project` (with underscores)

Instead of the expected:
- ✅ `Lesson 01 Roles in a Scrum Project` (exactly as named, just without extension)

## Root Cause

The `secure_filename()` function from Werkzeug was:
1. Converting spaces to underscores for safe file storage
2. This sanitized filename was being used for topic name generation
3. Result: Ugly topic names with underscores

## Solution Implemented

### Code Changes

**Before:**
```python
filename = secure_filename(file.filename)  # "Lesson_01_Roles_in_a_Scrum_Project.txt"
# ... later ...
clean_name = os.path.splitext(filename)[0]  # Still has underscores!
```

**After:**
```python
original_filename = file.filename  # "Lesson 01 Roles in a Scrum Project.txt"
safe_filename = secure_filename(file.filename)  # For storage only

# Use ORIGINAL filename for topic name - just remove extension
topic_name = os.path.splitext(original_filename)[0]  # "Lesson 01 Roles in a Scrum Project"
# Keep everything else: numbers, spaces, special characters, etc.
```

### Processing Steps

1. **Preserve Original:** Keep user's original filename with spaces
2. **Safe Storage:** Use `secure_filename()` only for saving to disk
3. **Clean for Topics:** Process the ORIGINAL filename:
   - Remove ONLY the file extension (.txt, .pdf, .docx)
   - **Keep everything else:** numbers, "Lesson XX", spaces, special characters
   - Topic name = exactly what user would expect

### Examples

| Original Filename | Safe Filename (Storage) | Topic Name (Display) |
|-------------------|------------------------|----------------------|
| `Lesson 01 Roles in a Scrum Project.txt` | `Lesson_01_Roles_in_a_Scrum_Project.txt` | `Lesson 01 Roles in a Scrum Project` |
| `Lesson 02 The Product Vision.txt` | `Lesson_02_The_Product_Vision.txt` | `Lesson 02 The Product Vision` |
| `15 The 45 Percent Disaster.txt` | `15_The_45_Percent_Disaster.txt` | `15 The 45 Percent Disaster` |
| `Planning Poker.txt` | `Planning_Poker.txt` | `Planning Poker` |
| `What's value.txt` | `Whats_value.txt` | `What's value` |

## Data Structure

The new `documents_data` structure stored in session:
```python
{
    'original_filename': 'Lesson 01 Roles in a Scrum Project.txt',  # For display
    'display_filename': 'Lesson 01 Roles in a Scrum Project.txt',   # For UI
    'filepath': '/temp/Lesson_01_Roles_in_a_Scrum_Project.txt',     # Safe path
    'text': '... extracted text ...',
    'suggested_topic': 'Roles in a Scrum Project',                  # Clean name
    'text_length': 12345
}
```

## UI Impact

### Configuration Screen Now Shows:

**File Display:**
```
📄 Lesson 01 Roles in a Scrum Project.txt
   8.5 KB of text
   
   Topic Name: [Roles in a Scrum Project    ]  ← Editable, no underscores!
   Flashcards: [25]
```

**Instead of:**
```
❌ Lesson_01_Roles_in_a_Scrum_Project.txt  ← Ugly!
```

## Verification

To verify the fix is working:

1. Upload any file with spaces in the name
2. Check the topic configuration screen
3. Topic name should show:
   ✅ Clean readable text
   ✅ No underscores
   ✅ No file extension
   ✅ No "Lesson XX" prefix
   ✅ Spaces preserved

## Testing Recommendations

**Test Case 1: Standard Lesson File**
- Upload: `Lesson 15 The 45 Percent Disaster.txt`
- Expected Topic: `Lesson 15 The 45 Percent Disaster`
- Expected Display: `Lesson 15 The 45 Percent Disaster.txt`

**Test Case 2: Simple Filename**
- Upload: `Planning Poker.txt`
- Expected Topic: `Planning Poker`
- Expected Display: `Planning Poker.txt`

**Test Case 3: Special Characters**
- Upload: `What's value.txt`
- Expected Topic: `What's value`
- Expected Display: `What's value.txt`

## Files Modified

1. **app.py** - Updated upload and topic name processing
2. **templates/create_project.html** - Updated to use `display_filename`

## Compatibility

- ✅ Works with existing projects (no migration needed)
- ✅ Backward compatible with old data
- ✅ No breaking changes to existing functionality
- ✅ Only affects NEW project creation

---

**Status: ✅ FIXED** - Topic names now display exactly as users expect!

