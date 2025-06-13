import os
import re
import json
import time
from datetime import datetime

import requests
import google.auth
from google.auth.transport.requests import Request as GoogleAuthRequest
from pymongo import MongoClient
from pdfminer.high_level import extract_text

# === CONFIGURATION ===

# Paths
RAW_ALERTS_DIR = "../data/raw_alerts"
EXTRACTED_JSON = "../data/safety_alerts.json"
EMBEDDED_JSON = "../data/safety_alerts_with_embeddings.json"

# MongoDB Atlas
MONGODB_URI = "mongodb+srv://ssiadmin:Smart2025$@samcluster.etajvho.mongodb.net/?retryWrites=true&w=majority&appName=SamCluster"
DATABASE_NAME = "drilling_ai"
COLLECTION_NAME = "incidents"

# Vertex AI Embedding
PROJECT_ID = "ssi-ai-learning-project"
LOCATION = "us-central1"
MODEL_ID = "text-embedding-005"

# === STEP 1: PDF EXTRACTION ===

def extract_date(full_text):
    published_match = re.search(r'Published:\s*(\d{1,2}/\d{1,2}/\d{4})', full_text)
    if published_match:
        raw_date = published_match.group(1)
        try:
            parsed_date = datetime.strptime(raw_date, "%m/%d/%Y")
            return parsed_date.strftime("%Y-%m-%d")
        except:
            pass

    md_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', full_text)
    if md_match:
        raw_date = md_match.group(1)
        try:
            parsed_date = datetime.strptime(raw_date, "%B %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except:
            pass

    return None

def extract_from_pdf(filepath):
    record = {}
    full_text = extract_text(filepath)
    match_id = re.search(r'SA_(\d+)', filepath)
    record["id"] = int(match_id.group(1)) if match_id else None

    lines = full_text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    record["title"] = lines[0] if lines else "Unknown Title"
    record["date"] = extract_date(full_text)
    record["description"] = "\n".join(lines[1:]) if len(lines) > 1 else ""
    return record

def extract_all():
    records = []
    for file in os.listdir(RAW_ALERTS_DIR):
        if file.endswith(".pdf"):
            filepath = os.path.join(RAW_ALERTS_DIR, file)
            data = extract_from_pdf(filepath)
            if data:
                records.append(data)
    with open(EXTRACTED_JSON, "w") as f:
        json.dump(records, f, indent=4)
    print(f"✅ Extracted {len(records)} PDFs")

# === STEP 2: EMBEDDING GENERATION ===

def generate_embeddings():
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not credentials.valid or credentials.expired:
        credentials.refresh(GoogleAuthRequest())
    auth_token = credentials.token

    ENDPOINT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:predict"

    with open(EXTRACTED_JSON, "r") as f:
        alerts = json.load(f)

    results = []
    for alert in alerts:
        text_input = f"{alert['title']}. {alert['description']}"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        body = {
            "instances": [{"content": text_input}],
            "parameters": {"task_type": "RETRIEVAL_DOCUMENT"}
        }
        try:
            response = requests.post(ENDPOINT_URL, headers=headers, json=body)
            response.raise_for_status()
            vector = response.json()["predictions"][0]["embeddings"]["values"]
            alert["embedding"] = vector
            results.append(alert)
            print(f"✅ Embedded ID {alert['id']}")
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Error embedding ID {alert['id']}: {e}")

    with open(EMBEDDED_JSON, "w") as f:
        json.dump(results, f, indent=4)
    print(f"✅ All embeddings generated")

# === STEP 3: MONGODB INGESTION ===

def ingest_mongodb():
    client = MongoClient(MONGODB_URI)
    collection = client[DATABASE_NAME][COLLECTION_NAME]

    # Optional: Clear existing data first
    collection.delete_many({})
    print("✅ MongoDB: Existing collection cleared")

    with open(EMBEDDED_JSON, "r") as f:
        alerts = json.load(f)

    for alert in alerts:
        doc = {
            "_id": alert["id"],
            "title": alert["title"],
            "description": alert["description"],
            "date": alert["date"],
            "embedding": alert["embedding"]
        }
        collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        print(f"✅ Inserted ID {doc['_id']}")

    print("\n✅ All documents inserted into MongoDB!")

# === MAIN RUNNER ===

if __name__ == "__main__":
    extract_all()
    generate_embeddings()
    ingest_mongodb()
    print("\n✅ FULL DATA PIPELINE COMPLETED ✅")
