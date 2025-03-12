# TowerNarratives
TowerNarratives is an automated system for generating detailed book reports based on three novels. The system ingests texts from various file formats (XML, PDF, EPUB), uses the OpenAI API to summarize and analyze the texts with an emphasis on social isolation, and finally produces a five-paragraph report. The report includes a dynamic title, thesis, and direct citations from the texts, and is exported as a DOCX file.

## Input:
- Three novels in XML, PDF, and EPUB formats (located in the Readings folder).

## Processing Steps:
1. Ingestion:
    - Custom modules extract text from XML, PDF, and EPUB files.
2. Cleaning:
    - Normalize and clean the extracted text using regular expressions.
3. Summarization:
    - Each book's text is summarized via the OpenAI API. Summaries include direct citations (exact quotes) to support analysis.
4. Comparative Analysis:
    - The summaries are compared to extract thematic insights regarding social isolation.
5. Thesis & Title Generation:
    - A thesis statement is generated from the comparative analysis, and a dynamic, creative title is produced based on the thesis.
6. Report Generation:
    - A structured, five-paragraph report is generated with:
        - Paragraph 1: Introduction with thesis.
        - Paragraph 2: Analysis of the first novel.
        - Paragraph 3: Analysis of the second novel.
        - Paragraph 4: Analysis of the third novel.
        - Paragraph 5: A concluding paragraph with a rebuttal and summary. Each paragraph starts with a four-space indent.

## Output:
- The final report is exported as a DOCX file.

## Requirements
The project depends on the following Python packages:

- openai
- PyPDF2
- ebooklib
- beautifulsoup4
- nltk
- python-dotenv
- fpdf2
- unidecode
- python-docx

Install them using:
```pip install -r requirements.txt```

You also need to have a .env file with your OpenAI key in this format:
```OPENAI_API_KEY=sk-...```
