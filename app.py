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
from project_manager import ProjectManager, Project
from migrate_to_projects import migrate

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

# Install flask-session separately (package name differs from import name)
try:
    import flask_session
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-session"])

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import openai
from document_processor import DocumentProcessor

# Create Flask app and set secret key
app = Flask(__name__)

# Configure server-side session to avoid cookie size limits
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

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

# Initialize server-side session
Session(app)

# Set up OpenAI API key
with open('openaikey.txt', 'r') as file:
    api_key = file.read().strip()

# Create OpenAI client
client = openai.OpenAI(api_key=api_key)

# Run migration if needed (converts old single-project structure to multi-project)
print("\nChecking if migration is needed...")
migrate()

# Initialize Project Manager
print("Initializing Project Manager...")
project_manager = ProjectManager()
print(f"[OK] Found {len(project_manager.projects)} project(s)\n")

# Configurable parameters
CARDS_PER_TRANSCRIPT = 25  # Default number of cards per transcript
TIME_PER_CARD = 10  # Default time per card in seconds
TOTAL_EXAM_TIME = 60  # Default total exam time in minutes

# Helper functions for project management
def get_current_project() -> Project:
    """Get the current project from session, or return default project"""
    project_id = session.get('current_project_id')
    
    if project_id and project_id in project_manager.projects:
        return project_manager.projects[project_id]
    
    # No project in session or project not found - use first available or create default
    if project_manager.projects:
        # Use first available project
        first_project_id = list(project_manager.projects.keys())[0]
        session['current_project_id'] = first_project_id
        return project_manager.projects[first_project_id]
    else:
        # No projects exist - create a default one
        default_project = project_manager.create_project("My Flash Cards")
        session['current_project_id'] = default_project.id
        return default_project

def set_current_project(project_id: str):
    """Set the current project in session"""
    if project_id in project_manager.projects:
        session['current_project_id'] = project_id
        return True
    return False

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
                flashcards = json.load(f)
                # Add answer_type to existing flashcards if missing
                for card in flashcards:
                    if 'answer_type' not in card:
                        card['answer_type'] = get_answer_type(card['answer'])
                return flashcards
    except Exception as e:
        print(f"Error loading saved flashcards: {e}")
    return None

