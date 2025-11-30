# Enhanced Project Creation Guide

## Overview

The project creation system has been significantly enhanced to give you **full control** over how flashcards are generated from your documents.

## 🎯 Key Features

### 1. **Two Topic Organization Strategies**

#### 📄 One Topic Per File (Recommended)
- **Best for:** Lesson-based content, structured courses, individual chapters
- **How it works:** Each uploaded file becomes its own topic
- **Example:** Upload 32 lesson files → Get 32 topics (one per lesson)
- **Benefits:**
  - Perfect organization for course materials
  - Easy to track progress per lesson
  - Clear topic names based on filenames

#### 🤖 AI-Extracted Topics
- **Best for:** Single large documents, unstructured content, mixed materials
- **How it works:** AI analyzes all content and extracts 3-8 key themes
- **Example:** Upload a textbook → Get topics like "Introduction", "Advanced Concepts", etc.
- **Benefits:**
  - Consolidates related content across files
  - Identifies cross-cutting themes
  - Good for broader topic organization

### 2. **Full Customization Control**

For each topic (regardless of strategy), you can customize:
- ✏️ **Topic Name:** Edit the suggested name or create your own
- 🔢 **Flashcard Count:** Set exactly how many cards per topic (5-50)
- 👁️ **Preview:** See file names, text size, and estimated processing time

### 3. **Improved AI Project Naming**

The AI now:
- ✅ Considers content from **all uploaded documents** (not just one)
- ✅ Detects course titles and certification names
- ✅ Generates descriptive names like "Scrum Product Owner Certification"
- ✅ Fully editable - change the suggestion if you prefer

### 4. **Simple Filename Processing**

When using "One Topic Per File":
- Removes only the file extension (.txt, .pdf, .docx)
- Keeps everything else exactly as you named it (spaces, numbers, etc.)
- Example: "Lesson 01 Roles in a Scrum Project.txt" → Topic: "Lesson 01 Roles in a Scrum Project"

## 📋 Step-by-Step Guide

### Step 1: Upload Documents

1. Navigate to **Projects → Create Project from Documents**
2. **Drag and drop** your files, or click "Select Files"
3. Upload any combination of:
   - PDF files (.pdf)
   - Word documents (.docx)
   - Text files (.txt)
4. Click **🚀 Process Documents**

### Step 2: Configure Your Project

After processing, you'll see a configuration screen:

#### A. Set Project Name
- Review the AI-suggested name
- Edit it if needed (3-6 words recommended)
- This will be your project identifier

#### B. Choose Topic Strategy

**Option 1: One Topic Per File** (Recommended for your use case)
- Each file = One topic
- You'll see a list of all files with:
  - Original filename
  - Suggested topic name (cleaned from filename)
  - Default 25 flashcards per topic
- Customize each:
  - Edit topic names
  - Adjust flashcard counts (5-50 per topic)
  - See total count update in real-time

**Option 2: AI-Extracted Topics**
- AI analyzes ALL content together
- Extracts 3-8 key themes
- Shows suggested topics with flashcard counts
- Customize:
  - Edit topic names
  - Adjust flashcard counts per topic

### Step 3: Review & Create

- Check the summary (total topics, total flashcards)
- Click **🚀 Create Project & Generate Flashcards**
- Wait while AI generates:
  - Questions tailored to each topic
  - Multiple question types (True/False, Multiple Choice, etc.)
  - **Detailed explanations** for every answer
- Typical timing: ~30-60 seconds per topic

### Step 4: Start Learning!

Once created, you'll be redirected to start your first study session!

## 💡 Best Practices

### For Course Materials (Like Your 32 Lessons)

1. **Use "One Topic Per File"** strategy
2. **Upload all lessons together** (the system handles any number)
3. **Review auto-generated topic names** - they're cleaned from filenames
4. **Adjust flashcard counts:**
   - Shorter lessons: 10-15 cards
   - Standard lessons: 20-25 cards
   - Complex lessons: 30-40 cards
5. **Project name suggestion:** Will detect it's a course and suggest accordingly

### For Mixed Content

1. Try **"AI-Extracted Topics"** first to see what themes emerge
2. Review the 3-8 suggested topics
3. Customize names to be more specific
4. Adjust card counts based on topic importance

### Flashcard Count Guidelines

- **5-10 cards:** Quick overviews, simple topics
- **15-25 cards:** Standard lessons, moderate complexity
- **30-50 cards:** Complex topics, comprehensive coverage
- **Per topic:** AI generates a mix of question types automatically

## 🎨 What You'll Get

Every generated flashcard includes:
- ✅ **Question:** Thoughtfully crafted from your content
- ✅ **Answer:** Properly formatted (True/False, A/B/C/D, etc.)
- ✅ **Question Type:** Auto-detected and labeled
- ✅ **Options:** For multiple choice questions
- ✅ **Explanation:** 1-2 sentences explaining WHY (new feature!)

## 🔄 Example Workflow

**Your Scenario: 32 Scrum Certification Lessons**

1. **Upload:** Drag all 32 .txt files at once
2. **Strategy:** Select "One Topic Per File"
3. **Review:** See all 32 lessons listed
   - "Lesson 01 Roles in a Scrum Project.txt" → Topic: "Lesson 01 Roles in a Scrum Project"
   - "Lesson 02 The Product Vision.txt" → Topic: "Lesson 02 The Product Vision"
   - Etc. (extension removed, everything else preserved)
4. **Customize:** 
   - Keep topic names as-is or edit them
   - Set 25 cards per lesson = 800 total cards
5. **Project Name:** AI suggests "Scrum Product Owner Certification"
6. **Create:** Click button, wait ~30-40 minutes for 800 cards
7. **Result:** One organized project with 32 topics!

## ⚙️ Technical Details

### File Processing
- Text extracted from each file separately
- No data loss or corruption
- Original files preserved in project folder
- Each topic generated from its source file's content

### AI Generation
- Uses GPT-4o for flashcard quality
- Maintains context per topic/file
- Generates explanations automatically
- Ensures question type variety

### Data Storage
```
projects/
└── your-project-name/
    ├── project.json (metadata)
    ├── flashcards.json (all generated cards)
    ├── mastery.json (your progress)
    ├── history.json (session stats)
    └── documents/
        ├── Lesson 01 Roles in a Scrum Project.txt
        ├── Lesson 02 The Product Vision.txt
        └── ... (all your source files)
```

## 🚀 Performance Notes

- **Processing:** ~2-3 seconds per file for text extraction
- **AI Generation:** ~30-60 seconds per topic
- **Total Time:** For 32 topics ≈ 30-40 minutes
- **Progress:** Loading overlay shows status during generation
- **Safe:** You can close browser - server continues processing

## ⚠️ Important Notes

1. **Be Patient:** Large projects (30+ topics) take time
2. **Don't Refresh:** During "Creating Project" screen
3. **Check Results:** Review flashcards after creation
4. **Regenerate if Needed:** Can always create a new project if not satisfied

## 🆕 What's New

Compared to the old system:
- ✅ No longer combines all files into one text blob
- ✅ One topic per file instead of 6 random topics total
- ✅ Full customization before generation
- ✅ Better project name detection
- ✅ Per-topic flashcard count control
- ✅ AI-generated explanations included
- ✅ Two strategies to choose from

---

**This update specifically addresses your feedback about wanting one topic per file for your lesson-based content!** 🎉

