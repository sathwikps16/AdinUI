import React, { useState } from 'react';
import servicenow from '../img/servicenow.png';
import zendesk from '../img/zendesk.png';
import remedyforce from '../img/remedyforce.png';
import jira from '../img/jira.png';
import "./Styles/TicketSystem.css";

const Ticket = () => {
    const [activeCard, setActiveCard] = useState(null); 
    const [urls, setUrls] = useState({}); 

    
    const images = {
        ServiceNow: servicenow,
        Zendesk: zendesk,
        Remedyforce: remedyforce,
        Jira: jira,
    };

    const toggleCard = (appName) => {
        setActiveCard((prev) => (prev === appName ? null : appName));
    };

    // Update the instance URL for a specific card
    const handleUrlChange = (appName, value) => {
        setUrls((prevUrls) => ({ ...prevUrls, [appName]: value }));
    };

    const handleSave = (appName) => {
        const instanceUrl = urls[appName];
        if (!instanceUrl) {
            alert('Please enter a valid URL');
            return;
        }

        // Replace with your backend call logic
        fetch('http://127.0.0.1:5000/ticketing-system', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Service_name: appName,
                Instance_URL: instanceUrl,
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert(`URL for ${appName} saved successfully!`);
                } else {
                    alert(`Success! ${data.message}`);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Error saving the ticketing system URL!');
            });
    };

    return (
        <div className="ticket-container">
            <h1>Ticketing System</h1>
            <div className="cards">
                {Object.keys(images).map((appName) => (
                    <div
                        key={appName}
                        className={`card ${activeCard === appName ? 'active' : ''}`}
                        onClick={() => toggleCard(appName)}
                    >
                        <img
                            src={images[appName]} 
                            alt={appName}
                        />
                        <p>{appName}</p>
                        {activeCard === appName && (
                            <div
                                className="card-details"
                                onClick={(e) => e.stopPropagation()} // Prevent parent card toggle
                            >
                                <label>
                                    Instance URL:
                                    <input
                                        type="text"
                                        value={urls[appName] || ''}
                                        onChange={(e) =>
                                            handleUrlChange(appName, e.target.value)
                                        }
                                        placeholder="Enter instance URL"
                                    />
                                </label>
                                <button onClick={() => handleSave(appName)}>Save</button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Ticket;
