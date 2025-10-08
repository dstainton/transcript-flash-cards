# Transcript Flash Cards

This flash card application helps users learn and test their knowledge based on questions generated from video transcripts. It generates flashcards using the OpenAI API and provides both study and exam modes. Answers are assessed using the OpenAI API too, so no more wrong answers because of a typo!

## Features

- **Transcript Processing:** 
  - Reads video transcripts from the `transcripts/` folder and generates flashcards
  - Optional `Topic.txt` file to provide context for flashcard generation
  - Saves generated flashcards to avoid regeneration
- **Answer Types:**
  - True/False statements
  - Yes/No questions
  - Multiple Choice (single answer)
  - Multiple Answer (select all that apply)
- **Configurable Settings:** 
  - Customize the number of cards
  - Adjust time limits
  - Select specific topics
- **Study Mode:** 
  - Presents flashcards in random order
  - Focuses on cards not answered correctly
  - Immediate feedback after each answer
  - Retires cards after three correct answers
- **Exam Mode:** 
  - Simulates an exam environment
  - Configurable time limit
  - Delayed scoring
  - Detailed results review
- **Statistics:** 
  - Tracks scores by topic and session
  - Maintains exam history
  - Maintains study session history
  - Shows success rates and progress
- **Modern Interface:**
  - Responsive design
  - Progress indicators
  - Timer display
  - Clean, card-based layout

## Quick Start (Windows)

### Easy Method - Double-Click to Start

1. **Prerequisites:**
   - Install Python 3.7 or higher from [python.org](https://www.python.org/)
   - Ensure "Add Python to PATH" is checked during installation

2. **Setup:**
   - Create a file named `openaikey.txt` in the root directory
   - Add your OpenAI API key to this file

3. **Run:**
   - Double-click `start_flashcards.bat`
   - The script will:
     - Create an isolated virtual environment (`.venv`) 
     - Install all required dependencies
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

5. **Add Transcripts:**
   - Create a `transcripts/` folder
   - Add your `.txt` transcript files
   - Optionally add a `Topic.txt` file with the main topic

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

1. **Start Page:**
   - Select topics to study
   - Choose study or exam mode
   - Configure time settings
   - Set exam question limits (exam mode only)

2. **Study Mode:**
   - View question and timer
   - Submit answer
   - Get immediate feedback
   - Cards retire after three correct answers

3. **Exam Mode:**
   - Answer questions within time limit
   - No immediate feedback
   - Review all answers at the end
   - See detailed results and statistics

4. **Statistics:**
   - View exam history
   - Track study progress
   - Monitor success rates
   - Review topic performance

## File Structure

```
transcript-flash-cards/
├── app.py                    # Main application file
├── start_flashcards.bat      # Windows launcher (auto-setup)
├── stop_flashcards.bat       # Windows stop script
├── requirements.txt          # Python dependencies
├── openaikey.txt             # OpenAI API key (create this)
├── secret_key.txt            # Auto-generated session key
├── .venv/                    # Virtual environment (auto-created)
├── .flask_session/           # Server-side session data
├── static/
│   └── style.css            # Application styling
├── templates/         
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── start.html           # Session configuration
│   ├── flashcard_scroll.html # Card display with scrolling
│   ├── results.html         # Session results
│   └── stats.html           # Statistics display
├── transcripts/
│   ├── Topic.txt            # Optional main topic context
│   └── *.txt                # Video transcript files
├── flashcards.json          # Generated flashcards cache
└── history.json             # Session history data
```

## Data Persistence

- **Flashcards:** Saved to `flashcards.json`
- **History:** Saved to `history.json`
- **Session:** Managed via Flask sessions
- **Secret Key:** Stored in `secret_key.txt`

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

## Known Limitations

- Session timeout after 30 minutes
- Requires active internet connection for API calls
- Limited to text-based answers
