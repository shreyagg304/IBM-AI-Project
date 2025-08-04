# backend/utils.py

from googletrans import Translator
import spacy

translator = Translator()
nlp = spacy.load("en_core_web_sm")  # For location extraction

def translate_to_english(text):
    translated = translator.translate(text, src='auto', dest='en')
    return translated.text

def translate_to_hindi(text):
    translated = translator.translate(text, src='en', dest='hi')
    return translated.text

def classify_issue(text):
    # Simple keyword-based classification (you can upgrade to ML later)
    text_lower = text.lower()
    if "water" in text_lower:
        return "water"
    elif "electricity" in text_lower or "power" in text_lower:
        return "electricity"
    elif "income" in text_lower or "certificate" in text_lower:
        return "income_certificate"
    elif "ration" in text_lower:
        return "ration"
    else:
        return "general"

def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE = location
            return ent.text
    return "Delhi"  # Default fallback
