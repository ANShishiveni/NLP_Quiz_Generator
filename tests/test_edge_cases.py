import pytest
from nlp.preprocessor import preprocess_text
from nlp.question_generator import generate_questions

def test_very_short_text():
    text = "Math rules."
    processed = preprocess_text(text)
    qs = generate_questions(processed, num_questions=3)
    assert isinstance(qs, list)

def test_ambiguous_sentence():
    text = "A set is a collection of distinct objects; the word set has many meanings."
    processed = preprocess_text(text)
    qs = generate_questions(processed, num_questions=2, question_types=['mcq','fill_blank'])
    assert len(qs) >= 1