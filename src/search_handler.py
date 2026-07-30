import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class SheetHandler:
    def __init__(self):
        self.column_count = len(Config.COLUMNS)
        # YOUR ACTUAL DEPLOYMENT URL
        self.webapp_url = "https://script.google.com/macros/s/AKfycby8IUK-1DQlj5wEjyUeSsV7mlYWwOyIaJdnKg7xlT9GWOi5ijb_aDnk3ETKUc_yYQAx/exec"

    def get_existing_names(self):
        """Read all existing names from the sheet via GET."""
        try:
            response = requests.get(self.webapp_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extract names from the JSON response
                names = []
                for row in data:
                    # The key might be "Name" or the first column header
                    name = row.get("Name") or list(row.values())[0] if row else ""
                    if name and name.strip():
                        names.append(name.strip())
                logger.info(f"Found {len(names)} existing venues")
                return names
            else:
                logger.error(f"GET failed: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Failed to read sheet: {e}")
            return []

    def append_row(self, row_data):
        """Append a row via POST."""
        try:
            response = requests.post(
                self.webapp_url,
                json=row_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info("Row appended successfully")
                    return True
                else:
                    logger.error(f"Append failed: {result}")
                    return False
            else:
                logger.error(f"POST failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Append error: {e}")
            return False