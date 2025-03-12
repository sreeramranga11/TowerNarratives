from ingestion import read_xml, read_pdf, read_epub
from text_processing import clean_text
from summarization import summarize_text, analyze_comparative
from report_generation import generate_thesis, generate_report

def process_book(file_path, file_type):
    """
    Process a book by:
      1. Reading the file content based on its file type (XML, PDF, or EPUB).
      2. Cleaning the extracted text to remove extra whitespace and irrelevant characters.
      3. Summarizing the cleaned text using the OpenAI API, ensuring that the summary includes direct citations.
    
    Parameters:
      - file_path: The path to the book file.
      - file_type: The type of the file ('xml', 'pdf', or 'epub').

    Returns:
      - A summary of the book that focuses on the theme of social isolation.
    """
    # Read the book file according to its type.
    if file_type == "xml":
        raw_text = read_xml(file_path)
    elif file_type == "pdf":
        raw_text = read_pdf(file_path)
    elif file_type == "epub":
        raw_text = read_epub(file_path)
    else:
        # Raise an error if the file type is not supported.
        raise ValueError("Unsupported file type")
    
    print("Finished reading file. Cleaning text...")
    # Clean the raw text to standardize spacing and remove unnecessary characters.
    cleaned = clean_text(raw_text)
    
    print("Summarizing entire text...")
    # Use the OpenAI API to generate a summary for the cleaned text.
    summary = summarize_text(cleaned)
    return summary

def main():
    """
    Main function to execute the entire workflow:
      1. Define file paths for the three novels located in the "Readings" folder.
      2. Process each book to produce summaries.
      3. Analyze the summaries comparatively to extract thematic differences/similarities.
      4. Generate a thesis statement based on the summaries and comparative analysis.
      5. Generate a complete five-paragraph book report (with citations) using the thesis, summaries, and analysis.
      6. Save the final report to a text file.
    """
    # Define file paths for the three books.
    xml_path = "Readings/The-Bell-Jar-1645639705._vanilla.xml"
    pdf_path = "Readings/the_stranger.pdf"
    epub_path = "Readings/franz-kafka_metamorphosis.epub"

    # Process each book and obtain a summary for each.
    print("Processing Metamorphosis (EPUB)...")
    metamorphosis_summary = process_book(epub_path, "epub")
    
    print("Processing The Bell Jar (XML)...")
    belljar_summary = process_book(xml_path, "xml")
    
    print("Processing The Stranger (PDF)...")
    stranger_summary = process_book(pdf_path, "pdf")
    
    # Combine the individual book summaries into a list for comparative analysis.
    summaries = [belljar_summary, stranger_summary, metamorphosis_summary]
    print("Analyzing comparative themes...")
    # Analyze the summaries to identify how each novel addresses social isolation.
    comparative_analysis = analyze_comparative(summaries)
    
    # Generate a thesis statement using the summaries and the comparative analysis.
    print("Generating thesis statement...")
    thesis_statement = generate_thesis(summaries, comparative_analysis)
    print("Thesis generated:", thesis_statement)
    
    # Generate the final five-paragraph book report.
    print("Generating final book report...")
    # The final report will incorporate the thesis, individual book summaries, and comparative analysis.
    book_summaries = [belljar_summary, stranger_summary, metamorphosis_summary]
    final_report = generate_report(thesis_statement, book_summaries, comparative_analysis)
    
    # Save the final report as a text file.
    with open("Final_Book_Report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("Book report generated and saved as Final_Book_Report.txt")

if __name__ == "__main__":
    # Run the main function if this script is executed directly.
    main()
