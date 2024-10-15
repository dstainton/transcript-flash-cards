# app.py

import os
import json
import random
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key in production

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurable parameters
CARDS_PER_TRANSCRIPT = 10  # Default number of cards per transcript
TIME_PER_CARD = 10  # Default time per card in seconds
TOTAL_EXAM_TIME = 600  # Default total exam time in seconds (10 minutes)

# Load transcripts and generate flashcards
def load_transcripts(folder_path):
    flashcards = []
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    transcript = f.read()
                cards = generate_flashcards(transcript, filename)
                flashcards.extend(cards)
    except Exception as e:
        print(f"Error loading transcripts: {e}")
    return flashcards

def generate_flashcards(transcript, filename):
    prompt = f"""
    Generate {CARDS_PER_TRANSCRIPT} flashcards from the following transcript:
    {transcript}

    Each flashcard should be a JSON object with the following keys:
    - 'topic': The main topic of the question.
    - 'question': The question text (can be yes/no or require a written sentence).
    - 'answer': The correct answer to the question.

    Return a JSON array of flashcards.
    """
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.5,
        )
        flashcards_json = response.choices[0].text.strip()
        flashcards = json.loads(flashcards_json)
        for card in flashcards:
            card['filename'] = filename
            card['correct_count'] = 0  # Initialize correct answer count
            card['attempts'] = 0  # Initialize attempts
        return flashcards
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []

# Load flashcards at startup
flashcards = load_transcripts('transcripts')  # Ensure transcripts are in 'transcripts' folder

# Shuffle flashcards
random.shuffle(flashcards)

# Initialize scores
all_time_scores = {}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        session['topics'] = request.form.getlist('topics')
        session['mode'] = request.form.get('mode')
        session['time_per_card'] = int(request.form.get('time_per_card', TIME_PER_CARD))
        session['total_exam_time'] = int(request.form.get('total_exam_time', TOTAL_EXAM_TIME))
        session['current_card_index'] = 0
        session['score'] = 0
        session['start_time'] = datetime.now().isoformat()
        session['exam_questions'] = []
        # Filter flashcards by selected topics
        session['flashcards'] = [card for card in flashcards if card['topic'] in session['topics']]
        random.shuffle(session['flashcards'])
        if session['mode'] == 'exam':
            # Select a subset for the exam
            min_questions = int(request.form.get('min_questions', 5))
            max_questions = int(request.form.get('max_questions', 10))
            num_questions = random.randint(min_questions, max_questions)
            session['exam_questions'] = session['flashcards'][:num_questions]
        return redirect(url_for('flashcard'))
    else:
        topics = set(card['topic'] for card in flashcards)
        return render_template('start.html', topics=topics)

@app.route('/flashcard', methods=['GET', 'POST'])
def flashcard():
    mode = session.get('mode', 'study')
    current_card_index = session.get('current_card_index', 0)
    start_time = datetime.fromisoformat(session.get('start_time', datetime.now().isoformat()))
    time_per_card = session.get('time_per_card', TIME_PER_CARD)
    total_exam_time = session.get('total_exam_time', TOTAL_EXAM_TIME)

    # Check for time expiration
    if mode == 'exam':
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if elapsed_time > total_exam_time:
            return redirect(url_for('results'))
    else:
        if 'card_start_time' in session:
            card_start_time = datetime.fromisoformat(session['card_start_time'])
            elapsed_time = (datetime.now() - card_start_time).total_seconds()
            if elapsed_time > time_per_card:
                session['current_card_index'] += 1
                return redirect(url_for('flashcard'))
        else:
            session['card_start_time'] = datetime.now().isoformat()

    # Get the current card
    if mode == 'exam':
        if current_card_index >= len(session['exam_questions']):
            return redirect(url_for('results'))
        card = session['exam_questions'][current_card_index]
    else:
        if current_card_index >= len(session['flashcards']):
            return redirect(url_for('results'))
        card = session['flashcards'][current_card_index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        card['attempts'] += 1
        # In exam mode, do not assess immediately
        if mode == 'exam':
            session.setdefault('user_answers', []).append({
                'question': card['question'],
                'user_answer': user_answer,
                'correct_answer': card['answer']
            })
        else:
            correct = check_answer(card['question'], user_answer, card['answer'])
            if correct:
                session['score'] += 1
                card['correct_count'] += 1
            else:
                card['correct_count'] = 0  # Reset if incorrect
            # Retire card if answered correctly three times in a row
            if card['correct_count'] >= 3:
                session['flashcards'].pop(current_card_index)
            else:
                session['current_card_index'] += 1
            session.pop('card_start_time', None)
        return redirect(url_for('flashcard'))

    return render_template('flashcard.html', card=card, mode=mode, time_limit=time_per_card)

@app.route('/results')
def results():
    mode = session.get('mode', 'study')
    if mode == 'exam':
        # Assess all answers at the end
        user_answers = session.get('user_answers', [])
        score = 0
        for answer in user_answers:
            correct = check_answer(answer['question'], answer['user_answer'], answer['correct_answer'])
            if correct:
                score += 1
        total_questions = len(user_answers)
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        return render_template('results.html', total_questions=total_questions, score=score, percentage=percentage)
    else:
        total_questions = session.get('current_card_index', 0)
        score = session.get('score', 0)
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        return render_template('results.html', total_questions=total_questions, score=score, percentage=percentage)

def check_answer(question, user_answer, correct_answer):
    prompt = f"""
    Question: {question}
    User Answer: {user_answer}
    Correct Answer: {correct_answer}
    Is the user's answer correct? Respond with "Yes" or "No".
    """
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0,
        )
        evaluation = response.choices[0].text.strip().lower()
        return evaluation == 'yes'
    except Exception as e:
        print(f"Error checking answer: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)