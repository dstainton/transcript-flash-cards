# Transcript Flash Cards

This flash card application helps users learn and test their knowledge based on questions generated from documents. It generates flashcards using the OpenAI API and provides both study and exam modes. Answers are assessed using the OpenAI API too, so no more wrong answers because of a typo!

## Features

- **🗂️ Multi-Project Management:**
  - Create and manage multiple flashcard projects
  - Each project has its own flashcards, statistics, and mastery tracking
  - Switch between projects seamlessly
  - Delete projects when no longer needed
  
- **📁 Drag & Drop Project Creation:**
  - Simply drag and drop documents (PDF, Word, or Text files) to create a new project
  - **Two topic strategies:** One topic per file (perfect for lessons) OR AI-extracted topics
  - **Full customization:** Edit topic names and flashcard counts before generation
  - AI automatically generates a descriptive project name from all your content
  - Clean, intuitive configuration UI
  
- **🤖 AI-Powered Generation:**
  - Automatic flashcard generation from document content
  - Smart topic extraction and categorization
  - Configurable flashcard counts per topic
  - Intelligent question type selection (True/False, Yes/No, Multiple Choice, Multiple Answer)
  - AI-generated explanations for every answer to enhance learning
  
- **Answer Types:**
  - True/False statements
  - Yes/No questions
  - Multiple Choice (single answer)
  - Multiple Answer (select all that apply)
  
- **Configurable Settings:** 
  - Customize the number of cards per session
  - Adjust time limits
  - Select specific topics to study
  - Choose between study and exam modes
  
- **📚 Study Mode:** 
  - Presents flashcards in random order
  - Focuses on cards not answered correctly
  - Immediate feedback after each answer with detailed explanations
  - AI-generated explanations help you understand WHY answers are correct or incorrect
  - Smart mastery system - cards retire after consistent correct answers
  - Visual streak indicators and mastery notifications
  
- **📝 Exam Mode:** 
  - Simulates a real exam environment
  - Configurable time limit and question count
  - Delayed scoring (no immediate feedback)
  - Detailed results review after completion
  
- **📊 Statistics (Per Project):** 
  - Tracks scores by topic and session
  - Maintains exam history and study session history
  - Shows success rates and progress over time
  - Mastery progress visualization
  - Project-specific analytics
  
- **Modern Interface:**
  - Responsive, ADHD-friendly design
  - Progress indicators and visual feedback
  - Timer display with color-coded warnings
  - Clean, card-based layout
  - Drag-and-drop file upload

## Quick Start (Windows)

### Easy Method - Double-Click to Start

