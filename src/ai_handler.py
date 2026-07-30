import google.generativeai as genai
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class AIHandler:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")

    def extract_venue_data(self, html_content, city):
        """Use Gemini to extract structured venue data from raw HTML."""
        prompt = f"""
        You are an expert data extractor. Extract the following fields from the HTML of a venue website.
        Return ONLY a valid JSON object with exactly these keys: Name, Address, Phone, WhatsApp, Email, ContactForm.
        If a field is not found, use empty string "".

        City: {city}
        HTML snippet (first 8000 chars):
        {html_content[:8000]}

        JSON output:
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean markdown code fences if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            data = json.loads(text)
            # Ensure all keys exist
            for key in ["Name", "Address", "Phone", "WhatsApp", "Email", "ContactForm"]:
                if key not in data:
                    data[key] = ""
            return data
        except Exception as e:
            logger.error(f"Gemini extraction failed: {e}")
            return {}