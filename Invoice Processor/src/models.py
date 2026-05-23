import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Party(BaseModel):
    """Represents a business entity on the invoice. 
    Only name is required for Vendor validation."""
    name: str = Field(..., description="The legal name of the entity")
    address: Optional[str] = Field(None, description="The full physical or billing address")
    tax_id: Optional[str] = Field(None, description="VAT ID, EIN, or Tax Registration Number")
    email: Optional[str] = Field(None, description="The email address of the entity")
    phone: Optional[str] = Field(None, description="The phone number of the entity")
    PO_number: Optional[str] = Field(None, description="The purchase order number associated with this party")

class InvoiceItem(BaseModel):
    """Line items are kept completely optional to prevent extraction failure 
    if the invoice table format is highly non-standard."""
    description: Optional[str] = Field(None, description="Description of the item or service")
    quantity: Optional[float] = Field(None, description="Quantity billed")
    unit_price: Optional[float] = Field(None, description="Price per single unit")
    amount: Optional[float] = Field(None, description="Total calculated amount for this line item")

class Invoice(BaseModel):
    # Core Fields Required for Google Sheets Write
    seller: Party = Field(..., description="The entity providing the goods/services (Vendor). MUST extract name.")
    buyer: Party = Field(..., description="The entity receiving/paying the invoice (Client/Customer)")
    invoice_id: str = Field(..., description="The unique invoice number or identifier string")
    issue_date: datetime.date = Field(..., description="The date the invoice was issued/created")
    
    subtotal: float = Field(..., description="The cumulative cost before taxes and discounts are applied")
    tax_amount: float = Field(..., description="The calculated tax amount charged on the invoice")
    total_amount: float = Field(..., description="The absolute final total balance due")

    # Optional Fields (Nice-to-have data that won't break the script if missing)
    due_date: Optional[datetime.date] = Field(None, description="The date by which payment must be received")
    currency: Optional[str] = Field("USD", description="The 3-letter ISO currency code (e.g., USD, EUR, PKR)")
    line_items: Optional[List[InvoiceItem]] = Field(default_factory=list, description="List of granular line items parsed from the table")


# class Invoice(BaseModel):
#     invoice_id: str = Field(..., min_length=1)
#     seller: str = "Unknown"
#     buyer: str = "Unknown"
#     date: Optional[datetime.date] = None  
#     subtotal: Optional[float] = None
#     tax_amount: Optional[float] = None
#     total_amount: Optional[float] = None


