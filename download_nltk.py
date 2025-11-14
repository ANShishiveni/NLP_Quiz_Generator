"""
Script to download required NLTK resources for the quiz generator.
"""
import nltk
import os
import ssl

def download_nltk_resources():
    """Download all required NLTK resources for the quiz generator."""
    print("Downloading NLTK resources...")
    
    # Create a directory for NLTK data if it doesn't exist
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Set NLTK data path
    nltk.data.path.append(nltk_data_dir)
    
    # Fix SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Download required resources
    resources = [
        'punkt',         # For sentence tokenization
        'stopwords',     # For stop words filtering
        'averaged_perceptron_tagger',  # For part-of-speech tagging
        'wordnet'        # For semantic word operations
    ]
    
    for resource in resources:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)
            print(f"Downloaded {resource} successfully.")
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")
    
    print("NLTK resource download complete.")

if __name__ == "__main__":
    download_nltk_resources()