import React, { useState } from "react";
import "./Styles/ServiceNow.css";

const Ticket = () => {
    const [credentials, setCredentials] = useState({ username: "", password: "", instanceUrl: "" });
    const [authSuccess, setAuthSuccess] = useState(false);
    const [loading, setLoading] = useState(false);
    const [urlError, setUrlError] = useState("");

    const handleSubmit = () => {
        const { instanceUrl, username, password } = credentials;

        if (!instanceUrl || !username || !password) {
            setUrlError("Please provide all required fields.");
            return;
        }

        const urlRegex = /^(https?:\/\/)?([\w\d\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
        if (!urlRegex.test(instanceUrl)) {
            setUrlError("Please enter a valid URL.");
            return;
        }

        setLoading(true);
        setUrlError(""); // Clear error if URL is valid

        fetch("http://127.0.0.1:5000/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ instanceUrl, username, password }),
        })
            .then((res) => res.json())
            .then((data) => {
                setLoading(false);
                if (data.success) {
                    localStorage.setItem("auth_token", data.token);
                    alert("Authentication successful!");
                    setAuthSuccess(true);
                } else {
                    alert(data.message);
                }
            })
            .catch(() => {
                setLoading(false);
                alert("Authentication failed due to a server error. Please try again.");
            });
    };

    const handleSave = () => {
        const { instanceUrl } = credentials;

        fetch("http://127.0.0.1:5000/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
            body: JSON.stringify({
                system: "ServiceNow",
                instance_url: instanceUrl,
                password: credentials.password, // Use the same password
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
            <h1>Zendesk Admin Portal</h1>
            <div className="credentials-step">
                <label>
                    Instance URL:
                    <input
                        type="text"
                        value={credentials.instanceUrl}
                        onChange={(e) =>
                            setCredentials({ ...credentials, instanceUrl: e.target.value })
                        }
                    />
                </label>
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
                {urlError && <div className="error-message">{urlError}</div>}
                {loading ? (
                    <div className="spinner">Authenticating...</div>
                ) : (
                    <button onClick={handleSubmit}>Authenticate</button>
                )}
            </div>

            {authSuccess && (
                <div className="save-step">
                    <button onClick={handleSave}>Save Data</button>
                </div>
            )}
        </div>
    );
};

export default Ticket;
