from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import google.auth
from google.auth.transport.requests import Request as GoogleAuthRequest
import google.generativeai as genai
import requests
import re
from datetime import datetime

# === Initialize FastAPI ===
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://smart-drilling-ai-hackathon.web.app"  # ✅ Add your live Firebase URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === MongoDB Atlas connection details ===
MONGODB_URI = "mongodb+srv://ssiadmin:Smart2025$@samcluster.etajvho.mongodb.net/?retryWrites=true&w=majority&appName=SamCluster"
DATABASE_NAME = "drilling_ai"
COLLECTION_NAME = "incidents"
client = MongoClient(MONGODB_URI)
collection = client[DATABASE_NAME][COLLECTION_NAME]

# === Vertex AI Embedding model details ===
PROJECT_ID = "ssi-ai-learning-project"
LOCATION = "us-central1"
MODEL_ID = "text-embedding-005"

# Auth for Vertex AI Embeddings
credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
if not credentials.valid or credentials.expired:
    credentials.refresh(GoogleAuthRequest())
auth_token = credentials.token

ENDPOINT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:predict"

# === Gemini Generative AI initialization ===
genai.configure(api_key="AIzaSyCvVHeltuFaGTsQ27PECOVY0-V1ygJmNh4")
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# === Pydantic request schema ===
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# === Embedding function for MongoDB Vector Search ===
def embed_query(text):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    body = {
        "instances": [{"content": text}],
        "parameters": {"task_type": "RETRIEVAL_QUERY"}
    }
    response = requests.post(ENDPOINT_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["predictions"][0]["embeddings"]["values"]

# === Extract Date from Description (fallback if date missing) ===
def extract_date_from_description(description):
    date_pattern = r'([A-Z][a-z]+ \d{1,2}, \d{4})'
    match = re.search(date_pattern, description)
    if match:
        try:
            parsed_date = datetime.strptime(match.group(1), "%B %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except Exception:
            return "Date Parsing Failed"
    return "Date Unknown"

# === Gemini-powered structured summarization ===
def summarize_description(text, location=None):
    base_prompt = (
        "You are Smart Drilling Incident Investigator AI Agent, tasked to generate precise, professional, and easy-to-read summaries of offshore safety incidents for engineers and business stakeholders.\n"
        "Given the following incident description, produce a 3-part summary:\n\n"
        "1️⃣ What Happened: One clear sentence on the incident.\n"
        "2️⃣ Consequences: One clear sentence on any injuries, damages or outcomes.\n"
        "3️⃣ Prevention: One clear sentence with recommended preventive actions.\n\n"
    )

    if location:
        base_prompt += f"The incident occurred at location: {location}\n\n"

    full_prompt = base_prompt + f"Incident Description:\n{text}\n\nAI Summary:"

    try:
        response = gemini_model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini summarization failed: {e}")
        return text[:300] + "..."

# === The main RAG API endpoint ===
@app.post("/query")
def query_incidents(request: QueryRequest):
    query_embedding = embed_query(request.query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": request.top_k
            }
        }
    ])

    output = []
    for doc in results:
        summary = summarize_description(doc["description"])

        if doc["date"]:
            clean_date = doc["date"]
        else:
            clean_date = extract_date_from_description(doc["description"])

        output.append({
            "id": doc["_id"],
            "title": doc["title"],
            "summary": summary,
            "date": clean_date
        })

    return {"results": output}
