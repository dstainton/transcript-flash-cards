# Transcript Flash Cards

This flash card application helps users learn and test their knowledge based on queestions generated from video transcripts. It generates flashcards using the OpenAI API and provides both study and exam modes. Answers are assessed using the OpenAI API too, so no more wrong answers because of a typo!

## Features

- **Transcript Processing:** Reads video transcripts from the `transcripts/` folder and generates flashcards.
- **Configurable Settings:** Customize the number of cards, time limits, and topics.
- **Study Mode:** Presents flashcards in random order and focuses on cards not answered correctly.
- **Exam Mode:** Simulates an exam environment with a total time limit and delayed scoring.
- **Scoring:** Tracks scores by topic, session, and maintains all-time scores.
- **Answer Checking:** Uses the OpenAI API to assess if answers are correct.
- **Graphical Interface:** Web-based interface with user-friendly controls.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/flashcard_app.git
   cd flashcard_app
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key:**

   - Obtain an API key from [OpenAI](https://openai.com/).
   - Set the `OPENAI_API_KEY` environment variable:

     ```bash
     export OPENAI_API_KEY='your-api-key'
     ```

4. **Add Transcripts:**

   - Place your `.txt` transcript files in the `transcripts/` folder.

## Configuration

- **Number of Cards per Transcript:**
  - Modify the `CARDS_PER_TRANSCRIPT` variable in `app.py` or set it via the interface.
- **Time Limits:**
  - **Per Card:** Adjust `TIME_PER_CARD` in seconds.
  - **Total Exam Time:** Adjust `TOTAL_EXAM_TIME` in seconds.
- **Topics Selection:**
  - Choose one or multiple topics on the start page to focus your study or exam session.

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open your web browser and navigate to `http://localhost:5000/` to access the app.

## Using the Application

1. **Home Page:**
   - Click on **Start** to begin configuring your session.

2. **Session Configuration:**
   - **Select Topics:** Choose the topics you want to study or be tested on.
   - **Select Mode:**
     - **Study Mode:** Immediate feedback after each question.
     - **Exam Mode:** Feedback provided after completing all questions.
   - **Set Time Limits:** Adjust the time per card or total exam time as needed.
   - **Set Exam Questions (Exam Mode):** Specify the minimum and maximum number of questions per topic.

3. **Flashcard Session:**
   - Read the question and provide your answer in the input field.
   - A timer displays the remaining time for the current card.
   - Click **Submit Answer** to proceed to the next card.

4. **Results Page:**
   - View your total score, the number of correct answers, and your percentage score.
   - Option to return to the home page or start a new session.

## Persisting Scores

- **All-Time Scores:**
  - Currently, the application tracks scores during the session.
  - To persist all-time scores, implement a database or file system storage to save and load scores across sessions.

## Customization

- **Graphical Interface:**
  - Customize the HTML templates in the `templates/` folder to change the look and feel.
- **Additional Features:**
  - Implement features like user authentication, progress tracking, or advanced analytics as needed.

## Error Handling

- Ensure all dependencies are installed, and the OpenAI API key is correctly set.
- Check console logs for error messages during transcript loading or API calls.

## Security Considerations

- Replace `app.secret_key` with a secure, random value in production.
- Protect your OpenAI API key and do not expose it in client-side code or public repositories.


