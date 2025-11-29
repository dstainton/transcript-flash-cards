# Card Mastery System - User Guide

## Overview

The flashcard app now includes a comprehensive **Card Mastery System** that tracks your learning progress across all topics. This system helps you focus on cards you haven't mastered yet and celebrates your achievements when you do master them!

## How Card Mastery Works

### 🎯 The 3-Strike Rule

A flashcard becomes **"mastered"** when you answer it correctly **3 times in a row** during study sessions.

- ✅ Answer correctly once → Streak: 1/3
- ✅ Answer correctly again → Streak: 2/3  
- ✅ Answer correctly a third time → 🎉 **MASTERED!**
- ❌ Answer incorrectly → Streak resets to 0/3

### 📊 Real-Time Feedback

While studying, you'll see visual feedback on every answer:

- **Correct answers**: "✅ Correct! 🔥 Streak: 2/3"
- **Mastered cards**: "✅ Correct! 🎉 CARD MASTERED! You answered correctly 3 times in a row!"
- **Incorrect answers**: "❌ Incorrect. 🔄 Streak reset to 0/3"
- **💡 Explanations**: Every answer (correct or incorrect) includes an AI-generated explanation to help you understand the concept better

### 💾 Persistent Progress

**Mastered cards stay mastered!** Your progress is saved permanently in `mastery.json`, so:

- When you start a new study session, mastered cards are automatically filtered out
- You won't waste time re-studying cards you've already learned
- Your progress persists even if you close the app and come back days later

## Using the Mastery System

### 1. Starting a Study Session

When you click "Get Started" and select topics:

- Each topic shows how many cards you've mastered (e.g., "15/25 mastered")
- Topics with all cards mastered show a green checkmark ✓
- Topics with some mastered cards show a refresh icon ⟳
- Only unmastered cards will appear in your study session

### 2. During Study

At the top of each flashcard, you'll see:

- **Progress**: "Question 5 / 25"
- **Cards Mastered**: "🎉 3 mastered" (shows how many you've mastered this session)
- **Remaining**: "22 remaining" (how many cards are left in this session)

### 3. Session Results

After completing a study session, the results page shows:

- Your score and percentage
- **Cards Mastered**: How many cards you mastered in this session
- A note: "Mastered cards won't appear in future sessions"

### 4. Viewing Mastery Progress

Click **"Mastery"** in the navigation bar to see:

- **Overall Progress**: Total cards mastered across all topics with a visual progress bar
- **Progress by Topic**: Detailed breakdown showing:
  - Topic name
  - Visual progress bar
  - Cards mastered (e.g., "18/25")
  - Percentage complete
  - Reset button (if you want to study that topic again)

### 5. Resetting Mastery

If you want to review topics you've already mastered:

1. Go to the **Mastery** page
2. Find the topic you want to reset
3. Click the **"Reset"** button
4. Confirm the action
5. All cards for that topic will become available for study again

⚠️ **Warning**: Resetting is permanent! You'll lose all mastery progress for that topic.

## Files Created/Modified

### New Files
- `mastery.json` - Stores your mastery progress (auto-created on first use)
- `templates/mastery.html` - Mastery statistics page
- `MASTERY_SYSTEM_GUIDE.md` - This guide

### Modified Files
- `app.py` - Added mastery tracking logic and routes
- `templates/flashcard_scroll.html` - Added mastery indicators
- `templates/results.html` - Shows cards mastered in session
- `templates/start.html` - Shows mastery progress per topic
- `templates/base.html` - Added Mastery link and flash messages
- `templates/index.html` - Added Mastery button
- `static/style.css` - Added mastery-related styles

## Key Features

### ✨ Smart Filtering
- Mastered cards automatically excluded from study sessions
- Focuses your time on cards you need to learn

### 📈 Progress Tracking
- See exactly how many cards you've mastered per topic
- Visual progress bars make it easy to track your learning

### 🎉 Motivational Feedback
- Celebration messages when you master a card
- Real-time streak tracking keeps you engaged
- Visual badges show your achievements

### 🔄 Flexible Reset
- Can reset individual topics if you want to review
- Complete control over your learning journey

## Tips for Effective Learning

1. **Focus on One Topic**: Select a single topic to concentrate your learning
2. **Study Regularly**: Short, frequent sessions are more effective than long cramming sessions
3. **Review Periodically**: Even mastered cards can be forgotten - use the reset feature to review
4. **Track Progress**: Use the Mastery page to identify which topics need more attention
5. **Celebrate Milestones**: When you fully master a topic, take a moment to appreciate your progress!

## Technical Details

### Mastery Storage
- Mastery data stored in `mastery.json`
- Uses MD5 hashing of questions to uniquely identify cards
- Stores: question text, topic, filename, and mastery date
- Survives app restarts and updates

### Streak Tracking
- Tracked per-session using Flask session storage
- Uses card hash to identify specific cards
- Resets to 0 on incorrect answer
- Increments by 1 on correct answer
- Triggers mastery at streak = 3

### Exam Mode vs Study Mode
- **Exam Mode**: Mastery system does NOT apply (cards not filtered or tracked)
- **Study Mode**: Full mastery system active (filtering, tracking, persistence)

## Troubleshooting

### Mastered cards still appearing?
- Make sure you're in Study Mode (not Exam Mode)
- Check that you didn't select "All Topics" which might include other unmastered cards
- Verify mastery.json exists and has content

### Progress not saving?
- Ensure the app has write permissions in its directory
- Check that mastery.json is being created/updated
- Don't close the app immediately after mastering a card (give it a second to save)

### Want to start fresh?
- Delete `mastery.json` to clear all mastery progress
- Or use the Reset button on specific topics

## Future Enhancements (Ideas)

- Spaced repetition reminders for mastered cards
- Export mastery progress reports
- Mastery streaks and achievements
- Study time tracking per topic
- Difficulty ratings for cards
- Custom mastery thresholds (e.g., 5 correct instead of 3)

---

**Enjoy your enhanced learning experience! 🎓📚**

