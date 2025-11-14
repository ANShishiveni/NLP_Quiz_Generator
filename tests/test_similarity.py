import pytest
from nlp.question_generator import cosine_similarity, normalize_answer

def test_cosine_similarity_basic():
    a = "Quantum mechanics"
    b = "Mechanics at the quantum level"
    c = "Banana elephant"
    assert cosine_similarity(a, b) > 0.25
    assert cosine_similarity(a, c) < 0.2