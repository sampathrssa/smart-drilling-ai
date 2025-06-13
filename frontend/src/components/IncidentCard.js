import React from 'react';

const IncidentCard = ({ incident }) => {
    return (
        <div style={{
            border: '1px solid #ddd',
            padding: '20px',
            marginBottom: '20px',
            borderRadius: '12px',
            backgroundColor: '#f7f7f7',
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
            textAlign: 'left'
        }}>
            <h3 style={{ color: '#007bff' }}>{incident.title}</h3>
            <p><strong>Date:</strong> {incident.date}</p>
            <p style={{ whiteSpace: 'pre-line' }}>{incident.summary}</p>
        </div>
    );
};

export default IncidentCard;
