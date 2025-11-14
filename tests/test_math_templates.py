import pytest
from nlp.preprocessor import preprocess_text
from nlp.question_generator import generate_questions
from sympy import sympify

def test_generate_math_questions_only():
    text = "Mathematics includes arithmetic and trigonometry."
    processed = preprocess_text(text)
    qs = generate_questions(processed, num_questions=3, difficulty='medium', question_types=['math'])
    assert qs and all(q.type == 'math' for q in qs)
    assert any('$' in q.text for q in qs)
    for q in qs:
        assert isinstance(sympify(q.correct_answer), object)

def test_latex_parsing_equivalence_available():
    from sympy.parsing.latex import parse_latex
    e1 = parse_latex(r"x^{2}")
    e2 = sympify("x**2")
    assert (e1 - e2).simplify() == 0