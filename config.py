import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
    CITIES = [c.strip() for c in os.getenv("CITIES", "").split(",") if c.strip()]

    # Columns mapping (A1:O1)
    COLUMNS = [
        "Name", "Address", "Phone", "whatsapp", "Mail Address",
        "Contact us Form", "Service to pitch", "Contacted",
        "Instructions", "Follow up 1", "Follow up 1 Instructions",
        "Follow up 2", "Follow up 2 Instructions", "UPDATE", "CLIENT CLOSED"
    ]

    # Service types to search
    VENUE_TYPES = ["marriage hall", "marquee", "event lounge"]