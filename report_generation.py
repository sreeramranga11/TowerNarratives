import os
from dotenv import load_dotenv
import openai

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_thesis(book_summaries, comparative_analysis):
    """
    Generates a thesis statement based on the provided book summaries and comparative analysis.
    Uses the OpenAI API (gpt-4o-mini-2024-07-18).
    """
    formatted_summaries = "\n\n".join(book_summaries)
    prompt = (
        "Based on the following book summaries and comparative analysis, generate a clear thesis statement that discusses "
        "how the novels address social isolation. Make sure to wrap the name of the book in quotation marks. \n\n"
        "Book Summaries:\n" + formatted_summaries + "\n\n" +
        "Comparative Analysis:\n" + comparative_analysis + "\n\n"
        "Thesis Statement:"
    )
    
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are an expert literary critic."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=150
    )
    thesis = response.choices[0].message["content"].strip()
    return thesis

def generate_paragraph(paragraph_index, thesis, book_summaries, comparative_analysis):
    """
    Generates an individual paragraph based on the specified index, ensuring that the output is exactly 4-5 sentences long
    and that publication titles are enclosed in double quotes.
      1: Introductory paragraph that presents the topic and ends with the thesis statement.
      2: Body paragraph discussing details from the first novel.
      3: Body paragraph discussing details from the second novel.
      4: Body paragraph discussing details from the third novel.
      5: Concluding paragraph that presents a rebuttal of a counterargument and summarizes the report.
    """
    instruction = (
        "Ensure your response is exactly 4-5 sentences long. "
        "Also, use double quotes (\") around publication titles instead of asterisks (*)."
    )
    
    if paragraph_index == 1:
        prompt = (
            "Generate an introductory paragraph about how three novels address social isolation. "
            "Introduce the topic and end the paragraph with the following thesis statement: " + thesis + ". "
            + instruction
        )
    elif paragraph_index == 2:
        prompt = (
            "Generate a body paragraph that discusses details from the first novel in support of the thesis. "
            "Use the following summary for reference: " + book_summaries[0] + ". "
            + instruction
        )
    elif paragraph_index == 3:
        prompt = (
            "Generate a body paragraph that discusses details from the second novel in support of the thesis. "
            "Use the following summary for reference: " + book_summaries[1] + ". "
            + instruction
        )
    elif paragraph_index == 4:
        prompt = (
            "Generate a body paragraph that discusses details from the third novel in support of the thesis. "
            "Use the following summary for reference: " + book_summaries[2] + ". "
            + instruction
        )
    elif paragraph_index == 5:
        prompt = (
            "Generate a concluding paragraph that presents a rebuttal to a counterargument against the thesis and summarizes the overall analysis. "
            "Use the following comparative analysis as a reference: " + comparative_analysis + ". "
            + instruction
        )
    else:
        prompt = ""
    
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a skilled writer who creates detailed book reports."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=300
    )
    paragraph = response.choices[0].message["content"].strip()
    return paragraph

def generate_report(thesis, book_summaries, comparative_analysis):
    """
    Generates a complete book report by asking GPT to generate each of the 5 paragraphs individually,
    then combines them (separated by two newlines) to form the final report.
    """
    paragraphs = []
    for i in range(1, 6):
        print(f"Generating paragraph {i}...")
        para = generate_paragraph(i, thesis, book_summaries, comparative_analysis)
        paragraphs.append(para)
    # Combine paragraphs with two newlines between each.
    report = "\n\n".join(paragraphs)
    return report
