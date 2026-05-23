import ollama
from dotenv import load_dotenv
import os
import json
from models import Invoice
from tracking import tracker

# Load environment variables (though Ollama doesn't need an API key)
load_dotenv()

# Updated Model Name
LLM_MODEL = "gemma4:e2b" 

SYSTEM_INSTRUCTIONS = """
You are a highly accurate Document Data Extraction Specialist. 

Your task is to extract structured information from the provided raw text of an invoice. 
1. Always identify the 'Seller' as the party providing the service/product and the 'Buyer' as the party being billed.
2. If a value (like tax_id or email) is not explicitly present in the text, return null (None).
3. Ensure dates are interpreted correctly. If the format is ambiguous, prefer the most logical business date.
4. Return the data strictly following the provided JSON schema.
5. Do not include any conversational text, or explanations in your output.
"""

def process_invoice_using_llm(raw_pdf: str):
    # Get the schema string to inject into the prompt
    schema_string = json.dumps(Invoice.model_json_schema(), indent=2)
    raw_pdf = raw_pdf.strip()
    clean_text = " ".join(raw_pdf.split())

    PROMPT = f"""
Identify the parties and totals from this invoice text.
- Seller: The party issuing the bill (getting paid).
- Buyer: The party being billed (paying).
- If the text is messy, prioritize the 'Bill To' section for the Buyer.
- If no due date is mentioned, scan the invoice document for anything referring to a due date. If
found, use it as the due date, else do not mention due date.

Return the data according to this JSON Schema:
{schema_string}

TEXT:
{clean_text}
"""

    try:
        # Calling Ollama instead of Gemini
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {'role': 'system', 'content': SYSTEM_INSTRUCTIONS},
                {'role': 'user', 'content': PROMPT},
            ],
            format='json' # Forces the local model to output valid JSON
        )

        # Extracting the content string from the Ollama response object
        content = response['message']['content']
        
        # Validate using your Pydantic model
        processed_invoice = Invoice.model_validate_json(content)
        
        tracker.processed.append(raw_pdf)
        print(content)
        return processed_invoice

    except Exception as e:
        tracker.processing_failed.append(raw_pdf)
        print(f"Ollama Failed to process invoice. Error: {e}")
        return None
                