import React, { useState } from 'react';
import search from '../img/servicenow.png';
import zendesk from '../img/zendesk.png';
import "./Styles/TicketSystem.css"

const Ticket = () => {
    const [modal, setModal] = useState({ isOpen: false, app: '' });
    const [url, setUrl] = useState('');

    const openModal = (appName) => {
        setModal({ isOpen: true, app: appName });
    };

    const closeModal = () => {
        setModal({ isOpen: false, app: '' });
        setUrl('');
    };

    const handleSave = () => {
        alert(`URL for ${modal.app} saved: ${url}`);
        closeModal();
    };

    return (
        <div className="ticket-container">
            <h1>Ticketing System</h1>
            <div className="cards">
                <div className="card" onClick={() => openModal('ServiceNow')}>
                    <img src={search} alt="ServiceNow" />
                    <p>ServiceNow</p>
                </div>
                <div className="card" onClick={() => openModal('Zendesk')}>
                    <img src={zendesk} alt="Zendesk" />
                    <p>Zendesk</p>
                </div>
            </div>

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
