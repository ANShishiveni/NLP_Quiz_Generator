import pytest
from nlp.question_generator import normalize_answer

def test_fill_blank_validation():
    a = normalize_answer("Quantum mechanics")
    u = normalize_answer("The field of quantum mechanics explains particles.")
    assert a in u