1. **Prerequisites:**
   - Install Python 3.7 or higher from [python.org](https://www.python.org/)
   - Ensure "Add Python to PATH" is checked during installation

2. **Setup:**
   - Create a file named `openaikey.txt` in the root directory
   - Add your OpenAI API key to this file
   - **Note:** If you have existing flashcards from a previous version, they will be automatically migrated to the new project structure on first run

3. **Run:**
   - Double-click `start_flashcards.bat`
   - The script will:
     - Create an isolated virtual environment (`.venv`) 
     - Install all required dependencies (including document processing libraries)
     - Automatically migrate existing data to the new project structure (if needed)
     - Start the Flask server
     - Automatically open your browser to http://localhost:5000

4. **Stop:**
   - Press `Ctrl+C` in the command window, or
   - Double-click `stop_flashcards.bat`

### Manual Installation (All Platforms)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dstainton/transcript-flash-cards.git
   cd transcript-flash-cards
   ```

2. **Create Virtual Environment (Recommended):**
   ```bash
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key:**
   - Create a file named `openaikey.txt` in the root directory
   - Add your OpenAI API key to this file
   - **Note:** If you have existing flashcards, they will be automatically migrated on first run

5. **Create Your First Project:**
   - Start the application
   - Click "Projects" in the header, then "Create Project from Documents"
   - Drag and drop your documents (PDF, Word, or text files)
   - Let AI analyze and create flashcards automatically
   - Alternatively, if migrating from an older version, your existing data will be preserved in a default project

## Configuration

- **Study Settings:**
  - Number of cards per transcript (`CARDS_PER_TRANSCRIPT`)
  - Time per card in seconds (`TIME_PER_CARD`)
  - Total exam time in seconds (`TOTAL_EXAM_TIME`)

## Running the Application

**Windows (Easy Method):**
- Double-click `start_flashcards.bat`

**Manual Method:**
```bash
# Activate virtual environment first (if using)
python app.py
```

Access the application at `http://localhost:5000/`

## Using the Application

1. **Creating Projects:**
   - Click "Projects" → "Create Project from Documents"
   - Drag and drop PDF, Word, or text files
   - AI analyzes content and suggests project name and topics
   - Review and create - flashcards are generated automatically

2. **Setup Your Session:**
   - Select your current project from the dropdown
   - Choose study mode or exam mode
   - Select specific topics to focus on
   - Configure time settings (if desired)
   - Set exam question limits (exam mode only)

3. **Study Mode:**
   - View questions with immediate timer feedback
   - Submit answers and get instant feedback
   - Track your streak - cards master after consistent correct answers
   - See mastery notifications and progress

4. **Exam Mode:**
   - Answer questions within the time limit
   - No immediate feedback during the exam
   - Review all answers at the end
   - See detailed results and statistics

5. **Managing Projects:**
   - Switch between projects easily
   - View project statistics (flashcards, mastery %, topics)
   - Delete projects when no longer needed
   - Each project maintains its own history and mastery data

6. **Tracking Progress:**
   - View per-project mastery progress
   - Check session-by-session statistics
   - Monitor success rates by topic
   - Track improvement over time

## File Structure

```
transcript-flash-cards/
├── app.py                      # Main application file
├── project_manager.py          # Project management logic
├── document_processor.py       # Document text extraction (PDF, DOCX, TXT)
├── migrate_to_projects.py      # Auto-migration script
├── start_flashcards.bat        # Windows launcher (auto-setup)
├── stop_flashcards.bat         # Windows stop script
├── CREATE_SHORTCUT.vbs         # Desktop shortcut creator
├── requirements.txt            # Python dependencies
├── openaikey.txt               # OpenAI API key (create this - never overwritten)
├── secret_key.txt              # Auto-generated session key (preserved)
├── .venv/                      # Virtual environment (auto-created)
├── .flask_session/             # Server-side session data
├── temp_uploads/               # Temporary storage for document uploads
├── static/
│   └── style.css              # Application styling
├── templates/         
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── start.html             # Session configuration
│   ├── flashcard_scroll.html  # Card display with scrolling
│   ├── results.html           # Session results
│   ├── stats.html             # Statistics display
│   ├── mastery.html           # Mastery progress view
│   ├── upload_documents.html  # Drag-and-drop upload UI
│   ├── create_project.html    # Project creation review
│   └── manage_projects.html   # Project management UI
└── projects/                   # Multi-project storage
    └── <project-id>/           # Each project has its own folder
        ├── project.json        # Project metadata
        ├── flashcards.json     # Project flashcards
        ├── history.json        # Session history
        ├── mastery.json        # Mastery tracking
        └── documents/          # Original source documents
```

### Legacy Files (Auto-Migrated)
If you have data from an older version, these files will be automatically migrated:
- `flashcards.json` → Moved to `projects/<default-project>/flashcards.json`
- `history.json` → Moved to `projects/<default-project>/history.json`
- `mastery.json` → Moved to `projects/<default-project>/mastery.json`
- `transcripts/` → Moved to `projects/<default-project>/documents/`

**Original files are backed up** with a `.backup` extension for safety.

## Data Persistence

- **Project Data:** Each project stores its own data in `projects/<project-id>/`
  - `flashcards.json` - Generated flashcards for the project
  - `history.json` - Study and exam session history
  - `mastery.json` - Mastery tracking per flashcard
  - `documents/` - Original source documents
  - `project.json` - Project metadata (name, ID, creation date)
- **Sessions:** Managed via server-side Flask sessions in `.flask_session/`
- **API Key:** Stored in `openaikey.txt` (never overwritten, must be created by user)
- **Secret Key:** Stored in `secret_key.txt` (auto-generated, preserved across updates)

**Important:** Your existing data is safe! The first time you run the updated version, any existing flashcards, history, and transcripts will be automatically migrated to a default project.

## Error Handling

- Validates all input data
- Handles API failures gracefully
- Provides user feedback for errors
- Maintains session stability

## Security

- Secure session management
- Protected API key storage
- Input validation and sanitization
- Error logging and monitoring

## Browser Compatibility

- Tested on modern browsers
- Responsive design for all screen sizes
- Graceful degradation for older browsers

## Additional Documentation

- **[What's New](WHATS_NEW.md)** - **📢 READ THIS!** Latest features and improvements
- **[Project Creation Guide](PROJECT_CREATION_GUIDE.md)** - **NEW!** Complete guide to creating projects with full control over topics and flashcard generation
- **[Flashcard Count Control](FLASHCARD_COUNT_CONTROL.md)** - **NEW!** How to use AI-suggested vs custom flashcard counts per topic
- **[Mastery System Guide](MASTERY_SYSTEM_GUIDE.md)** - Complete guide to the card mastery and spaced repetition system
- **[Answer Explanations Guide](EXPLANATION_FEATURE.md)** - How AI-generated explanations enhance your learning
- **[Installation Guide](INSTALLATION_GUIDE.md)** - Detailed installation instructions for all platforms
- **[Update Guide](UPDATE_GUIDE.md)** - How to update the application and preserve your data

## Known Limitations

- Session timeout after 30 minutes
- Requires active internet connection for API calls
- Limited to text-based answers
- Existing flashcards from before the explanation feature will show "No explanation available" (regenerate to get explanations)
