from ingestion import read_xml, read_pdf, read_epub
from text_processing import clean_text
from summarization import summarize_text, analyze_comparative
from report_generation import generate_thesis, generate_report

def process_book(file_path, file_type):
    """
    Processes a book file based on its type:
      - Reads the file.
      - Cleans the text.
      - Feeds the text for summarization.
    Returns the final summary for the book.
    """
    if file_type == "xml":
        raw_text = read_xml(file_path)
    elif file_type == "pdf":
        raw_text = read_pdf(file_path)
    elif file_type == "epub":
        raw_text = read_epub(file_path)
    else:
        raise ValueError("Unsupported file type")
    
    print("Finished reading file. Cleaning text...")
    cleaned = clean_text(raw_text)
    
    print("Summarizing entire text...")
    summary = summarize_text(cleaned)
    return summary

def main():
    # File paths ("Readings" folder in the project root)
    xml_path = "Readings/The-Bell-Jar-1645639705._vanilla.xml"
    pdf_path = "Readings/the_stranger.pdf"
    epub_path = "Readings/franz-kafka_metamorphosis.epub"

    print("Processing Metamorphosis (EPUB)...")
    metamorphosis_summary = process_book(epub_path, "epub")
    
    print("Processing The Bell Jar (XML)...")
    belljar_summary = process_book(xml_path, "xml")
    
    print("Processing The Stranger (PDF)...")
    stranger_summary = process_book(pdf_path, "pdf")
    
    # Prepare the summaries for comparative analysis.
    summaries = [belljar_summary, stranger_summary, metamorphosis_summary]
    print("Analyzing comparative themes...")
    comparative_analysis = analyze_comparative(summaries)
    
    print("Generating thesis statement...")
    thesis_statement = generate_thesis(summaries, comparative_analysis)
    print("Thesis generated:", thesis_statement)
    
    print("Generating final book report...")
    book_summaries = [belljar_summary, stranger_summary, metamorphosis_summary]
    final_report = generate_report(thesis_statement, book_summaries, comparative_analysis)
    
    # Save the final report to a file.
    with open("Final_Book_Report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("Book report generated and saved as Final_Book_Report.txt")

if __name__ == "__main__":
    main()
