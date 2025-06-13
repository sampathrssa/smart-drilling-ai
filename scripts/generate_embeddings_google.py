import json
import time
import requests
import google.auth
from google.auth.transport.requests import Request as GoogleAuthRequest  # <-- THIS IS KEY

# Replace with your project ID
PROJECT_ID = "ssi-ai-learning-project"
LOCATION = "us-central1"
MODEL_ID = "text-embedding-005"

# Load credentials automatically from gcloud auth
credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
auth_token = credentials.token

# Refresh token if expired
if not auth_token or credentials.expired:
    credentials.refresh(GoogleAuthRequest())
    auth_token = credentials.token

# Vertex AI REST endpoint for text-embedding-005
ENDPOINT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:predict"

# Input/output files
INPUT_FILE = "../data/safety_alerts.json"
OUTPUT_FILE = "../data/safety_alerts_with_embeddings.json"

# Load safety alerts
with open(INPUT_FILE, "r") as f:
    alerts = json.load(f)

# Embedding function
def get_embedding(text):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    body = {
        "instances": [{"content": text}],
        "parameters": {"task_type": "RETRIEVAL_DOCUMENT"}
    }
    response = requests.post(ENDPOINT_URL, headers=headers, json=body)
    response.raise_for_status()
    predictions = response.json()["predictions"]
    return predictions[0]["embeddings"]["values"]

# Process all alerts
results = []

for alert in alerts:
    try:
        text_input = f"{alert['title']}. {alert['description']}"
        embedding_vector = get_embedding(text_input)
        alert["embedding"] = embedding_vector
        results.append(alert)
        print(f"✅ Embedded ID {alert['id']} with vector size {len(embedding_vector)}")
        time.sleep(0.2)
    except Exception as e:
        print(f"❌ Error embedding ID {alert['id']}: {e}")

# Save output
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=4)

print(f"\n✅ All embeddings generated and saved to {OUTPUT_FILE}")
