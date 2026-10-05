from flask import Blueprint, render_template, jsonify, request, session, flash, redirect, url_for
from flask_login import current_user, login_required
import json
import logging
import traceback
from app import db
from models import Quiz, Question, QuizDB, QuestionDB, User, QuestionFeedbackDB
from nlp.preprocessor import preprocess_text
from nlp.question_generator import generate_questions, normalize_answer
from sympy import sympify, simplify
from sympy.parsing.latex import parse_latex
from sympy.core.numbers import Float
from document_parser import parse_document
from topics import TOPICS, TOPIC_TEXTS, get_all_topic_data

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

# In-memory storage for generated quizzes
quizzes = {}

@main.route('/')
def index():
    """Render the main page"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    # Get all topic data including subtopics and descriptions
    topic_data = get_all_topic_data()
    
    # Set theme from user preference if not already in session
    if current_user.is_authenticated and 'theme' not in session:
        session['theme'] = current_user.theme_preference
    
    return render_template('index.html', 
                          topics=TOPICS, 
                          topic_data=topic_data,
                          theme=session.get('theme', 'dark'))

@main.route('/metrics')
@login_required
def metrics_page():
    return render_template('metrics.html', theme=session.get('theme', 'dark'))

@main.route('/api/topics', methods=['GET'])
@login_required
def get_topics():
    """Return available topics with detailed information"""
    return jsonify({"topics": get_all_topic_data()})

@main.route('/api/quizzes', methods=['GET'])
@login_required
def get_quizzes():
    """Return all quizzes from the database for the current user"""
    try:
        db_quizzes = QuizDB.query.filter_by(user_id=current_user.id).order_by(QuizDB.created_at.desc()).all()
        quizzes_list = []
        
        for db_quiz in db_quizzes:
            quiz = {
                'id': db_quiz.id,
                'title': db_quiz.title,
                'topic': db_quiz.topic,
                'difficulty': db_quiz.difficulty,
                'created_at': db_quiz.created_at.isoformat() if db_quiz.created_at else None,
                'question_count': len(db_quiz.questions)
            }
            quizzes_list.append(quiz)
            
        return jsonify({"quizzes": quizzes_list})
    except Exception as e:
        logger.error(f"Error fetching quizzes: {str(e)}")
        return jsonify({"error": "Failed to fetch quizzes"}), 500

@main.route('/api/generate-quiz', methods=['POST'])
@login_required
def generate_quiz():
    """Generate a quiz based on provided text or selected topic"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        content_type = data.get('contentType')
        if not content_type:
            return jsonify({"error": "Content type not specified"}), 400
            
        num_questions = int(data.get('numQuestions', 5))
        difficulty = data.get('difficulty', 'medium')
        question_types = data.get('questionTypes', ['mcq', 'true_false', 'fill_blank'])
        
        if not question_types:
            return jsonify({"error": "No question types selected"}), 400
    
        # Get text either from direct input or from a selected topic
        if content_type == 'text':
            text = data.get('text', '')
            if not text:
                return jsonify({"error": "No text provided"}), 400
            topic = "Custom Text"
        elif content_type == 'topic':
            topic = data.get('topic')
            subtopic = data.get('subtopic')
            
            # If a subtopic is provided, use its content
            if subtopic and subtopic in TOPIC_TEXTS.get(topic, {}):
                text = TOPIC_TEXTS[topic][subtopic]
            elif topic in TOPIC_TEXTS:
                # If only main topic is provided, get the main topic text or combine all subtopics
                if isinstance(TOPIC_TEXTS[topic], str):
                    text = TOPIC_TEXTS[topic]
                else:
                    # Combine all subtopic texts
                    text = "\n\n".join(TOPIC_TEXTS[topic].values())
            else:
                return jsonify({"error": "Invalid topic selected"}), 400
        else:  # file upload handled separately
            return jsonify({"error": "Invalid content type"}), 400
        
        # Process text
        logger.debug(f"Processing text: {text[:100]}...")
        processed_text = preprocess_text(text)
        
        # Generate questions
        questions = generate_questions(
            processed_text, 
            num_questions=num_questions,
            difficulty=difficulty,
            question_types=question_types
        )
        
        # Create quiz object
        new_quiz = Quiz(
            id=0,  # Will be set by database
            title=f"Quiz on {topic}",
            questions=questions,
            topic=topic,
            difficulty=difficulty
        )
        
        # Save to database
        db_quiz = new_quiz.to_db()
        db_quiz.user_id = current_user.id  # Associate quiz with current user
        db.session.add(db_quiz)
        db.session.flush()  # To get the ID
        
        # Add questions to database
        for question in questions:
            db_question = question.to_db(quiz_id=db_quiz.id)
            db.session.add(db_question)
        try:
            db.session.commit()
        except Exception as e:
            try:
                if db.engine.url.drivername.startswith('sqlite'):
                    with db.engine.begin() as conn:
                        rows = conn.exec_driver_sql("PRAGMA table_info(questions)").fetchall()
                        cols = [row[1] for row in rows]
                        stmts = []
                        if "difficulty" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN difficulty TEXT")
                        if "validated" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN validated BOOLEAN DEFAULT 0")
                        if "validation_confidence" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN validation_confidence REAL DEFAULT 0.0")
                        if "flagged" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN flagged BOOLEAN DEFAULT 0")
                        if "support_text" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN support_text TEXT")
                        if "reference_source" not in cols:
                            stmts.append("ALTER TABLE questions ADD COLUMN reference_source TEXT")
                        for s in stmts:
                            conn.exec_driver_sql(s)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
        # Retrieve the complete quiz with its ID
        saved_quiz = Quiz.from_db(db_quiz)
        
        # Also keep in memory for backward compatibility
        quizzes[saved_quiz.id] = saved_quiz.to_dict()
        
        return jsonify({"quiz": saved_quiz.to_dict(), "quizId": saved_quiz.id})
    
    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Error generating quiz: {str(e)}\n{error_traceback}")
        return jsonify({"error": f"Failed to generate quiz: {str(e)}"}), 500

