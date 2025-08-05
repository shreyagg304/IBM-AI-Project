from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()
translator = Translator()

with open("contacts.json", "r", encoding="utf-8") as f:
    contacts = json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin like ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

# Serve the frontend folder (static files if you have CSS/JS later)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/")
def read_index():
    index_path = os.path.join("frontend", "index.html")
    return FileResponse(index_path)


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
