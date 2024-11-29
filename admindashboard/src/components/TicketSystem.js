// Ticket System

import React, { useState } from 'react';
import search from '../img/servicenow.png';
import zendesk from '../img/zendesk.png';
import "./Styles/TicketSystem.css";

const Ticket = () => {
    const [modal, setModal] = useState({ isOpen: false, app: '' });
    const [url, setUrl] = useState('');

    // Open the modal with the selected app name
    const openModal = (appName) => {
        setModal({ isOpen: true, app: appName });
    };

    // Close the modal and reset fields
    const closeModal = () => {
        setModal({ isOpen: false, app: '' });
        setUrl('');
    };

    // Handle save action
    const handleSave = async () => {
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
                    Service_name: modal.app,   // Service name (appName)
                    Instance_URL: url,        // Instance URL entered by the user
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(`URL for ${modal.app} saved successfully!`);
            } else {
                alert(`Error: ${data.message}`);
            }
            closeModal();
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
                <div className="card" onClick={() => openModal('ServiceNow')}>
                    <img src={search} alt="ServiceNow" />
                    <p>ServiceNow</p>
                </div>

                {/* Zendesk Card */}
                <div className="card" onClick={() => openModal('Zendesk')}>
                    <img src={zendesk} alt="Zendesk" />
                    <p>Zendesk</p>
                </div>

                {/* Remedyforce */}
                <div className="card" onClick={() => openModal('Zendesk')}>
                    <img src={zendesk} alt="Remedyforce" />
                    <p>Zendesk</p>
                </div>

                {/* Jira */}
                <div className="card" onClick={() => openModal('Zendesk')}>
                    <img src={zendesk} alt="Jira" />
                    <p>Zendesk</p>
                </div>

                
            </div>

            {/* Modal Section */}
            {modal.isOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>{modal.app}</h2>
                        <label>
                            Instance URL:
                            <input
                                type="text"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="Enter instance URL"
                            />
                        </label>
                        <div className="modal-actions">
                            <button onClick={handleSave}>Save</button>
                            <button onClick={closeModal}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Ticket;
