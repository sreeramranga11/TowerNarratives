import re
import nltk

def clean_text(text):
    """
    Cleans up the text by removing extra whitespace.
    
    This function uses a regular expression to replace any sequence of whitespace 
    characters (spaces, tabs, newlines) with a single space, then trims any leading 
    or trailing spaces from the resulting string.
    
    Parameters:
      text (str): The raw text input that may contain irregular spacing.
    
    Returns:
      str: The cleaned text with normalized spacing.
    """
    # Replace one or more whitespace characters with a single space and remove surrounding spaces.
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text, max_chars=4000):
    """
    Splits text into chunks, each having up to max_chars characters.
    
    The function uses sentence boundaries to ensure that sentences are not split in half.
    It tokenizes the text into individual sentences using NLTK's sentence tokenizer,
    then groups sentences into chunks such that the total length of a chunk does not exceed max_chars.
    
    Parameters:
      text (str): The input text to be divided into chunks.
      max_chars (int): The maximum number of characters allowed per chunk. Default is 4000.
    
    Returns:
      list of str: A list where each element is a text chunk with a length up to max_chars.
    """
    # List to store the resulting chunks.
    chunks = []
    # Variable to accumulate sentences into the current chunk.
    current_chunk = ""
    
    # Tokenize the input text into sentences.
    sentences = nltk.tokenize.sent_tokenize(text)
    
    # Iterate over each sentence.
    for sentence in sentences:
        # Check if adding the current sentence would exceed the maximum allowed characters.
        if len(current_chunk) + len(sentence) <= max_chars:
            # If not, append the sentence to the current chunk (with a preceding space).
            current_chunk += " " + sentence
        else:
            # Otherwise, add the current chunk (trimmed) to the list of chunks.
            chunks.append(current_chunk.strip())
            # Start a new chunk with the current sentence.
            current_chunk = sentence
    
    # After processing all sentences, add any remaining text as the last chunk.
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
