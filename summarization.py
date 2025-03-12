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
    In the summary, include at least one direct citation (an exact quote) from the text that supports your analysis.
    The citation should be enclosed in double quotes and reference the relevant section if possible.
    """
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]
    
    prompt = (
        "Focus on the theme of social isolation. Summarize the following text. "
        "In your summary, include at least one direct citation from the text (an exact quote) that supports your analysis of social isolation. "
        "Ensure that the citation is enclosed in double quotes and, if possible, indicate the section of the text.\n\n"
        f"{text}\n\n"
    )
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a helpful assistant that summarizes text with emphasis on social isolation and includes citations from the text."},
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
        "Compare these book summaries in terms of how they address social isolation. Make sure to include any direct citations (exact quotes) from the texts if present.\n"
        "Summaries:\n" + formatted_summaries + "\n\n"
        "Comparison:"
    )
    
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a helpful assistant that compares summaries with emphasis on social isolation and includes citations where applicable."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=300
    )
    analysis = response.choices[0].message["content"].strip()
    return analysis
