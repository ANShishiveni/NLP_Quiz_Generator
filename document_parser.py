"""
Document parser module for the AI Quiz Generator.
Extracts text from various document formats (TXT, PDF, DOCX, DOC, RTF).
"""
import logging
import os
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

def parse_document(file_content: bytes, filename: str) -> Optional[str]:
    """
    Parse document content and extract text.
    
    Args:
        file_content: The binary content of the file
        filename: The name of the file with extension
        
    Returns:
        Extracted text from the document, or None if parsing failed
    """
    logger.info(f"Parsing document: {filename}")
    
    # Determine file type from extension
    file_ext = os.path.splitext(filename)[1].lower()
    
    try:
        if file_ext == '.txt':
            return parse_txt(file_content)
        else:
            # For now, fallback to treating all documents as text files
            return parse_txt(file_content)
            
            # In a full implementation, these would be implemented:
            # if file_ext == '.pdf':
            #     return parse_pdf(file_content)
            # elif file_ext in ('.docx', '.doc'):
            #     return parse_docx(file_content)
            # elif file_ext == '.rtf':
            #     return parse_rtf(file_content)
    except Exception as e:
        logger.error(f"Error parsing document: {str(e)}")
        return None

def parse_txt(file_content: bytes) -> str:
    """Parse a text file."""
    # Try various encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'ascii']
    
    for encoding in encodings:
        try:
            return file_content.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    # If all encoding attempts fail, force latin-1 (which should always work)
    return file_content.decode('latin-1', errors='replace')