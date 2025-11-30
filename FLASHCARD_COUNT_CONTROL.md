# Intelligent Flashcard Count Control - User Guide

## Overview

The system now provides **sophisticated control** over flashcard generation with a perfect balance of AI intelligence and user customization.

## 🎯 How It Works

### Three Levels of Control

#### 1. **AI-Suggested Counts** (Default & Recommended)
- AI analyzes each document individually
- Considers:
  - Content length and complexity
  - Number of distinct concepts
  - Appropriate coverage for effective learning
- Suggests optimal count (5-50 cards)
- Provides reasoning for the suggestion

#### 2. **User Default Count**
- Set your own default (e.g., 25 cards per topic)
- Applied to all topics at once
- Quick way to standardize across files
- Still adjustable per topic

#### 3. **Per-Topic Customization**
- Every topic count is editable
- Works regardless of AI or default mode
- Fine-tune based on your knowledge
- Real-time total calculation

## 🎨 User Interface

### Configuration Screen Layout

```
┌─────────────────────────────────────────┐
│  Flashcard Count Settings               │
│  ○ Use AI Suggestions (recommended)     │
│  ○ Use My Default: [25] cards per topic │
│                                          │
│  💡 Tip: You can adjust individual      │
│  topic counts below either way          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📄 Lesson 01 Roles in a Scrum Project.txt
│    7.8 KB of text                        │
│                                          │
│ Topic Name: [Lesson 01 Roles in a...]   │
│ Flashcards: [18] 🤖 AI: 18              │
│ "Covers 3-4 key concepts effectively"   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📄 Lesson 02 The Product Vision.txt     │
│    5.2 KB of text                        │
│                                          │
│ Topic Name: [Lesson 02 The Product...]  │
│ Flashcards: [12] 🤖 AI: 12              │
│ "Concise content, optimal coverage"     │
└─────────────────────────────────────────┘

Total: 32 topics, 625 flashcards
```

## 📋 Usage Scenarios

### Scenario 1: Trust AI Completely (Default)

1. Upload your 32 lesson files
2. **Leave "Use AI Suggestions" selected** (default)
3. AI analyzes each file and sets optimal counts
   - Short lesson (5KB) → 12 cards
   - Standard lesson (8KB) → 20 cards
   - Complex lesson (12KB) → 30 cards
4. Review the suggestions
5. Adjust individual topics if you disagree
6. Create project

**Result:** Intelligent, content-appropriate flashcard distribution

### Scenario 2: Use Your Standard Default

1. Upload your files
2. Select **"Use My Default"**
3. Set your preferred number (e.g., 25)
4. All topics set to 25 cards
5. AI suggestions still visible for reference
6. Adjust individual topics if needed
7. Create project

**Result:** Consistent 25 cards per topic (or whatever you choose)

### Scenario 3: Hybrid Approach

1. Upload your files
2. Start with **"Use AI Suggestions"**
3. Review AI counts (shown next to each input)
4. **Manually adjust** specific topics:
   - Increase important topics: 18 → 30
   - Decrease simple topics: 25 → 15
5. Create project

**Result:** Best of both worlds - AI baseline + your expertise

### Scenario 4: Default as Maximum

While not automatic, you can achieve this:

1. Set default to your maximum (e.g., 30)
2. Select "Use My Default"
3. Manually review each topic
4. For topics where AI suggested less, reduce to AI value
5. For others, keep your maximum

**Result:** Capped distribution with AI guidance

## 🤖 AI Analysis Details

### What AI Considers

For each document, the AI evaluates:
- **Text length:** Word count and content volume
- **Complexity:** Technical depth and concept density
- **Topic scope:** Breadth of coverage
- **Learning efficiency:** Optimal number for retention without overwhelm

### AI Reasoning Examples

| Content Type | Suggested Count | Reasoning |
|--------------|----------------|-----------|
| Short intro (500 words) | 10 cards | "Brief overview with 2-3 key concepts" |
| Standard lesson (1500 words) | 20 cards | "Moderate complexity, balanced coverage" |
| Complex topic (3000 words) | 30 cards | "Dense content with multiple advanced concepts" |
| Simple reference (800 words) | 12 cards | "Straightforward content, focused scope" |

### Fallback Logic

If AI analysis fails:
- < 500 words → 10 cards
- 500-1500 words → 20 cards
- 1500+ words → 25 cards

## ⚙️ Technical Implementation

### AI Prompt

The system sends each file's content to GPT-4o-mini with:
```
Analyze this content and determine optimal flashcard count.
Consider: complexity, concepts, coverage, learning effectiveness.
Return: {"optimal_count": 15, "reasoning": "explanation"}
```

### Data Flow

1. **Upload**: Files uploaded and text extracted
2. **AI Analysis**: Each file analyzed for optimal count
3. **Storage**: Suggestions stored in session with reasoning
4. **Display**: UI shows AI counts + reasoning
5. **User Choice**: Select AI mode or default mode
6. **Adjustment**: Edit any individual count
7. **Generation**: Create flashcards with final counts

## 💡 Best Practices

### When to Use AI Suggestions

✅ **Use AI when:**
- You're unfamiliar with the content
- Files vary significantly in length/complexity
- You want optimal, data-driven distribution
- You trust AI to analyze content depth

### When to Use Your Default

✅ **Use Default when:**
- You know your content well
- You want consistent counts across all topics
- You have a specific study plan (e.g., always 20 cards)
- You prefer manual control

### When to Customize Per Topic

✅ **Customize when:**
- Some lessons are more important than others
- You already know some topics (fewer cards needed)
- Certain topics are exam-heavy (more cards needed)
- You want maximum precision

## 🎓 Example: 32-Lesson Course

### AI-Suggested Approach
```
Lesson 01 (Intro): 15 cards  (AI: "Foundational overview")
Lesson 02 (Vision): 12 cards (AI: "Concise, focused")
Lesson 03 (Backlog): 25 cards (AI: "Complex, detailed")
...
Lesson 32 (Budget): 18 cards (AI: "Practical application")

Total: ~625 cards (optimized distribution)
```

### User Default Approach
```
All 32 lessons: 25 cards each
Total: 800 cards (consistent)
```

### Hybrid Approach
```
Start with AI suggestions
Boost priority topics: +5-10 cards
Reduce known topics: -5-10 cards
Total: ~650 cards (personalized)
```

## ⚡ Quick Tips

1. **Default Mode:** Fastest setup - one number for all
2. **AI Mode:** Best for varied content - smart distribution
3. **Always Editable:** Change any count anytime before creating
4. **Live Totals:** See total flashcards update as you adjust
5. **Hover for Reasoning:** Mouse over AI badge to see why
6. **No Wrong Choice:** You can adjust counts later by recreating project

---

**This feature gives you complete control while leveraging AI intelligence!** 🎉

