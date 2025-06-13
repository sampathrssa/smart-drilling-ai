# File: scripts/generate_embeddings.py (bulletproof version)

import json
import os
import time

from google.cloud import aiplatform_v1
from google.auth import default

# Setup your GCP project and location
PROJECT_ID = "ssi-ai-learning-project"    # <-- replace
LOCATION = "us-central1"              # <-- adjust region

# Input/Output Files
INPUT_FILE = "../data/safety_alerts.json"
OUTPUT_FILE = "../data/safety_alerts_with_embeddings.json"

# Vertex AI Embedding Model
MODEL = "textembedding-gecko@latest"

# Load your safety alerts
with open(INPUT_FILE, "r") as f:
    alerts = json.load(f)

# Setup Vertex AI client with your default credentials
credentials, project = default()
client = aiplatform_v1.PredictionServiceClient(credentials=credentials)

# Build endpoint path for embedding model
endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL}"

def get_embedding(text):
    instance = {"content": text}
    instances = [instance]
    parameters = {}

    response = client.predict(
        endpoint=endpoint,
        instances=instances,
        parameters=parameters,
    )

    return response.predictions[0]["embeddings"]["values"]

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
