"""
Question generator module for the AI Quiz Generator.
Generates different types of questions based on preprocessed text.
"""
import random
import logging
import re
import nltk
from typing import Dict, Any, List, Optional
from sympy import symbols, sin, cos, simplify, latex, Integer
from models import Question

# Configure logger
logger = logging.getLogger(__name__)

def generate_questions(processed_text: Dict[str, Any], 
                      num_questions: int = 5, 
                      difficulty: str = 'medium',
                      question_types: Optional[List[str]] = None) -> List[Question]:
    """
    Generate questions based on preprocessed text.
    
    Args:
        processed_text: Preprocessed text data
        num_questions: Number of questions to generate
        difficulty: Difficulty level ('easy', 'medium', 'hard')
        question_types: List of question types to generate ('mcq', 'true_false', 'fill_blank')
        
    Returns:
        List of Question objects
    """
    logger.debug(f"Generating {num_questions} questions with difficulty '{difficulty}'")
    
    if question_types is None:
        question_types = ['mcq', 'true_false', 'fill_blank']
    
    sentences = [s['text'] for s in processed_text.get('sentences', [])]
    
    # Make sure we have enough sentences
    if len(sentences) < num_questions:
        logger.warning(f"Not enough sentences ({len(sentences)}) for requested questions ({num_questions})")
        num_questions = min(num_questions, len(sentences))
    
    # Select random sentences for question generation
    if len(sentences) > num_questions:
        selected_sentences = random.sample(sentences, num_questions)
    else:
        selected_sentences = sentences
    
    questions = []
    for i, sentence in enumerate(selected_sentences):
        # Choose a random question type from the allowed types
        question_type = random.choice(question_types)
        
        # Generate question based on type
        if question_type == 'mcq':
            question = generate_mcq(sentence, difficulty, i+1)
        elif question_type == 'true_false':
            question = generate_true_false(sentence, difficulty, i+1)
        elif question_type == 'fill_blank':
            question = generate_fill_blank(sentence, difficulty, i+1)
        elif question_type == 'math':
            question = generate_math_question(difficulty, i+1)
        else:
            logger.warning(f"Unknown question type: {question_type}")
            continue
        
        if question:
            d = classify_difficulty(sentence)
            question.difficulty = d
            validated, conf, support = verify_question(sentence, question, processed_text.get('original_text', ''))
            question.validated = validated
            question.validation_confidence = conf
            question.support_text = support
            question.reference_source = 'input_text'
            questions.append(question)
    
    return questions

def generate_math_question(difficulty: str, question_id: int) -> Optional[Question]:
    try:
        x = symbols('x')
        kind = random.choice(['arithmetic','simplify']) if difficulty != 'hard' else random.choice(['simplify','arithmetic'])
        if kind == 'arithmetic':
            a = random.randint(1, 12)
            b = random.randint(1, 12)
            c = random.randint(1, 12) if difficulty != 'easy' else random.randint(1, 6)
            expr_val = a + b * c
            q_text = f"Compute: $ {a} + {b} \\times {c} $"
            return Question(id=question_id, text=q_text, type='math', options=None, correct_answer=str(Integer(expr_val)))
        s_expr = sin(x)**2 + cos(x)**2
        s_simpl = simplify(s_expr)
        q_text = f"Simplify: $ {latex(s_expr)} $"
        return Question(id=question_id, text=q_text, type='math', options=None, correct_answer=str(s_simpl))
    except Exception:
        return None

def generate_mcq(sentence: str, difficulty: str, question_id: int) -> Optional[Question]:
    """Generate a multiple-choice question from a sentence."""
    try:
        # Extract a potential answer from the sentence
        answer = extract_answer(sentence)
        
        if not answer:
            return None
        
        # Create a question from the sentence
        question_text = create_question_from_sentence(sentence, answer)
        
        # Generate distractors (incorrect options)
        distractors = generate_distractors(answer, sentence, difficulty)
        
        # Combine answer and distractors
        options = [answer] + distractors[:3]  # Limit to 3 distractors for 4 total options
        
        # Shuffle options
        random.shuffle(options)
        
        return Question(
            id=question_id,
            text=question_text,
            type='mcq',
            options=options,
            correct_answer=answer
        )
    except Exception as e:
        logger.error(f"Error generating MCQ: {str(e)}")
        return None

def generate_true_false(sentence: str, difficulty: str, question_id: int) -> Optional[Question]:
    """Generate a true/false question from a sentence."""
    try:
        # Decide if the statement should be true or false
        is_true = random.choice([True, False])
        
        if is_true:
            # Use the original sentence
            question_text = sentence
            correct_answer = "True"
        else:
            # Modify the sentence to make it false
            question_text = modify_sentence_to_false(sentence)
            correct_answer = "False"
        
        return Question(
            id=question_id,
            text=question_text,
            type='true_false',
            options=["True", "False"],
            correct_answer=correct_answer
        )
    except Exception as e:
        logger.error(f"Error generating true/false question: {str(e)}")
        return None

