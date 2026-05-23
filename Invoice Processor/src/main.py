from file_manager import InvoiceFileManager
from pipeline import directory_to_sheets_invoices_pipeline

BASE_DIR = r"D:\Invoice Processor"

def main():
    # This will now look inside D:\Invoice Processor\Invoices
    fm = InvoiceFileManager(BASE_DIR)
    directory_to_sheets_invoices_pipeline(fm)

if __name__ == "__main__":
    main()
# from pathlib import Path
# from tracking import tracker
# from pipeline import directory_to_sheets_invoices_pipeline


# FOLDER_PATH = Path(r"D:\Invoice Processor\invoices")
# def main():
#     directory_to_sheets_invoices_pipeline(Path(tracker.folder_path))
#     print(tracker.get_summary())

# if __name__ == "__main__":
#     main()

