from dataclasses import dataclass, field
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

FOLDER_PATH = os.getenv("FOLDER_PATH")
if FOLDER_PATH:
    FOLDER_PATH = Path(FOLDER_PATH)

@dataclass
class PDFTracker:
    folder_path: Path
    scanned: list = field(default_factory=list)
    parsed: list = field(default_factory=list)
    parsing_failed: list = field(default_factory=list)
    processed: list = field(default_factory=list)
    processing_failed: list = field(default_factory=list)
    written_to_sheets: list = field(default_factory=list)
    writing_failed: list = field(default_factory=list)

    def get_summary(self) -> dict:
        return {
            "Scanned": self.scanned,
            "Parsed": self.parsed,
            "Parsing Failed": self.parsing_failed,
            "Processed": self.processed,
            "Processing Failed": self.processing_failed,
            "Written to Sheets": self.written_to_sheets,
            "Writing Failed": self.writing_failed
        }
    
tracker = PDFTracker(folder_path=FOLDER_PATH)