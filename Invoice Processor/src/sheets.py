import gspread
from models import Invoice
from tracking import tracker
from pathlib import Path

class GoogleSheetsAdapter:
    def __init__(self, json_keyfile: str, sheet_name: str):
        self.gc = gspread.service_account(filename=json_keyfile)
        # Opens the sheet by name and selects the first worksheet
        self.sheet = self.gc.open(sheet_name).sheet1

    def write_to_sheets(self, invoice: Invoice, file_path: Path):
        """Maps the Pydantic model to a list and appends it."""
        try:
            # model_dump() converts the Pydantic model into a nested dictionary
            data = invoice.model_dump()
        
            # Accessing nested 'seller' dictionary to get the 'name'
            # Accessing 'issue_date' instead of 'date'
            row = [
                data['invoice_id'],
                data['seller']['name'],      # Corrected from 'vendor_name'
                data['buyer']['name'],      # Corrected from 'vendor_name'
                str(data['issue_date']),     # Corrected from 'date'
                str(data['due_date']) if data['due_date'] else None,
                data['subtotal'],
                data['tax_amount'],
                data['total_amount'],
            ]
        
            # Append the row to the bottom of the sheet
            self.sheet.append_row(row)
            tracker.written_to_sheets.append(file_path)
            
        except Exception as e:
            print(f"Error writing to Google Sheets: {e}")
            # Ensure 'tracker' is the instance imported from your tracking file
            tracker.writing_failed.append(file_path)

    # def write_to_sheets(self, invoice: Invoice, file_path: Path):
    #     """Maps the Pydantic model to a list and appends it."""
    #     try:
    #         data = invoice.model_dump()
        
    #     # Prepare the row as a list (ensure this order matches your Sheet headers!)
    #         row = [
    #             data['invoice_id'],
    #             data['vendor_name'],
    #             str(data['date']),
    #             data['subtotal'],
    #             data['tax_amount'],
    #             data['total_amount']
    #         ]
        
    #         # Append the row to the bottom of the sheet
    #         self.sheet.append_row(row)
    #         tracker.written_to_sheets.append(file_path)
    #     except Exception as e:
    #         print(f"Error writing to Google Sheets: {e}")
    #         tracker.writing_failed.append(file_path)

