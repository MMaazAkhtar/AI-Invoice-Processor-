from pathlib import Path
import pdfplumber


def is_valid_pdf(file_path: Path) -> bool:
    """Basic validation for PDF existence and extension."""
    return file_path.exists() and file_path.is_file() and file_path.suffix.lower() == ".pdf"


def parse_pdf(file_path: Path) -> str | None:
    """Validates and extracts raw text from a PDF."""

    try:
        # Step 1: Validation
        if not is_valid_pdf(file_path):
            return None

        # Step 2: Extraction
        with pdfplumber.open(file_path) as pdf:
            pages_text = []

            for page in pdf.pages:
                text = page.extract_text(layout=True)
                if text:
                    pages_text.append(text)

        raw_text = "\n".join(pages_text)

        # Step 3: Cleanup
        clean_text = " ".join(raw_text.split())

        return clean_text if clean_text else None

    except Exception as e:
        print(f"Error extracting text from {file_path.name}: {e}")
        return None
    
print(parse_pdf(Path(r"D:\Invoice Processor\Invoices\human_review\invoice 3.pdf")))