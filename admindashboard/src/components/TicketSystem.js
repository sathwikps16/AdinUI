import React, { useState } from 'react';
import search from '../img/servicenow.png';
import zendesk from '../img/zendesk.png';
import Remedyforce from '../img/remedyforce.png';
import Jira from '../img/jira.png';
import "./Styles/TicketSystem.css";

const Ticket = () => {
    const [activeCard, setActiveCard] = useState('');
    const [instanceUrls, setInstanceUrls] = useState({});

    // Toggle the active card
    const toggleCard = (appName) => {
        setActiveCard(activeCard === appName ? '' : appName);
    };

    // Handle input change for instance URL
    const handleInputChange = (appName, value) => {
        setInstanceUrls({ ...instanceUrls, [appName]: value });
    };

    // Handle save action for an app
    const handleSave = async (appName) => {
        const url = instanceUrls[appName];
        if (!url) {
            alert('Please enter a valid URL');
            return;
        }

        try {
            // Send POST request to the Flask backend
            const response = await fetch('http://127.0.0.1:5000/ticketing-system', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    Service_name: appName, // Service name
                    Instance_URL: url,    // Instance URL
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(`URL for ${appName} saved successfully!`);
            } else {
                alert(`Error: ${data.message}`);
            }
            setInstanceUrls({ ...instanceUrls, [appName]: '' }); // Reset the URL for the app
        } catch (error) {
            alert('Error saving the ticketing system URL!');
            console.error('Error:', error);
        }
    };

    return (
        <div className="ticket-container">
            <h1>Ticketing System</h1>
            <div className="cards">
                {/* ServiceNow Card */}
                <div className={`card ${activeCard === 'ServiceNow' ? 'active' : ''}`} onClick={() => toggleCard('ServiceNow')}>
                    <img src={search} alt="ServiceNow" />
                    <p>ServiceNow</p>
                    {activeCard === 'ServiceNow' && (
                        <div className="card-details">
                            <label>
                                Instance URL:
                                <input
                                    type="text"
                                    value={instanceUrls['ServiceNow'] || ''}
                                    onChange={(e) => handleInputChange('ServiceNow', e.target.value)}
                                    placeholder="Enter instance URL"
                                />
                            </label>
                            <button onClick={() => handleSave('ServiceNow')}>Save</button>
                        </div>
                    )}
                </div>

                {/* Zendesk Card */}
                <div className={`card ${activeCard === 'Zendesk' ? 'active' : ''}`} onClick={() => toggleCard('Zendesk')}>
                    <img src={zendesk} alt="Zendesk" />
                    <p>Zendesk</p>
                    {activeCard === 'Zendesk' && (
                        <div className="card-details">
                            <label>
                                Instance URL:
                                <input
                                    type="text"
                                    value={instanceUrls['Zendesk'] || ''}
                                    onChange={(e) => handleInputChange('Zendesk', e.target.value)}
                                    placeholder="Enter instance URL"
                                />
                            </label>
                            <button onClick={() => handleSave('Zendesk')}>Save</button>
                        </div>
                    )}
                </div>

                {/* Remedyforce Card */}
                <div className={`card ${activeCard === 'Remedyforce' ? 'active' : ''}`} onClick={() => toggleCard('Remedyforce')}>
                    <img src={Remedyforce} alt="Remedyforce" />
                    <p>Remedyforce</p>
                    {activeCard === 'Remedyforce' && (
                        <div className="card-details">
                            <label>
                                Instance URL:
                                <input
                                    type="text"
                                    value={instanceUrls['Remedyforce'] || ''}
                                    onChange={(e) => handleInputChange('Remedyforce', e.target.value)}
                                    placeholder="Enter instance URL"
                                />
                            </label>
                            <button onClick={() => handleSave('Remedyforce')}>Save</button>
                        </div>
                    )}
                </div>

                {/* Jira Card */}
                <div className={`card ${activeCard === 'Jira' ? 'active' : ''}`} onClick={() => toggleCard('Jira')}>
                    <img src={Jira} alt="Jira" />
                    <p>Jira</p>
                    {activeCard === 'Jira' && (
                        <div className="card-details">
                            <label>
                                Instance URL:
                                <input
                                    type="text"
                                    value={instanceUrls['Jira'] || ''}
                                    onChange={(e) => handleInputChange('Jira', e.target.value)}
                                    placeholder="Enter instance URL"
                                />
                            </label>
                            <button onClick={() => handleSave('Jira')}>Save</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Ticket;
