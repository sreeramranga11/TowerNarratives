import os
from dotenv import load_dotenv
import openai

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_title(thesis):
    """
    Generates a short, interesting, and unique title based on the provided thesis statement.
    
    Parameters:
      - thesis (str): The thesis statement to base the title on.
    
    Returns:
      - str: A short and unique title.
    
    Process:
      - Constructs a prompt instructing GPT to generate a title based on the thesis.
      - Calls the OpenAI API using the GPT-4o-mini model.
      - Returns the generated title.
    """
    prompt = (
        "Based on the following thesis statement, generate a short, interesting, and unique title in around 5 words for a book report on social isolation:\n\n"
        + thesis + "\n\nTitle:"
    )
    response = openai.ChatCompletion.create(
         model="gpt-4o-mini-2024-07-18",
         messages=[
             {"role": "system", "content": "You are a creative writer."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
         max_tokens=20
    )
    title = response.choices[0].message["content"].strip()
    return title

def generate_thesis(book_summaries, comparative_analysis):
    """
    Generates a thesis statement based on the provided book summaries and comparative analysis.
    Uses the OpenAI API (gpt-4o-mini-2024-07-18).
    
    The prompt instructs GPT to wrap publication names in double quotes.
    
    Parameters:
      - book_summaries: List of summaries for each book.
      - comparative_analysis: A comparative analysis of the summaries.
    
    Returns:
      - A string containing the generated thesis statement.
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
    
    Structure:
      - Paragraph 1: Introductory paragraph that presents the topic and ends with the thesis statement.
      - Paragraph 2: Body paragraph discussing details from the first novel.
      - Paragraph 3: Body paragraph discussing details from the second novel.
      - Paragraph 4: Body paragraph discussing details from the third novel.
      - Paragraph 5: Concluding paragraph that presents a rebuttal of a counterargument and summarizes the report.
    
    Parameters:
      - paragraph_index (int): The paragraph number (1 to 5).
      - thesis (str): The thesis statement.
      - book_summaries (list): List of summaries for each book.
      - comparative_analysis (str): The comparative analysis of the summaries.
    
    Returns:
      - A string containing the generated paragraph.
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
    Generates a complete book report by:
      1. Generating each of the 5 paragraphs individually.
      2. Combining them with two newlines between paragraphs.
      3. Dynamically generating a title based on the thesis statement.
      4. Prepending the title to the report.
      5. Ensuring each paragraph starts with a four-space indent.
    
    Parameters:
      - thesis (str): The thesis statement.
      - book_summaries (list): List of book summaries.
      - comparative_analysis (str): The comparative analysis.
    
    Returns:
      - A string containing the complete report with a dynamic title.
    """
    # Generate a dynamic title based on the thesis.
    title = generate_title(thesis)
    
    paragraphs = []
    for i in range(1, 6):
        print(f"Generating paragraph {i}...")
        para = generate_paragraph(i, thesis, book_summaries, comparative_analysis)
        # Add a four-space indent to the beginning of each paragraph.
        indented_para = "    " + para
        paragraphs.append(indented_para)
    # Combine the title with the paragraphs; the title is separated by two newlines from the body.
    report = title + "\n\n" + "\n\n".join(paragraphs)
    return report