def generate_fill_blank(sentence: str, difficulty: str, question_id: int) -> Optional[Question]:
    """Generate a fill-in-the-blank question from a sentence."""
    try:
        # Extract a potential answer from the sentence
        answer = extract_answer(sentence)
        
        if not answer:
            return None
        
        # Replace the answer with a blank in the sentence
        pattern = re.compile(re.escape(answer), re.IGNORECASE)
        question_text = pattern.sub("__________", sentence, count=1)
        
        return Question(
            id=question_id,
            text=question_text,
            type='fill_blank',
            options=None,
            correct_answer=answer
        )
    except Exception as e:
        logger.error(f"Error generating fill-in-blank question: {str(e)}")
        return None

def create_question_from_sentence(sentence: str, answer: str) -> str:
    """Convert a sentence into a question based on the answer."""
    # Remove the answer from the sentence
    pattern = re.compile(re.escape(answer), re.IGNORECASE)
    question = pattern.sub("_____", sentence, count=1)
    
    # Convert to a question format
    question = f"Which of the following correctly completes this sentence: {question}"
    
    return question

def modify_sentence_to_false(sentence: str) -> str:
    """Modify a sentence to make it false."""
    # Try to negate the main verb
    pattern = r'\b(is|are|was|were|has|have|had|do|does|did)\b'
    match = re.search(pattern, sentence)
    
    if match:
        # Negate the auxiliary verb
        verb = match.group(1)
        negation_map = {
            'is': 'is not', 'are': 'are not', 'was': 'was not', 'were': 'were not',
            'has': 'has not', 'have': 'have not', 'had': 'had not',
            'do': 'do not', 'does': 'does not', 'did': 'did not'
        }
        negated_verb = negation_map.get(verb, verb + ' not')
        modified = sentence[:match.start()] + negated_verb + sentence[match.end():]
        return modified
    
    # Alternative: replace a key word
    return replace_key_word(sentence)

def replace_key_word(sentence: str) -> str:
    """Replace a key word in the sentence to alter its meaning."""
    try:
        # Make sure we have the required NLTK resources
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger', quiet=True)
        
        # Tokenize and tag parts of speech
        words = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        
        # Find nouns, verbs, or adjectives to replace
        replaceable_words = [(i, word) for i, (word, tag) in enumerate(pos_tags) 
                            if tag.startswith(('NN', 'VB', 'JJ')) and len(word) > 3]
        
        if replaceable_words:
            # Select a random word to replace
            idx, word = random.choice(replaceable_words)
            
            # Replace with an antonym or just a different word
            antonyms = {
                'large': 'small', 'big': 'small', 'small': 'large',
                'good': 'bad', 'bad': 'good', 'best': 'worst', 'worst': 'best',
                'right': 'wrong', 'wrong': 'right', 'correct': 'incorrect', 'incorrect': 'correct',
                'high': 'low', 'low': 'high', 'tall': 'short', 'short': 'tall',
                'hot': 'cold', 'cold': 'hot', 'warm': 'cool', 'cool': 'warm',
                'increase': 'decrease', 'decrease': 'increase', 'up': 'down', 'down': 'up',
                'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east',
                'early': 'late', 'late': 'early', 'first': 'last', 'last': 'first',
                'new': 'old', 'old': 'new', 'young': 'old', 'ancient': 'modern',
                'important': 'trivial', 'significant': 'insignificant',
                'positive': 'negative', 'negative': 'positive',
                'true': 'false', 'false': 'true'
            }
            
            replacement = antonyms.get(word.lower())
            if not replacement:
                # If no antonym is found, use a random unrelated word
                unrelated_words = ['banana', 'elephant', 'rocket', 'pizza', 'guitar', 
                                  'castle', 'diamond', 'tornado', 'rainbow', 'volcano']
                replacement = random.choice(unrelated_words)
            
            # Replace the word in the sentence
            words[idx] = replacement
            modified = ' '.join(words)
            
            # Fix capitalization
            if sentence[0].isupper():
                modified = modified[0].upper() + modified[1:]
            
            return modified
    
    except Exception as e:
        logger.error(f"Error replacing word: {str(e)}")
    
    # Fallback: add "not" somewhere in the middle
    words = sentence.split()
    mid_point = len(words) // 2
    words.insert(mid_point, "not")
    return ' '.join(words)

