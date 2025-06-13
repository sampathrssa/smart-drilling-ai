import json
from pymongo import MongoClient

# 🔧 Update your MongoDB Atlas URI:
MONGODB_URI = "mongodb+srv://ssiadmin:Smart2025$@samcluster.etajvho.mongodb.net/?retryWrites=true&w=majority&appName=SamCluster"

# Database & Collection details:
DATABASE_NAME = "drilling_ai"
COLLECTION_NAME = "incidents"

# Embedded data file:
INPUT_FILE = "../data/safety_alerts_with_embeddings.json"

# Load JSON data
with open(INPUT_FILE, "r") as f:
    alerts = json.load(f)

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_URI)
collection = client[DATABASE_NAME][COLLECTION_NAME]

# Ingest each record
for alert in alerts:
    doc = {
        "_id": alert["id"],
        "title": alert["title"],
        "description": alert["description"],
        "date": alert["date"],
        "embedding": alert["embedding"]  # <-- very important for vector search
    }
    collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
    print(f"✅ Inserted ID {doc['_id']}")

print("\n✅ All records ingested successfully into MongoDB Atlas Vector Store.")
