import pdfplumber
from pathlib import Path
from tracking import tracker
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def is_valid_pdf(file_path: Path) -> bool:
    """Checks if the PDF is readable and has at least one page."""
    try:
        # pypdf opens and closes the file internally
        reader = PdfReader(file_path, strict=True)
        return len(reader.pages) > 0
    except (PdfReadError, Exception):
        # Tracking the full Path object for consistency
        tracker.parsing_failed.append(file_path)
        return False

def scan_directory_for_pdfs(folder_path: Path):
    """Scans folder for .pdf files and logs them to the tracker."""
    if folder_path.exists() and folder_path.is_dir():
        for file_path in folder_path.iterdir():
            # .lower() ensures we catch .PDF, .Pdf, and .pdf
            if file_path.suffix.lower() == ".pdf":
                tracker.scanned.append(file_path)
            else:
                print(f"Skipping non-pdf: {file_path.name}")
    else:
        print(f"Error: The folder '{folder_path}' does not exist.")
    
    return tracker.scanned

def parse_pdf(file_path: Path) -> str | None:
    """Validates and extracts raw text from a PDF."""
    try:    
        # Step 1: Validation
        if not is_valid_pdf(file_path):
            return None
        
        # Step 2: Extraction
        # pdfplumber handles opening/closing via context manager
        with pdfplumber.open(file_path) as pdf:
            # layout=True preserves the visual structure of the invoice
            raw_text = "\n".join([page.extract_text(layout=True) or "" for page in pdf.pages])
        
        tracker.parsed.append(file_path)
        return raw_text
    
    except Exception as e:
        print(f"Error extracting text from {file_path.name}: {e}")
        return None

    
