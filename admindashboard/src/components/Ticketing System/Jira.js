import React, { useState } from "react";
import axios from "axios";

function App() {
  const [jiraUrl, setJiraUrl] = useState("");
  const [username, setUsername] = useState("");
  const [apiToken, setApiToken] = useState("");
  const [authToken, setAuthToken] = useState(null);
  const [message, setMessage] = useState("");

  const handleAuthenticate = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5102/authenticate", {
        instanceUrl: jiraUrl,
        username: username,
        password: apiToken,
      });

      if (response.data.success) {
        setAuthToken(response.data.token);
        setMessage("Authentication successful!");
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage("Error authenticating: " + error.message);
    }
  };

  const handleSaveCredentials = async () => {
    if (!authToken) {
      setMessage("Please authenticate first.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5102/save",
        {
          instance_url: jiraUrl,
          username: username,
          password: apiToken,
        },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (response.data.success) {
        setMessage("Credentials saved successfully!");
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage("Error saving credentials: " + error.message);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h2>Jira Authentication</h2>

      <div style={{ marginBottom: "10px" }}>
        <label>Jira URL:</label>
        <input
          type="text"
          placeholder="https://your-jira-instance.atlassian.net"
          value={jiraUrl}
          onChange={(e) => setJiraUrl(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>

      <div style={{ marginBottom: "10px" }}>
        <label>Username:</label>
        <input
          type="text"
          placeholder="Your Jira username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>

      <div style={{ marginBottom: "10px" }}>
        <label>API Token:</label>
        <input
          type="password"
          placeholder="Your Jira API token"
          value={apiToken}
          onChange={(e) => setApiToken(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>

      {message && <div style={{ color: "red", marginBottom: "10px" }}>{message}</div>}

      <div style={{ marginTop: "20px" }}>
        <button
          onClick={handleAuthenticate}
          style={{
            padding: "10px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            width: "100%",
            marginBottom: "10px",
          }}
        >
          Authenticate
        </button>
        <button
          onClick={handleSaveCredentials}
          style={{
            padding: "10px",
            backgroundColor: "#28a745",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            width: "100%",
          }}
          disabled={!authToken}
        >
          Save Credentials
        </button>
      </div>

      {message && (
        <div
          style={{
            marginTop: "20px",
            padding: "10px",
            backgroundColor: "#f8f8f8",
            border: "1px solid #ddd",
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
}

export default App;
