import React, { useState } from "react";
import "./Styles/TicketSystem.css";

const Ticket = () => {
    const [system, setSystem] = useState(""); // Selected system
    const [credentials, setCredentials] = useState({ username: "", password: "" });
    const [instanceUrl, setInstanceUrl] = useState(""); // Instance URL
    const [step, setStep] = useState(1); // 1: System Select, 2: Auth, 3: URL Validation
    const [loading, setLoading] = useState(false);
    const [authSuccess, setAuthSuccess] = useState(false); // Track authentication status
    const [urlValid, setUrlValid] = useState(false); // Track URL validation status

    const ticketingSystems = ["ServiceNow", "Zendesk", "Jira", "Remedyforce"];

    const handleAuthSubmit = () => {
        setLoading(true);
        fetch("http://127.0.0.1:5000/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...credentials, system }),
        })
            .then((res) => res.json())
            .then((data) => {
                setLoading(false);
                if (data.success) {
                    setAuthSuccess(true);
                    setTimeout(() => setStep(3), 2000); // Proceed to URL validation step
                } else {
                    alert(data.message);
                }
            })
            .catch((error) => {
                setLoading(false);
                alert("Authentication failed. Please try again.");
            });
    };

    const handleUrlValidation = () => {
        if (instanceUrl) {
            setLoading(true);
            fetch("http://127.0.0.1:5000/validate-url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ instance_url: instanceUrl }),
            })
                .then((res) => res.json())
                .then((data) => {
                    setLoading(false);
                    if (data.success) {
                        setUrlValid(true);
                        alert("Instance URL validated successfully!");
                    } else {
                        alert("Invalid Instance URL.");
                    }
                })
                .catch((error) => {
                    setLoading(false);
                    alert("Error connecting to the server.");
                });
        } else {
            alert("Please enter a valid URL.");
        }
    };

    const handleSave = () => {
        fetch("http://127.0.0.1:5000/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ system, instanceUrl }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert("Data saved successfully!");
                } else {
                    alert("Error saving data.");
                }
            })
            .catch((error) => alert("Error connecting to the server."));
    };

    return (
        <div className="ticket-container">
            <h1>Ticketing System</h1>

            {step === 1 && (
                <div className="dropdown-step">
                    <label>
                        Select Ticketing System:
                        <select value={system} onChange={(e) => setSystem(e.target.value)}>
                            <option value="">-- Select --</option>
                            {ticketingSystems.map((sys) => (
                                <option key={sys} value={sys}>
                                    {sys}
                                </option>
                            ))}
                        </select>
                    </label>
                    <button onClick={() => system && setStep(2)} disabled={!system}>
                        Next
                    </button>
                </div>
            )}

            {step === 2 && (
                <div className="credentials-step">
                    <label>
                        Username:
                        <input
                            type="text"
                            value={credentials.username}
                            onChange={(e) =>
                                setCredentials({ ...credentials, username: e.target.value })
                            }
                        />
                    </label>
                    <label>
                        Password:
                        <input
                            type="password"
                            value={credentials.password}
                            onChange={(e) =>
                                setCredentials({ ...credentials, password: e.target.value })
                            }
                        />
                    </label>
                    {loading ? (
                        <div className="spinner">Authenticating...</div>
                    ) : (
                        <button onClick={handleAuthSubmit}>Authenticate</button>
                    )}
                    {authSuccess && <div className="success-animation">Authentication Successful!</div>}
                </div>
            )}

            {step === 3 && (
                <div className="url-step">
                    <label>
                        Instance URL:
                        <input
                            type="text"
                            value={instanceUrl}
                            onChange={(e) => setInstanceUrl(e.target.value)}
                        />
                    </label>
                    <button onClick={handleUrlValidation}>Validate URL</button>
                    {urlValid && (
                        <button onClick={handleSave} className="save-button">
                            Save
                        </button>
                    )}
                </div>
            )}
        </div>
    );
};

export default Ticket;
