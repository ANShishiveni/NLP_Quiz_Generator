import pytest
from nlp.preprocessor import preprocess_text
from nlp.question_generator import generate_questions, normalize_answer

def test_generate_questions_basic():
    text = "Physics studies matter and energy. Quantum mechanics describes subatomic phenomena. Newton formulated laws of motion."
    processed = preprocess_text(text)
    qs = generate_questions(processed, num_questions=3, difficulty='medium', question_types=['mcq','true_false','fill_blank'])
    assert len(qs) >= 1
    for q in qs:
        assert q.correct_answer
        assert q.difficulty in ('easy','medium','hard')
        assert isinstance(q.validated, bool)
        assert q.validation_confidence >= 0.0

def test_normalize_answer():
    assert normalize_answer("  Hello, World! ") == "hello world"