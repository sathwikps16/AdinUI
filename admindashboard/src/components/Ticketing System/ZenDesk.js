import React, { useState } from "react";
import axios from "axios";

const ZendeskForm = () => {
  const [formData, setFormData] = useState({
    instance_url: "",
    admin_id: "",
    api_token: "", // Changed from password to api_token
  });
  const [message, setMessage] = useState("");
  const [authenticated, setAuthenticated] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAuthenticate = async () => {
    try {
      const response = await axios.post("http://localhost:5104/zendesk/authenticate", formData);
      if (response.data.success) {
        setAuthenticated(true);
        setMessage("Admin Credentials Verified You Can Save The Data!!");
      } else {
        setMessage(`Error: ${response.data.message}`);
      }
    } catch (error) {
      setMessage("An error occurred during authentication.");
      console.error(error);
    }
  };

  const handleSave = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5104/zendesk/save",
        formData,
        { headers: { Authorization: "Bearer zendesk-example-token" } }
      );
      if (response.data.success) {
        setMessage("Credentials saved successfully!");
      } else {
        setMessage(`Error: ${response.data.message}`);
      }
    } catch (error) {
      setMessage("An error occurred while saving credentials.");
      console.error(error);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h2>Zendesk Authentication</h2>
      <div style={{ marginBottom: "10px" }}>
        <label>Instance URL:</label>
        <input
          type="text"
          name="instance_url"
          value={formData.instance_url}
          onChange={handleChange}
          placeholder="https://yourcompany.zendesk.com"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Admin ID:</label>
        <input
          type="text"
          name="admin_id"
          value={formData.admin_id}
          onChange={handleChange}
          placeholder="admin@example.com"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>API Token:</label>
        <input
          type="text"
          name="api_token"
          value={formData.api_token}
          onChange={handleChange}
          placeholder="Enter your API token"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      <div style={{ marginBottom: "10px" }}>
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
        {authenticated && (
          <button
            onClick={handleSave}
            style={{
              padding: "10px",
              backgroundColor: "#28a745",
              color: "#fff",
              border: "none",
              cursor: "pointer",
              width: "100%",
            }}
          >
            Save Credentials
          </button>
        )}
      </div>
      {message && <p style={{ color: authenticated ? "green" : "red" }}>{message}</p>}
    </div>
  );
};

export default ZendeskForm;
