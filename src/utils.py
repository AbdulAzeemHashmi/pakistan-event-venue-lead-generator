import re

def clean_text(text):
    """Remove extra whitespace and normalize."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def is_duplicate(name, existing_list, threshold=0.8):
    """
    Simple duplicate check using exact match.
    For advanced fuzzy matching, install fuzzywuzzy.
    """
    if not name:
        return False
    name_clean = clean_text(name.lower())
    for existing in existing_list:
        if clean_text(existing.lower()) == name_clean:
            return True
    return False