"""
Text preprocessing module for the AI Quiz Generator.
Handles cleaning, tokenization, and structuring of input text.
"""
import re
import logging
import nltk
from typing import Dict, Any, List

# Configure logger
logger = logging.getLogger(__name__)

def preprocess_text(text: str) -> Dict[str, Any]:
    """
    Preprocess text for question generation.
    
    Args:
        text: The input text to process
        
    Returns:
        A dictionary containing processed text data
    """
    logger.debug("Preprocessing text...")
    
    # Clean the text
    clean_text_result = clean_text(text)
    
    # Tokenize into sentences
    sentences = tokenize_sentences(clean_text_result)
    
    # Process with NLTK
    processed = process_with_nltk(clean_text_result, sentences)
    
    return processed

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove special characters that aren't relevant
    text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\'\"\(\)\[\]]', ' ', text)
    
    return text.strip()

def tokenize_sentences(text: str) -> List[str]:
    """Tokenize text into sentences."""
    try:
        # Make sure NLTK punkt tokenizer is downloaded
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        # Tokenize into sentences
        sentences = nltk.sent_tokenize(text)
        return sentences
    except Exception as e:
        logger.error(f"Error tokenizing sentences: {str(e)}")
        # Fallback to a simple sentence splitter
        return re.split(r'(?<=[.!?])\s+', text)

def process_with_nltk(text: str, sentences: List[str]) -> Dict[str, Any]:
    """Process text using NLTK."""
    try:
        # Make sure required NLTK resources are downloaded
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            logger.info("Downloading NLTK resources...")
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        
        from nltk.corpus import stopwords
        
        # Get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Process sentences
        processed_sentences = []
        for sentence in sentences:
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
                
            # Tokenize words
            words = nltk.word_tokenize(sentence)
            
            # Part-of-speech tagging
            pos_tags = nltk.pos_tag(words)
            
            # Filter out sentences without enough content words
            content_words = [word for word, tag in pos_tags 
                            if word.lower() not in stop_words and 
                            tag.startswith(('NN', 'VB', 'JJ', 'RB'))]
            
            if len(content_words) >= 3:
                processed_sentences.append({
                    'text': sentence,
                    'words': words,
                    'pos_tags': pos_tags
                })
        
        return {
            'original_text': text,
            'sentences': processed_sentences,
            'sentence_count': len(processed_sentences)
        }
    
    except Exception as e:
        logger.error(f"Error in NLTK processing: {str(e)}")
        # Return a simplified result if NLTK processing fails
        return {
            'original_text': text,
            'sentences': [{'text': s} for s in sentences if len(s.split()) >= 5],
            'sentence_count': len([s for s in sentences if len(s.split()) >= 5])
        }