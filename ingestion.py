import xml.etree.ElementTree as ET
import PyPDF2
from ebooklib import epub
from bs4 import BeautifulSoup
import signal
import warnings

# Define a common TimeoutException
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out.")

def extract_text_with_timeout(page, timeout_seconds=10):
    """
    Extracts text from a PDF page with a timeout.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        text = page.extract_text()
    finally:
        signal.alarm(0)  # Disable the alarm
    return text

def read_pdf(file_path):
    """
    Reads a PDF file and extracts text from all pages.
    """
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        for i, page in enumerate(reader.pages, start=1):
            # print(f"Processing page {i}/{total_pages}")
            try:
                page_text = extract_text_with_timeout(page, timeout_seconds=10)
            except TimeoutException:
                print(f"Timeout processing page {i}, skipping this page.")
                continue
            except Exception as e:
                print(f"Error processing page {i}: {e}")
                continue
            if page_text:
                text += page_text + "\n"
    print("Finished processing all PDF pages.")
    return text

def extract_epub_item_content(item, timeout_seconds=10):
    """
    Extracts content from an EPUB item with a timeout.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        content = item.get_content()
    finally:
        signal.alarm(0)  # Disable the alarm
    return content

def read_epub(file_path):
    """
    Reads an EPUB file and extracts text from all document items.
    """
    # Suppress warnings from ebooklib if desired.
    warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")
    warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib.epub")
    
    book = epub.read_epub(file_path)
    text = ""
    items = list(book.get_items())
    total_items = len(items)
    for i, item in enumerate(items, start=1):
        # print(f"Processing EPUB item {i}/{total_items}: {item.get_name()}")
        # Check if the item is a document: either its type is XHTML or it's an instance of EpubHtml.
        if item.get_type() == 'application/xhtml+xml' or isinstance(item, epub.EpubHtml):
            try:
                content = extract_epub_item_content(item, timeout_seconds=10)
                soup = BeautifulSoup(content, "html.parser")
                text += soup.get_text(separator="\n") + "\n"
            except TimeoutException:
                print(f"Timeout processing item {i}, skipping this item.")
                continue
            except Exception as e:
                print(f"Error processing item {i}: {e}")
                continue
    print("Finished processing all EPUB items.")
    return text

def read_xml(file_path):
    """
    Reads an XML file and extracts text from all 'content:encoded' elements.
    If none are found, falls back to gathering text from all elements.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    texts = []
    for elem in root.iter():
        if "content:encoded" in elem.tag and elem.text:
            texts.append(elem.text)
    if not texts:
        # Fallback: collect all text nodes from the XML tree.
        for elem in root.iter():
            if elem.text:
                texts.append(elem.text)
    return "\n".join(texts)
