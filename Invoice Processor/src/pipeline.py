from file_manager import InvoiceFileManager
from pdf_utils import parse_pdf
from llm_extraction import process_invoice_using_llm
from sheets import GoogleSheetsAdapter

def directory_to_sheets_invoices_pipeline(fm: InvoiceFileManager):
    # Scan the main drop folder
    pdf_paths = list(fm.drop_folder.glob("*.pdf"))
    
    for pdf_path in pdf_paths:
        # HYBRID CHECK: If it returns True, it means it's a duplicate and was skipped
        if fm.should_process(pdf_path):
            continue

        try:
            # 1. Extraction
            extracted_raw_text = parse_pdf(pdf_path)
            if not extracted_raw_text:
                print(f"⚠️  Could not read text from {pdf_path.name}. Sending to human review.")
                fm.finalize(pdf_path, "review")
                continue

            processed_invoice = process_invoice_using_llm(extracted_raw_text)

            # 2. Validation (Check for nulls or anomalies)
            is_incomplete = (
                not processed_invoice or
                not processed_invoice.invoice_id or 
                processed_invoice.total_amount <= 0
            )

            if is_incomplete:
                print(f"⚠️  Missing/Null fields detected in {pdf_path.name}. Sending to human review.")
                fm.finalize(pdf_path, "review")
                continue

            # 3. Success Path
            sheets = GoogleSheetsAdapter(json_keyfile="credentials.json", sheet_name="Invoice_Processor")
            sheets.write_to_sheets(processed_invoice, pdf_path)
            fm.finalize(pdf_path, "success")

        except Exception as e:
            # Catch crashes or network timeouts and drop them into review too
            print(f"💥 Code Exception on {pdf_path.name}: {e}. Routing to human review.")
            fm.finalize(pdf_path, "review")