# app.py

import os
import json
import random
import time
from datetime import datetime, timedelta
import subprocess
import sys
import secrets
from collections import defaultdict

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

# List of required packages
required_packages = ['flask', 'openai']

# Check and install required packages
for package in required_packages:
    install_and_import(package)

from flask import Flask, render_template, request, redirect, url_for, session, flash
import openai

# Create Flask app and set secret key
app = Flask(__name__)

# Add to app configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# Generate a persistent secret key if it doesn't exist
SECRET_KEY_FILE = 'secret_key.txt'

def get_or_create_secret_key():
    try:
        if os.path.exists(SECRET_KEY_FILE):
            with open(SECRET_KEY_FILE, 'r') as f:
                return f.read().strip()
        else:
            # Generate a new secret key
            secret_key = secrets.token_hex(32)
            with open(SECRET_KEY_FILE, 'w') as f:
                f.write(secret_key)
            return secret_key
    except Exception as e:
        print(f"Error handling secret key: {e}")
        # Fallback to a new random key (will change on restart)
        return secrets.token_hex(32)

app.secret_key = get_or_create_secret_key()

# Set up OpenAI API key
with open('openaikey.txt', 'r') as file:
    api_key = file.read().strip()

# Create OpenAI client
client = openai.OpenAI(api_key=api_key)

# Configurable parameters
CARDS_PER_TRANSCRIPT = 15  # Default number of cards per transcript
TIME_PER_CARD = 10  # Default time per card in seconds
TOTAL_EXAM_TIME = 3600  # Default total exam time in seconds (10 minutes)

def save_flashcards(flashcards, filepath='flashcards.json'):
    """Save flashcards to a JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(flashcards, f, indent=2)
    except Exception as e:
        print(f"Error saving flashcards: {e}")

def load_saved_flashcards(filepath='flashcards.json'):
    """Load flashcards from a JSON file if it exists"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading saved flashcards: {e}")
    return None

def validate_flashcard(card):
    required_keys = ['question', 'answer', 'topic', 'filename']
    return all(key in card for key in required_keys)

# Load transcripts and generate flashcards
def load_transcripts(folder_path):
    """Load flashcards from saved file or generate new ones from transcripts"""
    # Try to load saved flashcards first
    saved_flashcards = load_saved_flashcards()
    if saved_flashcards:
        print("Loaded flashcards from saved file")
        return saved_flashcards

    # If no saved flashcards, generate new ones
    print("\nGenerating new flashcards from transcripts...")
    flashcards = []
    try:
        # First, try to read the Topic.txt file
        topic_file = os.path.join(folder_path, 'Topic.txt')
        if os.path.exists(topic_file):
            with open(topic_file, 'r', encoding='utf-8') as f:
                main_topic = f.read().strip()
            print(f"Found main topic: {main_topic}\n")
        else:
            main_topic = None
            print("Warning: Topic.txt not found in transcripts folder\n")

        transcript_files = [f for f in os.listdir(folder_path) 
                          if f.endswith('.txt') and f != 'Topic.txt']
        total_files = len(transcript_files)
        print(f"Found {total_files} transcript files to process\n")
        
        for index, filename in enumerate(transcript_files, 1):
            print(f"Processing transcript {index}/{total_files}: {filename}")
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                transcript = f.read()
            cards = generate_flashcards(transcript, filename, main_topic)
            flashcards.extend(cards)
            print(f"Generated {len(cards)} flashcards from {filename}\n")
        
        # Save the generated flashcards
        if flashcards:
            print(f"Saving {len(flashcards)} total flashcards to file...")
            save_flashcards(flashcards)
            print("Flashcards saved successfully!")
        else:
            print("No flashcards were generated!")
            
    except Exception as e:
        print(f"Error loading transcripts: {e}")
    return flashcards

def generate_flashcards(transcript, filename, main_topic=None):
    print(f"  Generating flashcards for {filename}...")
    
    # Get topic from filename (everything before the first dot)
    topic = filename.split('.')[0]
    
    # Include main topic in the prompt if available
    topic_context = f"Main topic: {main_topic}\n" if main_topic else ""
    
    prompt = f"""
    {topic_context}Generate exactly {CARDS_PER_TRANSCRIPT} flashcards from the following transcript.
    The response must be a valid JSON array containing flashcard objects.
    Each flashcard object must have these exact keys: 'question' and 'answer'.
    Format the response as a JSON array without any additional text or explanation.

    IMPORTANT: Answers must be one of:
    - "True" or "False"
    - "Yes" or "No"
    - A phrase of 5 words or less

    Example format:
    [
        {{
            "question": "Is this a true/false question?",
            "answer": "True"
        }},
        {{
            "question": "Should this answer be yes/no?",
            "answer": "Yes"
        }},
        {{
            "question": "What is a short answer?",
            "answer": "Five words or less only"
        }}
    ]

    Transcript:
    {transcript}
    """
    try:
        print("  Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that generates flashcards with very concise answers. "
                              "Answers must be True/False, Yes/No, or a phrase of 5 words or less."
                              "Each type of answer must be represented in the set of flashcards."
                              "Ignore anecdotes, jokes, stories, and other irrelevent information."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            temperature=0.5,
        )
        print("  Received response from OpenAI API")
        
        flashcards_json = response.choices[0].message.content.strip()
        print("  Raw response:")
        print(flashcards_json)
        
        try:
            flashcards = json.loads(flashcards_json)
            print(f"  Successfully parsed {len(flashcards)} flashcards")
            
            for card in flashcards:
                card['topic'] = topic  # Set topic from filename
                card['filename'] = filename
                card['correct_count'] = 0
                card['attempts'] = 0
            return flashcards
            
        except json.JSONDecodeError as e:
            print(f"  JSON parsing error: {e}")
            print("  Response was not valid JSON")
            return []
            
    except Exception as e:
        print(f"  Error generating flashcards: {e}")
        return []

