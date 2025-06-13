import json
from pymongo import MongoClient
import google.auth
from google.auth.transport.requests import Request as GoogleAuthRequest
import requests

# MongoDB Atlas connection string
MONGODB_URI = "mongodb+srv://ssiadmin:Smart2025$@samcluster.etajvho.mongodb.net/?retryWrites=true&w=majority&appName=SamCluster"
DATABASE_NAME = "drilling_ai"
COLLECTION_NAME = "incidents"

# Vertex AI model details
PROJECT_ID = "ssi-ai-learning-project"
LOCATION = "us-central1"
MODEL_ID = "text-embedding-005"

# Authenticate with Google Vertex AI (ADC)
credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
if not credentials.valid or credentials.expired:
    credentials.refresh(GoogleAuthRequest())
auth_token = credentials.token

ENDPOINT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:predict"

# Embedding function for query text
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

# Prepare semantic query
query_text = "gas leak incident related to pipeline corrosion"
query_embedding = embed_query(query_text)

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
collection = client[DATABASE_NAME][COLLECTION_NAME]

# Perform vector search in MongoDB Atlas
results = collection.aggregate([
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 100,
            "limit": 5
        }
    }
])

# Output top results
print(f"\nTop semantic matches for query: '{query_text}'\n")
for doc in results:
    print(f"ID: {doc['_id']}, Title: {doc['title']}")
    print(f"Description: {doc['description'][:200]}...\n")  # Show partial description
