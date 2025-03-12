import os
import hashlib
from dotenv import load_dotenv
import openai

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple cache to avoid duplicate summarization calls
cache = {}

def summarize_text(text):
    """
    Summarizes the given text with emphasis on the theme of social isolation.
    Uses the OpenAI API (gpt-4o-mini-2024-07-18).
    """
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]
    
    prompt = f"Focus on the theme of social isolation. Summarize the following text:\n\n{text}. Make sure to wrap the name of the book in quotation marks."
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a helpful assistant that summarizes text with emphasis on social isolation."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=150
    )
    summary = response.choices[0].message["content"].strip()
    cache[key] = summary
    return summary

def analyze_comparative(summaries):
    """
    Compares the summaries from three books and returns a comparative analysis.
    Uses the OpenAI API (gpt-4o-mini-2024-07-18).
    """
    formatted_summaries = "\n\n".join(summaries)
    
    prompt = (
        "Compare these book summaries in terms of how they address social isolation. Make sure to wrap the name of the book in quotation marks. \n"
        "Summaries:\n" + formatted_summaries + "\n\n"
        "Comparison:"
    )
    
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a helpful assistant that compares summaries with emphasis on social isolation."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=300
    )
    analysis = response.choices[0].message["content"].strip()
    return analysis
