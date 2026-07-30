# Pakistan Event Venue Lead Generator

Automated lead generation for marriage halls, marquees, and event lounges across Pakistani cities.

Data is appended directly to a Google Sheet with the following columns:
Name | Address | Phone | WhatsApp | Mail Address | Contact us Form | Service to pitch | Contacted | Instructions | Follow up 1 | Follow up 1 Instructions | Follow up 2 | Follow up 2 Instructions | UPDATE | CLIENT CLOSED

## Tech Stack
- Python 3.10+
- Google Gemini API (extraction)
- SerpAPI (search)
- gspread (Google Sheets API)
- dotenv (secrets)

## Setup
1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill your API keys
6. Enable Google Sheets API and download `service_account.json` (place in root)
7. Run: `python main.py`

## Environment Variables
- `GEMINI_API_KEY` – from Google AI Studio
- `SERPAPI_API_KEY` – from SerpAPI
- `SPREADSHEET_ID` – your Google Sheet ID
- `SHEET_NAME` – sheet name (default 'Sheet1')
- `CITIES` – comma-separated list (e.g., 'Karachi,Lahore,Islamabad')