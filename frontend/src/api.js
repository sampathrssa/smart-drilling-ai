import axios from 'axios';

const api = axios.create({
    baseURL: 'https://drilling-ai-backend-350279140213.us-central1.run.app', // Point to your FastAPI backend
});


export default api;
