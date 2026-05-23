# test_complete.py
from extractor import extract_invoice
from date_normalizer import extract_invoice_date

test_cases = [
    # 1. Standard Professional
    """ACME CORP
    Inv. No.: ABC/2024/99
    Date: 01-01-2024
    Total: $150.00""",

    # 2. With Subtotal and Tax
    """GLOBAL SERVICES
    Invoice #101
    Subtotal: $500.00
    Tax: $50.00
    Date: 12 Apr 2023
    Total Amount: $550.00""",

    # 3. European format
    """TECH SOLUTIONS
    Invoice ID: 2024-X-900
    Date: 12.04.2024
    Total: 1,200.50""",

    # 4. Messy OCR
    """   COFFEE   SUPPLY   
    Invoic # :    777888   
    Date : 2024 - 01 - 15
    Net Amount : $ 15.75""",

    # 5. No label
    """PAPER COMPANY
    Invoice 44592
    Date: April 10, 2024
    Total: $42.10""",
]

print("=" * 70)
print("COMPLETE INVOICE EXTRACTOR TEST (WITH DATE NORMALIZER)")
print("=" * 70)
print()

for i, text in enumerate(test_cases, 1):
    print(f"Test {i}:")
    print("-" * 40)
    
    # First, test date extraction separately
    date_result = extract_invoice_date(text)
    print(f"Date normalizer output: {date_result}")
    
    # Then test full extraction
    try:
        inv = extract_invoice(text)
        print(f"✅ EXTRACTION SUCCESSFUL")
        print(f"   Invoice ID: {inv.invoice_id}")
        print(f"   Vendor: {inv.vendor_name}")
        print(f"   Date: {inv.date}")
        print(f"   Subtotal: {inv.subtotal}")
        print(f"   Tax: {inv.tax_amount}")
        print(f"   Total: {inv.total_amount}")
    except Exception as e:
        print(f"❌ EXTRACTION FAILED: {e}")
    
    print()