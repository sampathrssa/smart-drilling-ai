# 🚀 Smart Drilling Incident Investigator AI

An AI-powered safety analysis platform designed for offshore oil & gas safety, built for the Google Cloud AI-in-Action Hackathon.

---

## 🌐 Live Deployment

- **Frontend (Firebase Hosting):** [https://smart-drilling-ai-hackathon.web.app](https://smart-drilling-ai-hackathon.web.app)
- **Backend (Cloud Run API):** [Your Cloud Run URL here]

---

## 🎯 Use Case

Helps drilling engineers quickly analyze past safety incidents by:

- Semantic search of incident reports using Vector Search
- Human-friendly AI agent summaries
- Preventive recommendations generated automatically
- Oil & Gas domain-specific safety guidance

---

## 🛠️ Technologies Used

| Layer | Technology |
| ----- | ----------- |
| PDF Extraction | `pdfminer` (Python) |
| Embedding Generation | Vertex AI `text-embedding-005` |
| Vector Database | MongoDB Atlas Vector Search |
| Backend API | FastAPI (Python 3.10) |
| Deployment | Google Cloud Run |
| Summarization | Gemini 1.5 Pro (Vertex AI Generative AI) |
| Frontend | React (Firebase Hosting) |

---

## 📂 Full Architecture

![System Architecture](architecture-diagram.png)

---

## 🔬 Dataset

- Public BSEE Safety Alerts dataset (US Bureau of Safety and Environmental Enforcement)

---

## 🔄 Full Pipeline

1️⃣ **PDF Extraction:** Extract raw text, dates, metadata from BSEE safety alerts.  
2️⃣ **Embeddings:** Generate vector embeddings using Google Vertex AI.  
3️⃣ **Ingestion:** Store documents & embeddings into MongoDB Atlas Vector Store.  
4️⃣ **Backend API:** FastAPI exposes semantic search API.  
5️⃣ **RAG Summarization:** Gemini 1.5 Pro generates AI summaries.  
6️⃣ **Frontend:** React UI allows users to search & query safety alerts in real-time.

---

## 🧪 Demo Use Case

Example queries supported:

- "Show me recent gas leaks"
- "Any incidents related to nitrogen cylinder failure?"
- "Recent equipment failure injuries"
- "Explosion safety incidents offshore"

---

## 🔧 Local Dev Setup

### Backend

```bash
cd backend/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload


### FrontEnd

cd frontend/
npm install
npm start