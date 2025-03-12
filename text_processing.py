import re
import nltk

# Uncomment the next line on first run to download required tokenizer data
# nltk.download('punkt')

def clean_text(text):
    """
    Cleans up the text by removing extra whitespace.
    """
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text, max_chars=4000):
    """
    Splits text into chunks of up to max_chars characters.
    Uses sentence boundaries to avoid cutting sentences in half.
    """
    chunks = []
    current_chunk = ""
    sentences = nltk.tokenize.sent_tokenize(text)
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
