import os
import shutil
from pathlib import Path

class InvoiceFileManager:
    def __init__(self, base_dir: str):
        self.drop_folder = Path(base_dir) / "Invoices"
        
        # We only keep two target subfolders now
        self.processed_folder = self.drop_folder / "processed"
        self.review_folder = self.drop_folder / "human_review"

        # Automatically create the structure
        for folder in [self.drop_folder, self.processed_folder, self.review_folder]:
            folder.mkdir(parents=True, exist_ok=True)

    def should_process(self, file_path: Path) -> bool:
        """
        Checks if file was already handled. 
        If yes, attempts lazy deletion of the leftover file in the drop folder.
        """
        if file_path.is_dir():
            return False

        # Check if this file already exists in either output folder
        for folder in [self.processed_folder, self.review_folder]:
            if (folder / file_path.name).exists():
                try:
                    os.remove(file_path)
                    print(f"🗑️  Cleaned up duplicate leftover: {file_path.name}")
                except PermissionError:
                    print(f"⏩ Skipping {file_path.name} (already in {folder.name}, but file is open)")
                return True  # It's already been dealt with; skip processing
        
        return False  # Brand new file, continue processing

    def finalize(self, file_path: Path, status: str):
        """Moves file to processed or human_review."""
        target = self.processed_folder if status == "success" else self.review_folder

        try:
            # 1. Copy first (Safe if open)
            shutil.copy2(file_path, target / file_path.name)
            # 2. Attempt Delete
            try:
                os.remove(file_path)
            except PermissionError:
                print(f"ℹ️  Saved to {target.name}, but original remains in drop folder (file open).")
        except Exception as e:
            print(f"❌ Error moving file to {target.name}: {e}")