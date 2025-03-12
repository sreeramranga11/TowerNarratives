import xml.etree.ElementTree as ET
import PyPDF2
from ebooklib import epub
from bs4 import BeautifulSoup
import signal
import warnings

# Define a custom exception for timeout situations.
class TimeoutException(Exception):
    pass

# This function acts as a signal handler to raise a TimeoutException
def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out.")

def extract_text_with_timeout(page, timeout_seconds=10):
    """
    Extracts text from a single PDF page with a specified timeout.
    
    Parameters:
      - page: A PDF page object from which to extract text.
      - timeout_seconds: The maximum number of seconds to allow for text extraction.
    
    Returns:
      - The extracted text as a string.
    
    Mechanism:
      - Sets an alarm signal to enforce a timeout.
      - Attempts to extract text using the page's extract_text() method.
      - Disables the alarm regardless of success or failure.
    """
    # Register our timeout handler for the SIGALRM signal.
    signal.signal(signal.SIGALRM, timeout_handler)
    # Set an alarm to go off after 'timeout_seconds'.
    signal.alarm(timeout_seconds)
    try:
        # Attempt to extract text from the given PDF page.
        text = page.extract_text()
    finally:
        # Disable the alarm so it does not affect subsequent operations.
        signal.alarm(0)
    return text

def read_pdf(file_path):
    """
    Reads a PDF file and extracts text from each of its pages.
    
    Parameters:
      - file_path: The path to the PDF file.
    
    Returns:
      - A single string containing the concatenated text of all pages.
    
    Process:
      - Opens the file in binary mode.
      - Uses PyPDF2 to read the PDF.
      - Iterates through each page and extracts text using extract_text_with_timeout.
      - Handles timeouts and other errors gracefully, skipping problematic pages.
    """
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        for i, page in enumerate(reader.pages, start=1):
            # For each page, attempt text extraction with a timeout.
            try:
                page_text = extract_text_with_timeout(page, timeout_seconds=10)
            except TimeoutException:
                print(f"Timeout processing page {i}, skipping this page.")
                continue  # Skip this page if timeout occurs.
            except Exception as e:
                print(f"Error processing page {i}: {e}")
                continue  # Skip page if any other error occurs.
            if page_text:
                # Append the extracted text and add a newline for separation.
                text += page_text + "\n"
    print("Finished processing all PDF pages.")
    return text

def extract_epub_item_content(item, timeout_seconds=10):
    """
    Extracts the content from an EPUB item with a timeout.
    
    Parameters:
      - item: An EPUB item object.
      - timeout_seconds: Maximum allowed time for extraction.
    
    Returns:
      - The content of the EPUB item as a byte string.
    
    Process:
      - Sets an alarm for the timeout.
      - Calls the get_content() method on the item.
      - Disables the alarm afterward.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        content = item.get_content()
    finally:
        signal.alarm(0)
    return content

def read_epub(file_path):
    """
    Reads an EPUB file and extracts text from its document items.
    
    Parameters:
      - file_path: The path to the EPUB file.
    
    Returns:
      - A single string containing the concatenated text extracted from the EPUB.
    
    Process:
      - Suppresses warnings from ebooklib for a cleaner output.
      - Opens and reads the EPUB using ebooklib.
      - Iterates over each item in the EPUB.
      - Checks if the item is a document (i.e., XHTML content or an instance of epub.EpubHtml).
      - Extracts the content, parses it with BeautifulSoup, and appends the text.
      - Handles timeouts and errors gracefully.
    """
    # Suppress warnings related to EPUB processing.
    warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")
    warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib.epub")
    
    # Read the EPUB book.
    book = epub.read_epub(file_path)
    text = ""
    items = list(book.get_items())
    total_items = len(items)
    for i, item in enumerate(items, start=1):
        # Check if the item is likely to be a document.
        if item.get_type() == 'application/xhtml+xml' or isinstance(item, epub.EpubHtml):
            try:
                # Extract the raw content from the item.
                content = extract_epub_item_content(item, timeout_seconds=10)
                # Parse the content with BeautifulSoup to extract text while preserving some structure.
                soup = BeautifulSoup(content, "html.parser")
                # Get text with newline separators and append to overall text.
                text += soup.get_text(separator="\n") + "\n"
            except TimeoutException:
                print(f"Timeout processing item {i}, skipping this item.")
                continue  # Skip items that time out.
            except Exception as e:
                print(f"Error processing item {i}: {e}")
                continue  # Skip items with other errors.
    print("Finished processing all EPUB items.")
    return text

def read_xml(file_path):
    """
    Reads an XML file and extracts text content.
    
    Parameters:
      - file_path: The path to the XML file.
    
    Returns:
      - A string containing concatenated text extracted from the XML.
    
    Process:
      - Parses the XML using ElementTree.
      - Iterates through all elements to find those with tags containing 'content:encoded'.
      - If no such elements are found, falls back to collecting text from all elements.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    texts = []
    # Try to extract text from elements with 'content:encoded' in their tag.
    for elem in root.iter():
        if "content:encoded" in elem.tag and elem.text:
            texts.append(elem.text)
    if not texts:
        # Fallback: If no 'content:encoded' elements, extract text from every element.
        for elem in root.iter():
            if elem.text:
                texts.append(elem.text)
    # Join all collected text snippets into a single string separated by newlines.
    return "\n".join(texts)
