import React, { useState } from "react";
import "./Styles/TicketSystem.css";

const Ticket = () => {
    const [system] = useState("ServiceNow"); // Fixed to ServiceNow
    const [credentials, setCredentials] = useState({ username: "", password: "" });
    const [instanceUrl, setInstanceUrl] = useState(""); // Store the instance URL
    const [authSuccess, setAuthSuccess] = useState(false); // Track authentication status
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState(1); // Track the current step (1: Auth, 2: Instance URL, 3: Save)
    const [urlError, setUrlError] = useState(""); // Track URL error message

    const handleAuthSubmit = () => {
        setLoading(true);
        fetch("http://127.0.0.1:5000/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                system,
                username: credentials.username,
                password: credentials.password,
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                setLoading(false);
                if (data.success) {
                    localStorage.setItem("auth_token", data.token); // Store token
                    localStorage.setItem("password", credentials.password); // Store password
                    setAuthSuccess(true);
                    setStep(2); // Move to Instance URL step
                    alert("Authentication successful!");
                } else {
                    setAuthSuccess(false);
                    alert(data.message);
                }
            })
            .catch(() => {
                setLoading(false);
                alert("Authentication failed due to a server error. Please try again.");
            });
    };

    const handleSave = () => {
        // Updated validation logic
        const urlRegex = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
        if (instanceUrl.indexOf("www.") > -1 || !urlRegex.test(instanceUrl)) {
            setUrlError("Please enter a valid URL (e.g., https://example.com).");
            return;
        }

        setUrlError(""); // Clear error if URL is valid

        fetch("http://127.0.0.1:5000/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
            body: JSON.stringify({
                system,
                instance_url: instanceUrl,
                password: localStorage.getItem("password"), // Use saved password
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert("Data saved successfully!");
                } else {
                    alert(data.message);
                }
            })
            .catch(() => alert("Error connecting to the server."));
    };

    return (
        <div className="ticket-container">
            <h1>ServiceNow Admin Portal</h1>

            {step === 1 && (
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
                </div>
            )}

            {step === 2 && authSuccess && (
                <div className="url-step">
                    <label>
                        Instance URL:
                        <input
                            type="text"
                            value={instanceUrl}
                            onChange={(e) => setInstanceUrl(e.target.value)}
                        />
                    </label>
                    {urlError && <div className="error-message">{urlError}</div>}
                    <button onClick={handleSave}>Save</button>
                </div>
            )}

            {authSuccess && <div className="success-message">Welcome, Admin!</div>}
        </div>
    );
};

export default Ticket;
