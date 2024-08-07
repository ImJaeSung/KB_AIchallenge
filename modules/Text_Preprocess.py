import re

class TextProcessor:
    def __init__(self):
        self.split_pattern = re.compile(r'(의|가|은|는|을|를|에|에서|에게)\b')
        self.clean_pattern = re.compile(
            r'\\n|\\u[a-zA-Z0-9]{4}|\\u200b|\\|http[^\s]*|\'|\"|<br/>|</p>'
        )

    # extract word from query
    def extract_first_noun_phrase(self, query):
        parts = self.split_pattern.split(query, maxsplit=1)

        if parts:
            return parts[0].strip()
        else:
            return None


    # text cleaning
    def clean_text(self, text):
        cleaned_text = re.sub(self.clean_pattern, ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        return cleaned_text.strip()