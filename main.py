import logging
from src.sheet_handler import SheetHandler
from src.search_handler import SearchHandler
from src.ai_handler import AIHandler
from src.utils import clean_text, is_duplicate
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Pakistan Event Venue Lead Generator")

    # Initialize handlers
    sheet = SheetHandler()
    search = SearchHandler()
    ai = AIHandler()

    # Get existing names to avoid duplicates
    existing_names = sheet.get_existing_names()

    for city in Config.CITIES:
        logger.info(f"Processing city: {city}")
        for venue_type in Config.VENUE_TYPES:
            query = f"{venue_type} in {city} Pakistan"
            logger.info(f"Searching: {query}")

            # Get URLs from search (using SerpAPI or fallback)
            urls = search.get_venue_urls(query, num_results=10)

            for url in urls:
                logger.info(f"Scraping: {url}")
                raw_html = search.fetch_html(url)
                if not raw_html:
                    continue

                # Extract structured data using Gemini
                extracted = ai.extract_venue_data(raw_html, city)

                if not extracted or not extracted.get("Name"):
                    logger.warning(f"No name extracted from {url}")
                    continue

                # Check duplicate
                if is_duplicate(extracted["Name"], existing_names):
                    logger.info(f"Skipping duplicate: {extracted['Name']}")
                    continue

                # Build row (15 columns)
                row = [
                    extracted.get("Name", ""),
                    extracted.get("Address", ""),
                    extracted.get("Phone", ""),
                    extracted.get("WhatsApp", ""),
                    extracted.get("Email", ""),
                    extracted.get("ContactForm", ""),
                    "Marriage Hall / Marquee",  # Service to pitch (default)
                    "FALSE",                    # Contacted
                    "",                         # Instructions
                    "",                         # Follow up 1
                    "",                         # Follow up 1 Instructions
                    "",                         # Follow up 2
                    "",                         # Follow up 2 Instructions
                    "=TODAY()",                 # UPDATE (auto date)
                    "FALSE"                     # CLIENT CLOSED
                ]

                # Append to sheet
                sheet.append_row(row)
                existing_names.append(extracted["Name"])
                logger.info(f"Added: {extracted['Name']}")

    logger.info("All cities processed successfully!")

if __name__ == "__main__":
    main()