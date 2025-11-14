import pytest
from nlp.preprocessor import preprocess_text
from nlp.question_generator import generate_questions, verify_question, normalize_answer

def test_synonym_validation():
    text = "The automobile is parked outside. A car is a road vehicle, typically with four wheels."
    processed = preprocess_text(text)
    qs = generate_questions(processed, num_questions=1, difficulty='medium', question_types=['fill_blank'])
    assert qs
    q = qs[0]
    ok, conf, support = verify_question(processed['sentences'][0]['text'], q, processed['original_text'])
    assert conf >= 0.6