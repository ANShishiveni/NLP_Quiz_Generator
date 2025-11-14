import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from app import db
from flask_login import UserMixin

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    theme_preference = db.Column(db.String(20), default='dark')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quizzes = db.relationship('QuizDB', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'

# SQLAlchemy database models
class QuizDB(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    topic = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('QuestionDB', backref='quiz', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class QuestionDB(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    options = db.Column(db.Text)  # JSON string
    correct_answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20))
    validated = db.Column(db.Boolean, default=False)
    validation_confidence = db.Column(db.Float, default=0.0)
    flagged = db.Column(db.Boolean, default=False)
    support_text = db.Column(db.Text)
    reference_source = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Question {self.id}: {self.text[:30]}...>'
    
    @property
    def options_list(self):
        if self.options:
            return json.loads(self.options)
        return []
    
    @options_list.setter
    def options_list(self, options_list):
        if options_list:
            self.options = json.dumps(options_list)
        else:
            self.options = None

# Dataclass models for easier handling in the application
@dataclass
class Question:
    id: int
    text: str
    type: str
    options: Optional[List[str]] = None
    correct_answer: str = ""
    difficulty: str = "medium"
    validated: bool = False
    validation_confidence: float = 0.0
    support_text: Optional[str] = None
    reference_source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_db(cls, db_question):
        return cls(
            id=db_question.id,
            text=db_question.text,
            type=db_question.type,
            options=db_question.options_list,
            correct_answer=db_question.correct_answer,
            difficulty=db_question.difficulty or "medium",
            validated=bool(db_question.validated),
            validation_confidence=db_question.validation_confidence or 0.0,
            support_text=db_question.support_text,
            reference_source=db_question.reference_source
        )
    
    def to_db(self, quiz_id=None):
        db_question = QuestionDB(
            text=self.text,
            type=self.type,
            correct_answer=self.correct_answer,
            difficulty=self.difficulty,
            validated=self.validated,
            validation_confidence=self.validation_confidence,
            flagged=False,
            support_text=self.support_text,
            reference_source=self.reference_source
        )
        if quiz_id:
            db_question.quiz_id = quiz_id
        if self.options:
            db_question.options_list = self.options
        return db_question

class QuestionFeedbackDB(db.Model):
    __tablename__ = 'question_feedback'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@dataclass
class Quiz:
    id: int
    title: str
    questions: List[Question] = field(default_factory=list)
    topic: str = ""
    difficulty: str = "medium"
    created_at: datetime = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.id,
            'title': self.title,
            'questions': [q.to_dict() for q in self.questions],
            'topic': self.topic,
            'difficulty': self.difficulty,
        }
        if self.created_at:
            result['created_at'] = self.created_at.isoformat()
        return result
    
    @classmethod
    def from_db(cls, db_quiz):
        """Create a Quiz dataclass instance from a QuizDB object"""
        questions = [Question.from_db(q) for q in db_quiz.questions]
        return cls(
            id=db_quiz.id,
            title=db_quiz.title,
            questions=questions,
            topic=db_quiz.topic,
            difficulty=db_quiz.difficulty,
            created_at=db_quiz.created_at
        )
    
    def to_db(self):
        """Convert to a QuizDB object"""
        db_quiz = QuizDB(
            title=self.title,
            topic=self.topic,
            difficulty=self.difficulty
        )
        if self.id:
            db_quiz.id = self.id
        return db_quiz
