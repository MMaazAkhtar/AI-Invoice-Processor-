from date_normalizer import extract_invoice_date

text = "Apr 20, 2026"
date = extract_invoice_date(text)
print(date)