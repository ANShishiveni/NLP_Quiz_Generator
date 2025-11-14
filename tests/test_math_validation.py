import pytest
from nlp.question_generator import normalize_answer
from sympy import sympify, pi, simplify

def test_numeric_equivalence():
    assert simplify(sympify("2+2") - sympify("4")) == 0

def test_symbolic_equivalence():
    assert simplify(sympify("sin(x)**2 + cos(x)**2") - sympify("1")) == 0

def test_pi_approx():
    assert abs(float(sympify("3.14159")) - float(pi)) < 1e-3