@main.route('/api/quiz/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    """Retrieve a specific quiz by ID"""
    # Always authorize against the database before using the in-memory cache.
    db_quiz = QuizDB.query.get(quiz_id)
    if not db_quiz:
        return jsonify({"error": "Quiz not found"}), 404
    if db_quiz.user_id != current_user.id:
        return jsonify({"error": "Unauthorized access to quiz"}), 403

    quiz = quizzes.get(quiz_id)
    if not quiz:
        quiz_obj = Quiz.from_db(db_quiz)
        quiz = quiz_obj.to_dict()
        quizzes[quiz_id] = quiz
    
    return jsonify({"quiz": quiz})

@main.route('/api/upload-document', methods=['POST'])
@login_required
def upload_document():
    """Upload a document and extract text for quiz generation"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if file:
        # Read the file content
        file_content = file.read()
        
        # Parse the document
        text = parse_document(file_content, file.filename)
        
        if not text:
            return jsonify({"error": "Could not extract text from the document"}), 400
            
        # Return the extracted text
        return jsonify({"text": text})
    
    return jsonify({"error": "File upload failed"}), 400

@main.route('/api/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    """Submit a completed quiz and get results"""
    data = request.json
    quiz_id = data.get('quizId')
    answers = data.get('answers', {})
    
    # Authorize ownership before consulting the shared in-memory cache.
    db_quiz = QuizDB.query.get(quiz_id)
    if not db_quiz:
        return jsonify({"error": "Invalid quiz ID"}), 400
    if db_quiz.user_id != current_user.id:
        return jsonify({"error": "Unauthorized access to quiz"}), 403

    quiz = quizzes.get(quiz_id)
    if not quiz:
        quiz_obj = Quiz.from_db(db_quiz)
        quiz = quiz_obj.to_dict()
        quizzes[quiz_id] = quiz
    
    score = 0
    results = []
    
    # Calculate score and prepare feedback
    def answers_equal(user_answer, correct_answer, q_type):
        ua = user_answer or ""
        ca = correct_answer or ""
        ua_n = normalize_answer(ua)
        ca_n = normalize_answer(ca)
        if q_type in ('mcq', 'fill_blank', 'true_false', 'math'):
            try:
                e1 = sympify(ua)
                e2 = sympify(ca)
                if isinstance(e1, Float) or isinstance(e2, Float):
                    try:
                        return abs(float(e1) - float(e2)) <= 1e-6
                    except Exception:
                        pass
                return simplify(e1 - e2) == 0
            except Exception:
                try:
                    e1 = parse_latex(ua)
                    e2 = parse_latex(ca)
                    return simplify(e1 - e2) == 0
                except Exception:
                    pass
        if q_type == 'fill_blank':
            return ca_n in ua_n
        return ua_n == ca_n

    for question in quiz['questions']:
        q_id = question['id']
        user_answer = answers.get(str(q_id))
        correct_answer = question['correct_answer']
        is_correct = False
        
        if question['type'] in ('mcq','true_false','fill_blank','math'):
            is_correct = answers_equal(user_answer, correct_answer, question['type'])
        
        if is_correct:
            d = question.get('difficulty', 'medium')
            w = 2 if d == 'medium' else (3 if d == 'hard' else 1)
            score += w
            
        results.append({
            'question_id': q_id,
            'correct': is_correct,
            'user_answer': user_answer,
            'correct_answer': correct_answer
        })
    
    # Calculate percentage
    total_weight = sum(2 if q.get('difficulty','medium')=='medium' else (3 if q.get('difficulty')=='hard' else 1) for q in quiz['questions']) if quiz['questions'] else 0
    percentage = (score / total_weight) * 100 if total_weight else 0
    
    return jsonify({
        'score': score,
        'total': total_weight,
        'percentage': percentage,
        'results': results
    })

@main.route('/api/report-question', methods=['POST'])
@login_required
def report_question():
    data = request.json or {}
    question_id = data.get('questionId')
    reason = data.get('reason')
    if not question_id or not reason:
        return jsonify({'error': 'Missing questionId or reason'}), 400
    feedback = QuestionFeedbackDB(question_id=question_id, user_id=current_user.id if current_user.is_authenticated else None, reason=reason)
    db.session.add(feedback)
    q = QuestionDB.query.get(question_id)
    if q:
        q.flagged = True
    db.session.commit()
    return jsonify({'status': 'ok'})

@main.route('/api/metrics', methods=['GET'])
@login_required
def metrics():
    total = QuestionDB.query.count()
    validated = QuestionDB.query.filter_by(validated=True).count()
    flagged = QuestionDB.query.filter_by(flagged=True).count()
    avg_conf = db.session.query(db.func.avg(QuestionDB.validation_confidence)).scalar() or 0.0
    return jsonify({'total_questions': total, 'validated': validated, 'flagged': flagged, 'validation_rate': (validated/total*100 if total else 0), 'avg_confidence': avg_conf})

@main.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark theme"""
    current_theme = session.get('theme', 'dark')
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    session['theme'] = new_theme
    
    # If user is logged in, update their preference
    if current_user.is_authenticated:
        current_user.theme_preference = new_theme
        db.session.commit()
    
    return jsonify({'theme': new_theme})