# Load flashcards at startup
flashcards = load_transcripts('transcripts')  # Ensure transcripts are in 'transcripts' folder

# Shuffle flashcards
random.shuffle(flashcards)

# Initialize scores
all_time_scores = {}
exam_history = defaultdict(list)
study_history = defaultdict(list)

# Add persistent storage for history
def save_history():
    """Save history to JSON file with datetime objects converted to ISO format strings"""
    history = {
        'exam_history': {
            k.isoformat(): v for k, v in exam_history.items()
        },
        'study_history': {
            k.isoformat(): v for k, v in study_history.items()
        },
        'all_time_scores': all_time_scores
    }
    with open('history.json', 'w') as f:
        json.dump(history, f)

def load_history():
    """Load history from JSON file and convert ISO format strings back to datetime objects"""
    global exam_history, study_history, all_time_scores
    try:
        if os.path.exists('history.json'):
            with open('history.json', 'r') as f:
                history = json.load(f)
                # Convert string dates back to datetime objects
                exam_history = defaultdict(list, {
                    datetime.fromisoformat(k): v 
                    for k, v in history['exam_history'].items()
                })
                study_history = defaultdict(list, {
                    datetime.fromisoformat(k): v 
                    for k, v in history['study_history'].items()
                })
                all_time_scores = history['all_time_scores']
    except Exception as e:
        print(f"Error loading history: {e}")

# Add cleanup of old history entries
def cleanup_old_history(days=30):
    cutoff = datetime.now() - timedelta(days=days)
    exam_history = {k: v for k, v in exam_history.items() 
                   if isinstance(k, datetime) and k > cutoff}
    study_history = {k: v for k, v in study_history.items() 
                   if isinstance(k, datetime) and k > cutoff}

# Load history at startup
load_history()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        if not request.form.getlist('topics'):
            flash('Please select at least one topic', 'error')
            return redirect(url_for('start'))
        selected_topics = request.form.getlist('topics')  # Get list of selected topics
        
        # Initialize session
        session.clear()  # Clear any existing session data
        session['mode'] = request.form.get('mode', 'study')
        
        # Get time values with proper error handling and defaults
        try:
            session['time_per_card'] = int(request.form.get('time_per_card') or TIME_PER_CARD)
            session['total_exam_time'] = int(request.form.get('total_exam_time') or TOTAL_EXAM_TIME)
        except ValueError:
            session['time_per_card'] = TIME_PER_CARD
            session['total_exam_time'] = TOTAL_EXAM_TIME
            
        session['current_card_index'] = 0
        session['score'] = 0
        session['start_time'] = datetime.now().isoformat()
        session['topics'] = selected_topics  # Missing topics in session
        
        # Filter flashcards by selected topics if any are selected
        if selected_topics and 'all' not in selected_topics:
            session['flashcards'] = [card for card in flashcards if card['topic'] in selected_topics]
        else:
            session['flashcards'] = flashcards.copy()  # Use all flashcards
            
        if not session['flashcards']:  # If no flashcards match the selected topics
            return render_template('start.html', 
                                topics=sorted(set(card['topic'] for card in flashcards)),
                                error="No flashcards found for selected topics")
            
        random.shuffle(session['flashcards'])
        
        if session['mode'] == 'exam':
            try:
                min_questions = int(request.form.get('min_questions') or 5)
                max_questions = int(request.form.get('max_questions') or 10)
            except ValueError:
                min_questions = 5
                max_questions = 10
                
            num_questions = random.randint(min_questions, max_questions)
            session['exam_questions'] = session['flashcards'][:num_questions]
        
        return redirect(url_for('flashcard'))
    else:
        # Get unique topics from flashcards
        topics = sorted(set(card['topic'] for card in flashcards))
        return render_template('start.html', 
                             topics=topics,
                             time_per_card=TIME_PER_CARD,
                             total_exam_time=TOTAL_EXAM_TIME)

