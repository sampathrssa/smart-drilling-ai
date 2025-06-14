import React, { useState } from 'react';
import api from './api';
import IncidentCard from './components/IncidentCard';
import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        setLoading(true);
        try {
            const response = await api.post('/query', { query, top_k: 5 });
            setResults(response.data.results);
        } catch (error) {
            console.error('Error:', error);
            alert('Error querying backend');
        }
        setLoading(false);
    };

    return (
        <div className="container">
            <div className="left-panel">
                <div className="left-content">
                    <img src="/offshore_rig.png" alt="Offshore Rig" className="rig-image" />
                    <div className="example-queries">
                        <h3>Example Queries</h3>
                        <ul>
                            <li>Show me recent gas leaks</li>
                            <li>Any incidents related to nitrogen cylinder failure?</li>
                            <li>Recent equipment failure injuries</li>
                            <li>Explosion safety incidents offshore</li>
                        </ul>
                    </div>
                </div>
            </div>


            <div className="right-panel">
                <h1>Smart Drilling Incident Investigator</h1>
                <p>AI-powered RAG Engine for Offshore Oil & Gas Safety</p>

                <div className="search-section">
                    <input
                        type="text"
                        placeholder="Ask a safety incident question..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="search-input"
                    />
                    <button onClick={handleSearch} disabled={loading} className="search-button">
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>

                <div className="results-section">
                    {results.map((incident) => (
                        <IncidentCard key={incident.id} incident={incident} />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
