# 🚀 Smart Drilling Incident Investigator AI 


An AI-powered safety analysis platform designed for offshore oil & gas safety, built for the Google Cloud AI-in-Action Hackathon.

Team Members | Submission by : 

**Murugadass Krishnan** : https://www.linkedin.com/in/murugadass-krishnan-694ba57/

**Sampath Ramanujam**   : https://www.linkedin.com/in/sampath-ramanujam-4842402/

---

## 🌐 Live Deployment

- **Frontend (Firebase Hosting):** [https://smart-drilling-ai-hackathon.web.app](https://smart-drilling-ai-hackathon.web.app)
- **Backend (Cloud Run API):** (https://drilling-ai-backend-350279140213.us-central1.run.app)

---

## 🎯 Use Case

Helps drilling engineers quickly analyze past safety incidents by:

- Semantic search of incident reports using Vector Search
- Human-friendly AI agent summaries
- Preventive recommendations generated automatically
- Oil & Gas domain-specific safety guidance

---

**Project Summary**

The Smart Drilling Incident Investigator AI is an end-to-end Retrieval-Augmented Generation (RAG) platform that empowers oil & gas safety engineers to analyze offshore drilling incident reports. The solution uses multiple Google Cloud tools integrated with MongoDB Atlas Vector Search to enable real-time semantic search and AI-powered safety recommendations.


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
https://www.bsee.gov/guidance-and-regulations/guidance/safety-alerts-program
https://www.bsee.gov/resources-tools/incident-reporting
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