@app.route('/flashcard', methods=['GET', 'POST'])
def flashcard():
    # Check if session is properly initialized
    if 'flashcards' not in session or not session['flashcards']:
        return redirect(url_for('start'))

    mode = session['mode']
    current_card_index = session['current_card_index']
    
    # Get the current card
    if mode == 'exam':
        if current_card_index >= len(session.get('exam_questions', [])):
            return redirect(url_for('results'))
        card = session['exam_questions'][current_card_index]
    else:
        if current_card_index >= len(session['flashcards']): 
            return redirect(url_for('results'))
        card = session['flashcards'][current_card_index]

    # Handle POST request (answer submission)
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if not user_answer:
            return render_template('flashcard.html', 
                                card=card, 
                                mode=mode, 
                                error="Please provide an answer")
        
        if mode == 'exam':
            session.setdefault('user_answers', []).append({
                'question': card['question'],
                'user_answer': user_answer,
                'correct_answer': card['answer']
            })
            session['current_card_index'] += 1
        else:
            correct = check_answer(card['question'], user_answer, card['answer'])
            if correct:
                session['score'] += 1
                card['correct_count'] = session.get(f'correct_count_{current_card_index}', 0) + 1
                session[f'correct_count_{current_card_index}'] = card['correct_count']
            else:
                session[f'correct_count_{current_card_index}'] = 0
            
            if card['correct_count'] >= 3:
                session['flashcards'].pop(current_card_index)
            else:
                session['current_card_index'] += 1

            # Track attempts for each card
            card['attempts'] = card.get('attempts', 0) + 1
            session['total_attempts'] = session.get('total_attempts', 0) + 1
                
        return redirect(url_for('flashcard'))

    return render_template('flashcard.html', 
                         card=card, 
                         mode=mode, 
                         time_limit=session.get('time_per_card'))

# Modify the results route
@app.route('/results')
def results():
    if 'mode' not in session:
        return redirect(url_for('index'))
    
    mode = session.get('mode', 'study')
    timestamp = datetime.now()
    
    if mode == 'exam':
        user_answers = session.get('user_answers', [])
        score = 0
        results = []
        
        for answer in user_answers:
            correct = check_answer(answer['question'], answer['user_answer'], answer['correct_answer'])
            results.append({
                'question': answer['question'],
                'user_answer': answer['user_answer'],
                'correct_answer': answer['correct_answer'],
                'is_correct': correct
            })
            if correct:
                score += 1
                
        total_questions = len(user_answers)
        percentage = calculate_percentage(score, total_questions)
        
        exam_history[timestamp] = {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'topics': session.get('topics', [])
        }
        
        save_history()  # Save history after exam
        
        return render_template('results.html',
                             mode=mode,
                             total_questions=total_questions,
                             score=score,
                             percentage=percentage,
                             results=results)
    else:
        total_questions = session.get('current_card_index', 0)
        score = session.get('score', 0)
        percentage = calculate_percentage(score, total_questions)
        
        study_history[timestamp] = {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'topics': session.get('topics', [])
        }
        
        save_history()  # Save history after study session
        
        return render_template('results.html',
                             mode=mode,
                             total_questions=total_questions,
                             score=score,
                             percentage=percentage)

@app.route('/stats')
def stats():
    return render_template('stats.html', 
                         exam_history=exam_history,
                         study_history=study_history,
                         all_time_scores=all_time_scores)

# Update the route decorator to match the name used in templates
@app.route('/exit', methods=['POST'])
def exit():  # Changed from exit_session to exit
    if 'mode' in session:
        mode = session['mode']
        score = session.get('score', 0)
        total = session.get('current_card_index', 0)
        timestamp = datetime.now()
        
        if mode == 'exam':
            exam_history[timestamp] = {
                'score': score,
                'total': total,
                'topics': session.get('topics', [])
            }
        else:
            study_history[timestamp] = {
                'score': score,
                'total': total,
                'topics': session.get('topics', [])
            }
            
        save_history()  # Save history on exit
            
    session.clear()
    return redirect(url_for('index'))

def check_answer(question, user_answer, correct_answer):
    if not all(isinstance(x, str) for x in [question, user_answer, correct_answer]):
        print("Warning: Non-string input in check_answer")
        return False
    prompt = f"""
    Question: {question}
    User Answer: {user_answer}
    Correct Answer: {correct_answer}
    Is the user's answer correct? Respond with "Yes" or "No".
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            n=1,
            temperature=0,
        )
        evaluation = response.choices[0].message.content.strip().lower()
        return evaluation == 'yes'
    except Exception as e:
        print(f"Error checking answer: {e}")
        return False

# Fix percentage calculation to handle zero division
def calculate_percentage(score, total):
    try:
        return (score / total) * 100 if total > 0 else 0
    except ZeroDivisionError:
        return 0

# Add at start of app
def init_app():
    global flashcards, exam_history, study_history, all_time_scores
    load_history()
    flashcards = load_transcripts('transcripts')
    random.shuffle(flashcards)

if __name__ == '__main__':
    init_app()
    app.run(debug=True)