def extract_answer(sentence: str) -> Optional[str]:
    """Extract a potential answer from a sentence."""
    try:
        # Make sure we have the required NLTK resources
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger', quiet=True)
        
        # Tokenize and tag parts of speech
        words = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        
        # Look for noun phrases, proper nouns, or other important terms
        candidates = []
        
        # Find consecutive nouns (simple noun phrases)
        current_phrase = []
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                current_phrase.append(word)
            elif current_phrase:
                if len(current_phrase) > 0:
                    candidates.append(' '.join(current_phrase))
                current_phrase = []
        
        # Add the last phrase if there is one
        if current_phrase:
            candidates.append(' '.join(current_phrase))
        
        # Find proper nouns (names, places, etc.)
        proper_nouns = [word for word, tag in pos_tags if tag == 'NNP']
        if proper_nouns:
            candidates.extend(proper_nouns)
        
        # Find numbers and dates
        numbers = [word for word, tag in pos_tags if tag == 'CD']
        if numbers:
            candidates.extend(numbers)
        
        # Select the best candidate
        if candidates:
            # Choose a longer one if available for better context
            candidates.sort(key=len, reverse=True)
            return candidates[0]
    
    except Exception as e:
        logger.error(f"Error extracting answer: {str(e)}")
    
    # Fallback: use a random substantial word
    words = [w for w in sentence.split() if len(w) > 4]
    if words:
        return random.choice(words)
    
    return None

def generate_distractors(answer: str, context: str, difficulty: str) -> List[str]:
    """Generate distractors (incorrect options) for a multiple-choice question."""
    # Simple implementation: use random words from the context
    words = [w for w in context.split() if w.lower() != answer.lower() and len(w) > 3]
    
    # Ensure we have enough words
    if len(words) < 3:
        # Add some generic distractors
        generic_distractors = [
            "None of the above", "All of the above", 
            "Cannot be determined", "Not mentioned",
            "Unknown", "No evidence provided"
        ]
        words.extend(generic_distractors)
    
    # Shuffle and take the first 3
    random.shuffle(words)
    return words[:3]

def classify_difficulty(sentence: str) -> str:
    w = len(sentence.split())
    if w >= 20:
        return 'hard'
    if w >= 12:
        return 'medium'
    return 'easy'

def normalize_answer(text: Optional[str]) -> str:
    if not text:
        return ''
    t = re.sub(r"[^A-Za-z0-9 ]", " ", text.lower())
    t = re.sub(r"\s+", " ", t).strip()
    return t

def _tf(tokens: List[str]) -> Dict[str, float]:
    d: Dict[str, float] = {}
    for tok in tokens:
        d[tok] = d.get(tok, 0.0) + 1.0
    total = float(len(tokens)) or 1.0
    for k in d:
        d[k] /= total
    return d

def cosine_similarity(a: str, b: str) -> float:
    ta = normalize_answer(a).split()
    tb = normalize_answer(b).split()
    fa = _tf(ta)
    fb = _tf(tb)
    keys = set(fa.keys()) | set(fb.keys())
    dot = sum(fa.get(k, 0.0) * fb.get(k, 0.0) for k in keys)
    na = sum(v*v for v in fa.values()) ** 0.5
    nb = sum(v*v for v in fb.values()) ** 0.5
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)

def verify_question(sentence: str, question: Question, original_text: str) -> (bool, float, str):
    s_norm = normalize_answer(sentence)
    a_norm = normalize_answer(question.correct_answer)
    in_sentence = a_norm and a_norm in s_norm
    in_text = False
    if original_text:
        in_text = a_norm in normalize_answer(original_text)
    syn_ok, np_ok = False, False
    try:
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet', quiet=True)
        from nltk.corpus import wordnet as wn
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        def lemmas(word: str) -> List[str]:
            l = [lemmatizer.lemmatize(word, pos='n'), lemmatizer.lemmatize(word, pos='v'), lemmatizer.lemmatize(word, pos='a')]
            return list({w for w in l if w})
        def synonyms(word: str) -> List[str]:
            syns = []
            for syn in wn.synsets(word):
                for lem in syn.lemmas():
                    syns.append(lem.name().replace('_', ' '))
            return list({w.lower() for w in syns})
        answer_tokens = [t for t in re.split(r"\s+", a_norm) if t]
        syn_matches = 0
        for tok in answer_tokens:
            tok_forms = set([tok] + lemmas(tok) + synonyms(tok))
            if any(normalize_answer(f) in s_norm for f in tok_forms):
                syn_matches += 1
        syn_ok = syn_matches >= max(1, len(answer_tokens)//2)
        words = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(words)
        np_tokens = []
        current = []
        for w, tag in tags:
            if tag.startswith('NN'):
                current.append(normalize_answer(w))
            elif current:
                np_tokens.append(' '.join(current))
                current = []
        if current:
            np_tokens.append(' '.join(current))
        np_ok = any(a_norm in np for np in np_tokens)
    except Exception:
        pass
    cos_s = cosine_similarity(question.correct_answer, sentence)
    cos_t = cosine_similarity(question.correct_answer, original_text) if original_text else 0.0
    cos_ok = max(cos_s, cos_t) >= 0.25
    ok = in_sentence or in_text or syn_ok or np_ok or cos_ok
    conf = 1.0 if in_sentence else (0.9 if in_text else (0.75 if syn_ok else (0.65 if np_ok else (0.55 if cos_ok else 0.3))))
    return ok, conf, sentence