def get_answer_type(correct_answer):
    """Determine the type of answer expected"""
    answer_lower = correct_answer.strip().lower()
    if answer_lower in ['true', 'false']:
        return 'true_false'
    elif answer_lower in ['yes', 'no']:
        return 'yes_no'
    elif len(correct_answer.split()) == 1 and correct_answer.isalpha() and len(correct_answer) == 1:
        return 'multiple_choice'
    elif ',' in correct_answer and all(len(part.strip()) == 1 and part.strip().isalpha() for part in correct_answer.split(',')):
        return 'multiple_answer'
    else:
        # Default to multiple_choice for any other single word answers
        return 'multiple_choice'

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
    Each flashcard object must have these exact keys: 'question', 'answer', 'explanation', and optionally 'options'.
    Format the response as a JSON array without any additional text or explanation.

    CRITICAL RULES FOR QUESTION TYPES:
    
    1. TRUE/FALSE questions: Use ONLY for statements that can be evaluated as factually true or false.
       - Answer MUST be exactly "True" or "False" (capitalized)
       - Question should be a statement, not a question
       - MUST include "explanation" field with 1-2 sentences explaining WHY the answer is True or False
       - Example: {{"question": "The Product Owner is responsible for maximizing product value.", "answer": "True", "explanation": "The Product Owner is accountable for maximizing the value of the product resulting from the work of the Scrum Team."}}
       
    2. YES/NO questions: Use ONLY for questions asking about permissions, recommendations, or subjective matters.
       - Answer MUST be exactly "Yes" or "No" (capitalized)
       - Question should end with a question mark
       - MUST include "explanation" field with 1-2 sentences explaining WHY
       - Example: {{"question": "Should the team estimate in story points?", "answer": "Yes", "explanation": "Story points allow teams to estimate relative complexity without committing to specific time estimates, which is more accurate for complex work."}}
       
    3. MULTIPLE CHOICE: Use for questions with one correct answer from several options.
       - Answer MUST be a single letter: "A", "B", "C", or "D"
       - MUST include "options" array with 4 choices formatted as "A) text", "B) text", etc.
       - MUST include "explanation" field with 1-2 sentences explaining WHY the correct answer is right
       - Example: {{"question": "What is the primary role of a Product Owner?", "answer": "A", "options": ["A) Maximize product value", "B) Write code", "C) Manage the team", "D) Create documentation"], "explanation": "The Product Owner's primary responsibility is to maximize the value of the product by managing the Product Backlog and ensuring the team works on the most valuable items."}}
       
    4. MULTIPLE ANSWER: Use for questions where multiple options can be correct.
       - Answer MUST be comma-separated letters like "A,C" or "B,C,D" (no spaces)
       - MUST include "options" array with choices formatted as "A) text", "B) text", etc.
       - MUST include "explanation" field explaining WHY these specific answers are correct
       - Question should indicate multiple answers needed: "(Select all that apply)" or "Which of the following..."
       - Example: {{"question": "Which of the following are Scrum values? (Select all that apply)", "answer": "A,C,D", "options": ["A) Courage", "B) Speed", "C) Focus", "D) Respect"], "explanation": "The five Scrum values are Commitment, Focus, Openness, Respect, and Courage. Speed is not a Scrum value."}}

    DO NOT mix question types! If the question asks "Is...", use True/False. If it asks "Should..." or "Can...", use Yes/No.
    Ensure answers match the question type exactly.
    ALWAYS include an "explanation" field that helps learners understand the concept, not just the answer.

    Transcript:
    {transcript}
    """
    try:
        print("  Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that generates exam-style flashcards. "
                              "STRICT RULES: "
                              "1) True/False questions MUST have answers of exactly 'True' or 'False' (capitalized) and be statements. "
                              "2) Yes/No questions MUST have answers of exactly 'Yes' or 'No' (capitalized) and be questions about permissions or recommendations. "
                              "3) Multiple Choice MUST have single letter answers (A, B, C, or D) with an options array. "
                              "4) Multiple Answer MUST have comma-separated letters (e.g., 'A,C') with an options array. "
                              "NEVER mix up question types with answer types. "
                              "Focus on key concepts and ignore anecdotes, jokes, or stories."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            n=1,
            temperature=0.4,
        )
        print("  Received response from OpenAI API")
        
        flashcards_json = response.choices[0].message.content.strip()
        print("  Raw response:")
        print(flashcards_json)
        
        # Remove markdown code blocks if present
        if flashcards_json.startswith('```'):
            # Find the first newline after ```json or ```
            first_newline = flashcards_json.find('\n')
            # Find the last ``` marker
            last_marker = flashcards_json.rfind('```')
            if first_newline != -1 and last_marker != -1:
                flashcards_json = flashcards_json[first_newline+1:last_marker].strip()
                print("  Removed markdown code blocks from response")
        
        try:
            flashcards = json.loads(flashcards_json)
            print(f"  Successfully parsed {len(flashcards)} flashcards")
            
            for card in flashcards:
                card['topic'] = topic  # Set topic from filename
                card['filename'] = filename
                card['correct_count'] = 0
                card['attempts'] = 0
                card['answer_type'] = get_answer_type(card['answer'])  # Add answer type
            return flashcards
            
        except json.JSONDecodeError as e:
            print(f"  JSON parsing error: {e}")
            print("  Response was not valid JSON")
            return []
            
    except Exception as e:
        print(f"  Error generating flashcards: {e}")
        return []

def generate_project_name_from_text(text):
    """Use AI to generate a concise project name from document text"""
    # Truncate text to avoid token limits (first 3000 characters)
    sample_text = text[:3000]
    
    prompt = f"""
    Based on the following document content, generate a short, concise project name (3-6 words max).
    The name should capture the main topic or subject matter.
    Respond with ONLY the project name, nothing else.
    
    Document content:
    {sample_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use mini for simple tasks
            messages=[
                {"role": "system", "content": "You generate concise, descriptive project names."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.5,
        )
        
        project_name = response.choices[0].message.content.strip()
        # Remove quotes if present
        project_name = project_name.strip('"\'')
        print(f"Generated project name: {project_name}")
        return project_name
    
    except Exception as e:
        print(f"Error generating project name: {e}")
        return "New Project"

def extract_topics_from_text(text):
    """Use AI to extract topics and determine flashcard count per topic"""
    # Truncate text to avoid token limits (first 5000 characters)
    sample_text = text[:5000]
    
    prompt = f"""
    Analyze the following document content and extract 3-8 main topics/sections.
    For each topic, suggest an appropriate number of flashcards (5-25 per topic).
    
    Return your response as a JSON array of objects with this exact structure:
    [{{"name": "Topic Name", "flashcard_count": 10}}]
    
    Consider the complexity and importance of each topic when determining flashcard counts.
    Respond with ONLY the JSON array, no additional text.
    
    Document content:
    {sample_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing educational content and extracting key topics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3,
        )
        
        topics_json = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if topics_json.startswith('```'):
            first_newline = topics_json.find('\n')
            last_marker = topics_json.rfind('```')
            if first_newline != -1 and last_marker != -1:
                topics_json = topics_json[first_newline+1:last_marker].strip()
        
        topics = json.loads(topics_json)
        print(f"Extracted {len(topics)} topics")
        return topics
    
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return []

def generate_flashcards_from_text(text, topic_name, num_cards):
    """Generate flashcards for a specific topic from document text"""
    prompt = f"""
    Generate EXACTLY {num_cards} flashcards (no more, no less) about "{topic_name}" from the following content.
    
    IMPORTANT: The JSON array MUST contain precisely {num_cards} flashcard objects.
    
    The response must be a valid JSON array containing flashcard objects.
    Each flashcard object must have these exact keys: 'question', 'answer', 'explanation', and optionally 'options'.
    Format the response as a JSON array without any additional text or explanation.

    CRITICAL RULES FOR QUESTION TYPES:
    
    1. TRUE/FALSE questions: Use ONLY for statements that can be evaluated as factually true or false.
       - Answer MUST be exactly "True" or "False" (capitalized)
       - Question should be a statement, not a question
       - MUST include "explanation" field with 1-2 sentences explaining WHY
       
    2. YES/NO questions: Use ONLY for questions asking about permissions, recommendations, or subjective matters.
       - Answer MUST be exactly "Yes" or "No" (capitalized)
       - Question should end with a question mark
       - MUST include "explanation" field with 1-2 sentences explaining WHY
       
    3. MULTIPLE CHOICE: Use for questions with one correct answer from several options.
       - Answer MUST be a single letter: "A", "B", "C", or "D"
       - MUST include "options" array with 4 choices formatted as "A) text", "B) text", etc.
       - MUST include "explanation" field with 1-2 sentences explaining WHY the correct answer is right
       
    4. MULTIPLE ANSWER: Use for questions where multiple options can be correct.
       - Answer MUST be comma-separated letters like "A,C" or "B,C,D" (no spaces)
       - MUST include "options" array with choices formatted as "A) text", "B) text", etc.
       - MUST include "explanation" field explaining WHY these specific answers are correct
       - Question should indicate multiple answers needed

    ALWAYS include an "explanation" field that helps learners understand the concept, not just the answer.

    Document content:
    {text[:4000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You generate high-quality flashcards from educational content. "
                              "Follow the question type rules strictly. "
                              "Always include clear explanations to help learners understand the concepts."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.4,
        )
        
        flashcards_json = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if flashcards_json.startswith('```'):
            first_newline = flashcards_json.find('\n')
            last_marker = flashcards_json.rfind('```')
            if first_newline != -1 and last_marker != -1:
                flashcards_json = flashcards_json[first_newline+1:last_marker].strip()
        
        flashcards = json.loads(flashcards_json)
        
        # Add metadata to each card
        for card in flashcards:
            card['topic'] = topic_name
            card['correct_count'] = 0
            card['attempts'] = 0
            card['answer_type'] = get_answer_type(card['answer'])
        
        print(f"Generated {len(flashcards)} flashcards for topic '{topic_name}'")
        return flashcards
    
    except Exception as e:
        print(f"Error generating flashcards for topic '{topic_name}': {e}")
        return []

# Project-aware helper functions for mastery
def get_card_hash(question):
    """Generate a unique hash for a flashcard question"""
    import hashlib
    return hashlib.md5(question.encode('utf-8')).hexdigest()

def mark_card_mastered(card):
    """Mark a card as mastered in current project"""
    project = get_current_project()
    card_hash = get_card_hash(card['question'])
    project.mastery[card_hash] = {
        'question': card['question'],
        'topic': card['topic'],
        'filename': card.get('filename', 'Unknown'),
        'mastered_date': datetime.now().isoformat()
    }
    project.save_mastery()

def is_card_mastered(card):
    """Check if a card is mastered in current project"""
    project = get_current_project()
    card_hash = get_card_hash(card['question'])
    return card_hash in project.mastery

def reset_topic_mastery(topic):
    """Reset all mastered cards for a specific topic in current project"""
    project = get_current_project()
    project.mastery = {
        k: v for k, v in project.mastery.items() 
        if v['topic'] != topic
    }
    project.save_mastery()

def get_mastery_stats():
    """Get mastery statistics by topic for current project"""
    project = get_current_project()
    stats = defaultdict(lambda: {'mastered': 0, 'total': 0})
    
    # Count total cards per topic
    for card in project.flashcards:
        topic = card['topic']
        stats[topic]['total'] += 1
        if is_card_mastered(card):
            stats[topic]['mastered'] += 1
    
    return dict(stats)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    print("TEST ROUTE CALLED")
    import sys
    sys.stdout.flush()
    # Also try logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.info("TEST ROUTE CALLED VIA LOGGING")
    # Also write to file
    with open('debug.log', 'a') as f:
        f.write("TEST ROUTE CALLED\n")
    return "Test route working!"


@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        print(f"\n===== START ROUTE POST REQUEST =====")
        
        # Handle project selection if changed
        if 'project_id' in request.form:
            new_project_id = request.form.get('project_id')
            if new_project_id != session.get('current_project_id'):
                set_current_project(new_project_id)
                print(f"Switched to project: {new_project_id}")
        
        if not request.form.getlist('topics'):
            flash('Please select at least one topic', 'error')
            return redirect(url_for('start'))
        selected_topics = request.form.getlist('topics')
        
        print(f"Form data: {dict(request.form)}")
        print(f"Topics selected: {selected_topics}")
        print(f"Raw topics list: {list(selected_topics)}")
        
        # Reset specific session keys to ensure clean start
        keys_to_reset = ['mode', 'user_answers', 'exam_questions', 'completed_cards', 'current_card_index', 'score', 'start_time', 'topics', 'total_attempts', 'exam_start_time', 'exam_duration_seconds', 'question_start_time', 'question_duration_seconds', 'flashcards', 'total_cards', 'time_per_card', 'total_exam_time', 'results_saved']
        for key in keys_to_reset:
            if key in session:
                del session[key]
        
        # Initialize session
        session['mode'] = request.form.get('mode', 'study')
        
        # Initialize all session variables
        session['user_answers'] = []
        session['exam_questions'] = []
        session['completed_cards'] = []
        
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
        session['topics'] = selected_topics
        session['completed_cards'] = []
        session['total_attempts'] = 0
        
        # Debug: Print session state
        print(f"New flashcard session started - mode: {session['mode']}, current_card_index: {session['current_card_index']}")
        print(f"Session keys after setup: {list(session.keys())}")
        
        # Test session persistence by setting a test value
        session['test_value'] = 'test_persistence'
        print(f"Test value set: {session.get('test_value')}")
        
        # Initialize exam timer
        if session['mode'] == 'exam':
            session['exam_start_time'] = datetime.now().isoformat()
            session['exam_duration_seconds'] = session['total_exam_time'] * 60  # Convert minutes to seconds
            session['question_start_time'] = datetime.now().isoformat()
            session['question_duration_seconds'] = session['time_per_card']  # Time per question in seconds
        
        # Get current project and load its flashcards
        project = get_current_project()
        project.load_flashcards()
        project.load_mastery()
        
        # Filter flashcards by selected topics if any are selected
        print(f"Selected topics: {selected_topics}")
        print(f"Total flashcards available: {len(project.flashcards)}")
        
        if 'all' in selected_topics:
            session['flashcards'] = project.flashcards.copy()  # Use all flashcards
            print(f"Using all flashcards: {len(session['flashcards'])}")
        else:
            session['flashcards'] = [card for card in project.flashcards if card['topic'] in selected_topics]
            print(f"Filtered flashcards: {len(session['flashcards'])}")
        
        # In study mode, filter out already mastered cards
        if session['mode'] == 'study':
            original_count = len(session['flashcards'])
            session['flashcards'] = [card for card in session['flashcards'] if not is_card_mastered(card)]
            mastered_count = original_count - len(session['flashcards'])
            if mastered_count > 0:
                print(f"Filtered out {mastered_count} already mastered cards")
                flash(f"{mastered_count} card(s) already mastered in selected topics", 'info')
            
        session['total_cards'] = len(session['flashcards'])
        print(f"Total cards set to: {session['total_cards']}")
        
        # Debug: Show first few topics from flashcards
        if project.flashcards:
            sample_topics = list(set(card['topic'] for card in project.flashcards[:10]))
            print(f"Sample topics from flashcards: {sample_topics}")
            
        if not session['flashcards']:  # If no flashcards match the selected topics
            print("ERROR: No flashcards found - redirecting back to start")
            print(f"Selected topics were: {selected_topics}")
            print(f"Total flashcards in project: {len(project.flashcards)}")
            return render_template('start.html', 
                                topics=sorted(set(card['topic'] for card in project.flashcards)),
                                mastery_stats=get_mastery_stats(),
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
        # Get current project and load its data
        project = get_current_project()
        project.load_flashcards()
        project.load_mastery()
        
        # Get all projects with their stats for the selector
        available_projects = []
        for proj_id, proj in project_manager.projects.items():
            proj.load_flashcards()
            proj.load_mastery()
            available_projects.append({
                'id': proj.id,
                'name': proj.name,
                'stats': proj.get_stats()
            })
        available_projects = sorted(available_projects, key=lambda x: x['name'])
        
        # Get unique topics from current project flashcards with mastery stats
        topics = sorted(set(card['topic'] for card in project.flashcards)) if project.flashcards else []
        mastery_stats = get_mastery_stats()
        
        return render_template('start.html', 
                             topics=topics,
                             mastery_stats=mastery_stats,
                             current_project=project,
                             available_projects=available_projects,
                             time_per_card=TIME_PER_CARD,
                             total_exam_time=TOTAL_EXAM_TIME)

@app.route('/flashcard', methods=['GET', 'POST'])
def flashcard():
    # Check if session is properly initialized
    mode = session.get('mode', 'study')
    current_card_index = session.get('current_card_index', 0)
    
    print(f"Flashcard route - mode: {mode}, current_card_index: {current_card_index}")
    print(f"Session keys in flashcard route: {list(session.keys())}")
    print(f"Test value in flashcard route: {session.get('test_value', 'NOT_FOUND')}")
    
    if mode == 'exam':
        exam_questions = session.get('exam_questions', [])
        print(f"Exam questions: {len(exam_questions)}")
        if 'exam_questions' not in session or not exam_questions:
            print("No exam questions - redirecting to start")
            return redirect(url_for('start'))
    else:
        flashcards = session.get('flashcards', [])
        print(f"Study flashcards: {len(flashcards)}")
        if 'flashcards' not in session or not flashcards:
            print("No flashcards - redirecting to start")
            return redirect(url_for('start'))

    # Get the current card first
    if mode == 'exam':
        exam_questions = session.get('exam_questions', [])
        print(f"Checking exam: current_card_index={current_card_index}, exam_questions_length={len(exam_questions)}")
        if current_card_index >= len(exam_questions):
            print(f"Redirecting to results - current_card_index ({current_card_index}) >= exam_questions length ({len(exam_questions)})")
            return redirect(url_for('results'))
        card = exam_questions[current_card_index]
    else:
        flashcards = session.get('flashcards', [])
        print(f"Checking study: current_card_index={current_card_index}, flashcards_length={len(flashcards)}")
        if current_card_index >= len(flashcards):
            print(f"Redirecting to results - current_card_index ({current_card_index}) >= flashcards length ({len(flashcards)})")
            return redirect(url_for('results'))
        card = flashcards[current_card_index]

    # Check for timer expiry in exam mode
    if mode == 'exam':
        exam_start_time = datetime.fromisoformat(session.get('exam_start_time', datetime.now().isoformat()))
        elapsed_seconds = (datetime.now() - exam_start_time).total_seconds()
        if elapsed_seconds >= session.get('exam_duration_seconds', 0):
            return redirect(url_for('results'))
        
        # Check for per-question timer expiry
        question_start_time = datetime.fromisoformat(session.get('question_start_time', datetime.now().isoformat()))
        question_elapsed = (datetime.now() - question_start_time).total_seconds()
        if question_elapsed >= session.get('question_duration_seconds', 0):
            # Check if there's a user answer from the form (timeout but answer provided)
            user_answer = ''
            if request.method == 'POST':
                if card.get('answer_type') == 'multiple_answer':
                    user_answer = ','.join(request.form.getlist('answer'))
                else:
                    user_answer = request.form.get('answer', '')
            
            if user_answer:
                # Time expired but user provided an answer - evaluate it
                is_correct = check_answer(card['question'], user_answer, card['answer'])
                completed_card = {
                    'question': card['question'],
                    'user_answer': user_answer,
                    'correct_answer': card['answer'],
                    'correct': is_correct,
                    'feedback': get_feedback(card['question'], user_answer, card['answer'], is_correct) + ' ⏰ (Time expired)',
                    'answer_type': card.get('answer_type', 'multiple_choice'),
                    'options': card.get('options', []),
                    'explanation': card.get('explanation', 'No explanation available.')
                }
                
                # Store in user_answers for results calculation
                session.setdefault('user_answers', []).append({
                    'question': card['question'],
                    'user_answer': user_answer,
                    'correct_answer': card['answer']
                })
            else:
                # Time expired with no answer
                completed_card = {
                    'question': card['question'],
                    'user_answer': '',  # Empty answer for timeout
                    'correct_answer': card['answer'],
                    'correct': False,
                    'feedback': '⏰ Time expired! No answer submitted.',
                    'answer_type': card.get('answer_type', 'multiple_choice'),
                    'options': card.get('options', []),
                    'explanation': card.get('explanation', 'No explanation available.')
                }
                
                # Store in user_answers for results calculation
                session.setdefault('user_answers', []).append({
                    'question': card['question'],
                    'user_answer': '',  # Empty answer for timeout
                    'correct_answer': card['answer']
                })
            
            # Add to completed cards for display
            session.setdefault('completed_cards', []).append(completed_card)
            session['current_card_index'] += 1
            session['question_start_time'] = datetime.now().isoformat()  # Reset question timer
            return redirect(url_for('flashcard'))

    # Handle POST request (answer submission)
    if request.method == 'POST':
        # Handle multiple answer submissions (checkboxes)
        if card.get('answer_type') == 'multiple_answer':
            user_answer = ','.join(request.form.getlist('answer'))
        else:
            user_answer = request.form.get('answer')
            
        if not user_answer:
            # Get completed cards based on mode
            if mode == 'exam':
                completed_cards = session.get('completed_cards', [])
                # Calculate remaining time for exam
                exam_start_time = datetime.fromisoformat(session.get('exam_start_time', datetime.now().isoformat()))
                elapsed_seconds = (datetime.now() - exam_start_time).total_seconds()
                exam_remaining_seconds = max(0, session.get('exam_duration_seconds', 0) - elapsed_seconds)
                
                # Calculate remaining time for current question
                question_start_time = datetime.fromisoformat(session.get('question_start_time', datetime.now().isoformat()))
                question_elapsed = (datetime.now() - question_start_time).total_seconds()
                question_remaining_seconds = max(0, session.get('question_duration_seconds', 0) - question_elapsed)
            else:
                completed_cards = session.get('completed_cards', [])
                exam_remaining_seconds = None
                question_remaining_seconds = None
                
            return render_template('flashcard_scroll.html', 
                                cards=completed_cards,
                                current_card=card, 
                                mode=mode, 
                                time_limit=session.get('time_per_card'),
                                exam_remaining_seconds=exam_remaining_seconds,
                                question_remaining_seconds=question_remaining_seconds,
                                error="Please provide an answer")
        
        if mode == 'exam':
            # Store the completed question with results for display
            completed_card = {
                'question': card['question'],
                'user_answer': user_answer,
                'correct_answer': card['answer'],
                'correct': check_answer(card['question'], user_answer, card['answer']),
                'feedback': get_feedback(card['question'], user_answer, card['answer'], check_answer(card['question'], user_answer, card['answer'])),
                'answer_type': card.get('answer_type', 'multiple_choice'),
                'options': card.get('options', []),
                'explanation': card.get('explanation', 'No explanation available.')
            }
            
            # Add to completed cards for display
            session.setdefault('completed_cards', []).append(completed_card)
            
            # Also store in user_answers for results calculation
            session.setdefault('user_answers', []).append({
                'question': card['question'],
                'user_answer': user_answer,
                'correct_answer': card['answer']
            })
            session['current_card_index'] += 1
            session['question_start_time'] = datetime.now().isoformat()  # Reset question timer for next question
        else:
            correct = check_answer(card['question'], user_answer, card['answer'])
            
            # Track streak for this specific card
            card_hash = get_card_hash(card['question'])
            current_streak = session.get(f'streak_{card_hash}', 0)

            if correct:
                session['score'] += 1
                current_streak += 1
                session[f'streak_{card_hash}'] = current_streak
            else:
                current_streak = 0
                session[f'streak_{card_hash}'] = 0
            
            # Generate feedback with streak information
            base_feedback = get_feedback(card['question'], user_answer, card['answer'], correct)
            mastered = False
            
            if correct and current_streak < 3:
                feedback = f"{base_feedback} 🔥 Streak: {current_streak}/3"
            elif correct and current_streak >= 3:
                feedback = f"{base_feedback} 🎉 CARD MASTERED! You answered correctly 3 times in a row!"
                mastered = True
                # Mark the card as permanently mastered
                mark_card_mastered(card)
            else:
                feedback = f"{base_feedback} 🔄 Streak reset to 0/3"

            # Store the completed card with results
            completed_card = {
                'question': card['question'],
                'user_answer': user_answer,
                'correct_answer': card['answer'],
                'correct': correct,
                'feedback': feedback,
                'answer_type': card.get('answer_type', 'multiple_choice'),
                'options': card.get('options', []),
                'streak': current_streak,
                'mastered': mastered,
                'explanation': card.get('explanation', 'No explanation available.')
            }
            
            # Add to completed cards list
            session.setdefault('completed_cards', []).append(completed_card)
            
            # Track how many cards have been mastered in this session
            if mastered:
                session['cards_mastered_this_session'] = session.get('cards_mastered_this_session', 0) + 1
            
            # Check if this is the last card
            is_last_card = (current_card_index + 1 >= len(session['flashcards']))
            
            if current_streak >= 3:
                # Remove card from session after mastering
                session['flashcards'].pop(current_card_index)
            else:
                session['current_card_index'] += 1

            # Track attempts for each card
            card['attempts'] = card.get('attempts', 0) + 1
            session['total_attempts'] = session.get('total_attempts', 0) + 1
            
            # If this is the last card, show results
            if is_last_card:
                return redirect(url_for('results'))
                
        return redirect(url_for('flashcard', new_card='true'))

    # Get all completed cards and current card for scrolling interface
    if mode == 'exam':
        # Exam mode now shows completed cards below current question
        completed_cards = session.get('completed_cards', [])
        # Calculate remaining time for exam
        exam_start_time = datetime.fromisoformat(session.get('exam_start_time', datetime.now().isoformat()))
        elapsed_seconds = (datetime.now() - exam_start_time).total_seconds()
        exam_remaining_seconds = max(0, session.get('exam_duration_seconds', 0) - elapsed_seconds)
        
        # Calculate remaining time for current question
        question_start_time = datetime.fromisoformat(session.get('question_start_time', datetime.now().isoformat()))
        question_elapsed = (datetime.now() - question_start_time).total_seconds()
        question_remaining_seconds = max(0, session.get('question_duration_seconds', 0) - question_elapsed)
    else:
        completed_cards = session.get('completed_cards', [])
        exam_remaining_seconds = None
        question_remaining_seconds = None
    
    # Calculate mastery progress for study mode
    cards_mastered_session = session.get('cards_mastered_this_session', 0) if mode == 'study' else 0
    cards_remaining = len(session.get('flashcards', [])) if mode == 'study' else 0
    
    return render_template('flashcard_scroll.html', 
                         cards=completed_cards,
                         current_card=card, 
                         mode=mode, 
                         time_limit=session.get('time_per_card'),
                         exam_remaining_seconds=exam_remaining_seconds,
                         question_remaining_seconds=question_remaining_seconds,
                         cards_mastered_session=cards_mastered_session,
                         cards_remaining=cards_remaining)

# Modify the results route
@app.route('/results')
def results():
    if 'mode' not in session:
        return redirect(url_for('index'))
    
    mode = session.get('mode', 'study')
    timestamp = datetime.now()
    
    # Check if results have already been saved for this session to prevent duplicates
    if session.get('results_saved', False):
        # Results already saved, just display them
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
            
            return render_template('results.html',
                                 mode=mode,
                                 total_questions=total_questions,
                                 score=score,
                                 percentage=percentage)
    
    # Save results for the first time
    session['results_saved'] = True
    
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
        
        # Save to project history
        project = get_current_project()
        project.load_history()  # Load existing history before adding new entry
        project.history['exam_history'][timestamp] = {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'topics': session.get('topics', [])
        }
        project.save_history()
        
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
        cards_mastered = session.get('cards_mastered_this_session', 0)
        
        # Save to project history
        project = get_current_project()
        project.load_history()  # Load existing history before adding new entry
        project.history['study_history'][timestamp] = {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'topics': session.get('topics', []),
            'cards_mastered': cards_mastered
        }
        project.save_history()
        
        return render_template('results.html',
                             mode=mode,
                             total_questions=total_questions,
                             score=score,
                             percentage=percentage,
                             cards_mastered=cards_mastered)

@app.route('/stats')
def stats():
    project = get_current_project()
    project.load_history()
    return render_template('stats.html', 
                         exam_history=project.history.get('exam_history', {}),
                         study_history=project.history.get('study_history', {}),
                         all_time_scores=project.history.get('all_time_scores', {}))

@app.route('/mastery')
def mastery():
    """Show mastery progress for all topics"""
    mastery_stats = get_mastery_stats()
    return render_template('mastery.html', 
                         mastery_stats=mastery_stats)

@app.route('/reset_mastery/<topic>', methods=['POST'])
def reset_mastery(topic):
    """Reset mastered cards for a specific topic"""
    reset_topic_mastery(topic)
    flash(f'Mastery progress reset for "{topic}"', 'success')
    return redirect(url_for('mastery'))

@app.route('/manage-projects')
def manage_projects():
    """Show project management page"""
    projects = []
    for proj_id, proj in project_manager.projects.items():
        proj.load_flashcards()
        proj.load_mastery()
        proj.load_history()
        projects.append({
            'id': proj.id,
            'name': proj.name,
            'stats': proj.get_stats()
        })
    projects = sorted(projects, key=lambda x: x['name'])
    
    current_project_id = session.get('current_project_id')
    
    return render_template('manage_projects.html',
                         projects=projects,
                         current_project_id=current_project_id)

@app.route('/switch-project/<project_id>', methods=['POST'])
def switch_project(project_id):
    """Switch to a different project"""
    if not set_current_project(project_id):
        flash('Project not found', 'error')
    return redirect(url_for('start'))

@app.route('/delete-project/<project_id>', methods=['POST'])
def delete_project(project_id):
    """Delete a project"""
    # Don't allow deleting the current project if it's the only one
    if len(project_manager.projects) == 1:
        flash('Cannot delete the only project', 'error')
        return redirect(url_for('manage_projects'))
    
    # If deleting current project, switch to another one first
    if project_id == session.get('current_project_id'):
        # Find another project to switch to
        for pid in project_manager.projects.keys():
            if pid != project_id:
                set_current_project(pid)
                break
    
    # Delete the project
    project_name = project_manager.projects[project_id].name if project_id in project_manager.projects else "Unknown"
    if project_manager.delete_project(project_id):
        flash(f'Project "{project_name}" deleted successfully', 'success')
    else:
        flash(f'Failed to delete project', 'error')
    
    return redirect(url_for('manage_projects'))

@app.route('/upload-documents', methods=['GET', 'POST'])
def upload_documents():
    """Handle document uploads for creating a new project"""
    if request.method == 'POST':
        # Check if files were uploaded
        if 'documents' not in request.files:
            return jsonify({'success': False, 'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('documents')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'success': False, 'error': 'No files selected'}), 400
        
        # Initialize document processor
        processor = DocumentProcessor()
        
        # Create temporary directory for uploads
        temp_dir = os.path.join(os.getcwd(), 'temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)
        
        uploaded_files = []
        errors = []
        
        try:
            # Save uploaded files temporarily
            for file in files:
                if file.filename == '':
                    continue
                
                filename = secure_filename(file.filename)
                
                # Check if file type is supported
                if not processor.is_supported_file(filename):
                    errors.append(f"{filename}: Unsupported file type")
                    continue
                
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                uploaded_files.append(filepath)
            
            if not uploaded_files:
                return jsonify({
                    'success': False, 
                    'error': 'No valid files uploaded',
                    'errors': errors
                }), 400
            
            # Extract text from documents
            results, processing_errors = processor.process_multiple_documents(uploaded_files)
            
            if processing_errors:
                errors.extend([f"{k}: {v}" for k, v in processing_errors.items()])
            
            if not results:
                return jsonify({
                    'success': False,
                    'error': 'Failed to extract text from any document',
                    'errors': errors
                }), 400
            
            # Combine all extracted text
            combined_text = '\n\n'.join([
                f"=== {filename} ===\n{text}" 
                for filename, text in results.items()
            ])
            
            # Store information in session for project creation
            session['pending_project'] = {
                'documents': uploaded_files,
                'extracted_text': combined_text,
                'document_count': len(results),
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'message': f'Successfully processed {len(results)} document(s)',
                'document_count': len(results),
                'errors': errors if errors else None
            })
        
        except Exception as e:
            # Clean up temp files on error
            for filepath in uploaded_files:
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass
            
            return jsonify({
                'success': False,
                'error': f'Upload failed: {str(e)}'
            }), 500
    
    # GET request - show upload page
    return render_template('upload_documents.html')

@app.route('/create-project-from-documents', methods=['GET', 'POST'])
def create_project_from_documents():
    """Create a new project from uploaded documents using AI"""
    # Check if there's pending project data
    if 'pending_project' not in session:
        flash('No pending project found. Please upload documents first.', 'error')
        return redirect(url_for('upload_documents'))
    
    pending = session['pending_project']
    
    if request.method == 'POST':
        try:
            # Get custom project name if provided, otherwise use AI-generated
            project_name = request.form.get('project_name', '').strip()
            
            if not project_name:
                # Use AI to generate project name
                project_name = generate_project_name_from_text(pending['extracted_text'])
            
            # Check for duplicate names and append number if needed
            original_name = project_name
            existing_names = [p.name for p in project_manager.projects.values()]
            counter = 1
            while project_name in existing_names:
                counter += 1
                project_name = f"{original_name} ({counter})"
            
            # Extract topics using AI
            topics = extract_topics_from_text(pending['extracted_text'])
            
            if not topics:
                flash('Failed to extract topics from documents', 'error')
                return redirect(url_for('create_project_from_documents'))
            
            # Create the new project
            new_project = project_manager.create_project(project_name)
            
            # Move uploaded documents to project's documents folder
            import shutil
            for temp_filepath in pending['documents']:
                if os.path.exists(temp_filepath):
                    filename = os.path.basename(temp_filepath)
                    dest_path = os.path.join(new_project.documents_folder, filename)
                    shutil.move(temp_filepath, dest_path)
            
            # Generate flashcards for each topic
            total_flashcards_generated = 0
            for topic_info in topics:
                topic_name = topic_info['name']
                num_cards = topic_info['flashcard_count']
                
                # Extract relevant text for this topic (simplified - uses all text for now)
                topic_flashcards = generate_flashcards_from_text(
                    pending['extracted_text'],
                    topic_name,
                    num_cards
                )
                
                # Add to project
                new_project.flashcards.extend(topic_flashcards)
                total_flashcards_generated += len(topic_flashcards)
            
            # Save the project
            new_project.save_flashcards()
            
            # Clean up temp directory
            temp_dir = os.path.join(os.getcwd(), 'temp_uploads')
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    os.makedirs(temp_dir, exist_ok=True)
                except:
                    pass
            
            # Clear pending project from session
            del session['pending_project']
            
            # Set as current project
            set_current_project(new_project.id)
            
            flash(f'Project "{project_name}" created with {total_flashcards_generated} flashcards across {len(topics)} topics!', 'success')
            return redirect(url_for('start'))
        
        except Exception as e:
            flash(f'Error creating project: {str(e)}', 'error')
            print(f"Error in create_project_from_documents: {e}")
            import traceback
            traceback.print_exc()
            return redirect(url_for('create_project_from_documents'))
    
    # GET request - show project setup page
    # Generate AI suggestions
    try:
        suggested_name = generate_project_name_from_text(pending['extracted_text'])
        suggested_topics = extract_topics_from_text(pending['extracted_text'])
    except Exception as e:
        print(f"Error generating AI suggestions: {e}")
        suggested_name = "New Project"
        suggested_topics = []
    
    return render_template('create_project.html',
                         suggested_name=suggested_name,
                         suggested_topics=suggested_topics,
                         document_count=pending['document_count'])

# Update the route decorator to match the name used in templates
@app.route('/exit', methods=['POST'])
def exit():  # Changed from exit_session to exit
    # Only save if we're in a session and results haven't already been saved
    if 'mode' in session and not session.get('results_saved', False):
        mode = session['mode']
        score = session.get('score', 0)
        total = session.get('current_card_index', 0)
        timestamp = datetime.now()
        
        percentage = calculate_percentage(score, total)
        
        # Save to project history
        project = get_current_project()
        project.load_history()  # Load existing history before adding new entry
        if mode == 'exam':
            project.history['exam_history'][timestamp] = {
                'score': score,
                'total': total,
                'percentage': percentage,
                'topics': session.get('topics', [])
            }
        else:
            project.history['study_history'][timestamp] = {
                'score': score,
                'total': total,
                'percentage': percentage,
                'topics': session.get('topics', [])
            }
        project.save_history()
            
    session.clear()
    return redirect(url_for('index'))

def get_feedback(question, user_answer, correct_answer, is_correct):
    """Generate helpful feedback for the user"""
    if is_correct:
        return f"✅ Correct! Your answer '{user_answer}' is right."
    else:
        return f"❌ Incorrect. Your answer was '{user_answer}', but the correct answer is '{correct_answer}'. Try to understand why this is the correct answer."

def check_answer(question, user_answer, correct_answer):
    """Enhanced answer checking with better evaluation logic"""
    if not all(isinstance(x, str) for x in [question, user_answer, correct_answer]):
        print("Warning: Non-string input in check_answer")
        return False
    
    # Normalize answers for comparison
    user_clean = user_answer.strip().lower()
    correct_clean = correct_answer.strip().lower()
    
    # Direct exact match (case-insensitive)
    if user_clean == correct_clean:
        return True
    
    # Handle True/False variations
    if correct_clean in ['true', 'false']:
        if user_clean in ['true', 't', 'yes', 'y', '1'] and correct_clean == 'true':
            return True
        if user_clean in ['false', 'f', 'no', 'n', '0'] and correct_clean == 'false':
            return True
    
    # Handle Yes/No variations
    if correct_clean in ['yes', 'no']:
        if user_clean in ['yes', 'y', 'true', 't', '1'] and correct_clean == 'yes':
            return True
        if user_clean in ['no', 'n', 'false', 'f', '0'] and correct_clean == 'no':
            return True
    
    # Handle Multiple Choice (single letter answers)
    if len(correct_clean) == 1 and correct_clean.isalpha():
        return user_clean == correct_clean
    
    # Handle Multiple Answer (comma-separated letters)
    if ',' in correct_clean:
        correct_answers = [ans.strip().lower() for ans in correct_clean.split(',')]
        user_answers = [ans.strip().lower() for ans in user_clean.split(',')]
        return set(correct_answers) == set(user_answers)
    
    # If we get here, it's likely a multiple choice question that wasn't properly classified
    # Default to exact match for any remaining cases
    return user_clean == correct_clean

# Fix percentage calculation to handle zero division
def calculate_percentage(score, total):
    try:
        return (score / total) * 100 if total > 0 else 0
    except ZeroDivisionError:
        return 0

if __name__ == '__main__':
    app.run(debug=True)