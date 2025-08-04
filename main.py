from fastapi import FastAPI, Request
from pydantic import BaseModel
from googletrans import Translator
import json

app = FastAPI()
translator = Translator()

with open("contacts.json", "r", encoding="utf-8") as f:
    contacts = json.load(f)

class Query(BaseModel):
    message: str

@app.post("/process")
def process(query: Query):
    # Step 1: Translate
    translated = translator.translate(query.message, src='auto', dest='en').text

    # Step 2: Classify (simplified)
    issue_type = "water" if "water" in translated.lower() else "electricity"

    # Step 3: Get location (example only)
    location = "Delhi"  # You can extract using spaCy or manual input

    # Step 4: Lookup contact
    email = contacts.get(issue_type, {}).get(location, "contact@gov.in")

    # Step 5: Generate email
    email_text = f"""Subject: Regarding {issue_type} issue

Dear Sir/Madam,

I am writing to report a {issue_type} issue in {location}. The issue is:
"{translated}"

Kindly address the issue at your earliest.

Sincerely,
Citizen
"""

    # Step 6: Back translate (optional)
    back_translated = translator.translate(email_text, src='en', dest='hi').text

    return {
        "english_draft": email_text,
        "hindi_draft": back_translated,
        "email_to": email
    }
