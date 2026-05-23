import re
from datetime import datetime
from typing import Optional
from models import Invoice
from date_normalizer import extract_invoice_date


REGEX_PATTERNS: dict[str, list[str]] = {
    "invoice_id": [r"(?i)(?:Invoic(?:e)?|Inv|Bill|ID)\b.*?[:\s#]+(?!(?:No|Number|ID|Num)\b)([A-Z0-9\-\./]+)"],
    "vendor_name": [r"(?m)^((?:(?!\bInvoice\b|\bBill\b|\bBill To\b|\bTo\b|\bInv\b).)+)$"],
    "subtotal": [r"(?i)Sub\s?total[:\s]*\$?\s*([\d,]+\.\d{1,2})"],
    "tax_amount": [r"(?i)(?:Tax|VAT|GST|Sales\sTax)[:\s]*\$?\s*([\d,]+\.\d{1,2})"],
    "total_amount": [r"(?i)\b(?:Total(?:\sAmount)?|Balance(?:\sDue)?|Amount\sDue|Net\sAmount)[:\s]*\$?\s*([\d,]+\.\d{1,2})"]
}

def extract_invoice(raw_pdf: str) -> Invoice:
    # Extract date using your normalizer
    date_str = extract_invoice_date(raw_pdf)
    print(date_str)
    date_obj = None
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            date_obj = None
    
    # Extract other fields
    invoice_id = "Not Found"
    vendor_name = "Unknown"
    subtotal = 0.0
    tax_amount = 0.0
    total_amount = 0.0
    
    # Extract invoice_id
    for pattern in REGEX_PATTERNS["invoice_id"]:
        match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
        if match:
            invoice_id = match.group(1).strip()
            break
    
    # Extract vendor_name
    for pattern in REGEX_PATTERNS["vendor_name"]:
        match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
        if match:
            vendor_name = match.group(1).strip()
            break
    
    # Extract subtotal
    for pattern in REGEX_PATTERNS["subtotal"]:
        match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
        if match:
            val = re.sub(r'[^\d.]', '', match.group(1).strip())
            if val and val != '.':
                subtotal = float(val)
            break
    
    # Extract tax_amount
    for pattern in REGEX_PATTERNS["tax_amount"]:
        match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
        if match:
            val = re.sub(r'[^\d.]', '', match.group(1).strip())
            if val and val != '.':
                tax_amount = float(val)
            break
    
    # Extract total_amount
    for pattern in REGEX_PATTERNS["total_amount"]:
        match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
        if match:
            val = re.sub(r'[^\d.]', '', match.group(1).strip())
            if val and val != '.':
                total_amount = float(val)
            break
    
    # Create Invoice object (Pydantic will handle validation)
    return Invoice(
        invoice_id=invoice_id,
        vendor_name=vendor_name,
        date=date_obj,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount
    )
# import re
# from models import Invoice

# REGEX_PATTERNS: dict[str, list[str]] = {
#     # Fix: Captures the ID only if it's NOT a common label word like 'No', 'ID', or 'Number'
#     "invoice_id": [r"(?i)(?:Invoic(?:e)?|Inv|Bill|ID)\b.*?[:\s#]+(?!(?:No|Number|ID|Num)\b)([A-Z0-9\-\./]+)"],
    
#     "vendor_name": [r"(?m)^((?:(?!\bInvoice\b|\bBill\b|\bTo\b|\bInv\b).)+)$"],
#     "date": [r"(?i)(?:Date)[:\s]+(\d{1,4}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})"],
#     "subtotal": [r"(?i)Sub\s?total[:\s]*\$?\s*([\d,]+\.\d{1,2})"],
#     "tax_amount": [r"(?i)(?:Tax|VAT|GST|Sales\sTax)[:\s]*\$?\s*([\d,]+\.\d{1,2})"],
#     "total_amount": [r"(?i)\b(?:Total(?:\sAmount)?|Balance(?:\sDue)?|Amount\sDue|Net\sAmount)[:\s]*\$?\s*([\d,]+\.\d{1,2})"]
# }
   

# def extract_invoice(raw_pdf: str) -> Invoice:
#     extracted_data = {}
#     for field, patterns in REGEX_PATTERNS.items():
#         found_value = None
#         for pattern in patterns:
#             match = re.search(pattern, raw_pdf, re.IGNORECASE | re.MULTILINE)
#             if match:
#                 found_value = match.group(1).strip()
#                 if field in ["subtotal", "tax_amount", "total_amount"]:
#                     found_value = re.sub(r'[^\d.]', '', found_value)
#                 break 
        
#         # FIX: Ensure we never pass None to Pydantic
#         if found_value is None:
#             if field in ["subtotal", "tax_amount", "total_amount"]:
#                 extracted_data[field] = 0.0
#             else:
#                 extracted_data[field] = "Not Found"
#         else:
#             extracted_data[field] = found_value

#     return Invoice(**extracted_data)

