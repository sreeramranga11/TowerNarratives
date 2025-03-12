# TowerNarratives
Tower Narratives is an automated pipeline that generates a comprehensive literary analysis report on the theme of social isolation. The system ingests multiple book files, processes them with a language model, and produces a cohesive five-paragraph report complete with citations from the texts.

## Features
Multi-format Ingestion: Supports TXT, PDF, and other common formats.
Preprocessing & Chunking: Splits large texts into manageable chunks to accommodate LLM context limits.
Thematic Analysis: Uses language models to extract key passages on social isolation.
Automated Report Generation: Produces a structured report featuring a thesis, arguments, and conclusion.

## Project Structure
ingest.py: Loads and parses text from various file types.
chunker.py: Breaks texts into chunks that fit model context sizes.
analysis.py: Analyzes text chunks to extract insights on social isolation.
report_generator.py: Synthesizes analyses into a five-paragraph report.
main.py: Orchestrates the entire pipeline.

## Requirements
Python 3.7 or higher
Required libraries: PyPDF2 (for PDF processing), plus any necessary LLM API client libraries (e.g., OpenAI's API)

## Usage
Prepare the Files: Place your book files in the designated directory.
Run the Pipeline: Execute python main.py to start the ingestion, analysis, and report generation process.
Review the Report: The final book report will be generated in the output directory.
