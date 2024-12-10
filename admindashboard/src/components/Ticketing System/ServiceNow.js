// import React, { useState } from "react";
// import "./Styles/ServiceNow.css";

// const Ticket = () => {
//     const [credentials, setCredentials] = useState({ username: "", password: "", instanceUrl: "" });
//     const [authSuccess, setAuthSuccess] = useState(false);
//     const [loading, setLoading] = useState(false);
//     const [urlError, setUrlError] = useState("");

//     const handleSubmit = () => {
//         const { instanceUrl, username, password } = credentials;

//         if (!instanceUrl || !username || !password) {
//             setUrlError("Please provide all required fields.");
//             return;
//         }

//         const urlRegex = /^(https?:\/\/)?([\w\d\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
//         if (!urlRegex.test(instanceUrl)) {
//             setUrlError("Please enter a valid URL.");
//             return;
//         }

//         setLoading(true);
//         setUrlError(""); // Clear error if URL is valid

//         fetch("http://127.0.0.1:5001/authenticate", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ instanceUrl, username, password }),
//         })
//             .then((res) => res.json())
//             .then((data) => {
//                 setLoading(false);
//                 if (data.success) {
//                     localStorage.setItem("auth_token", data.token);
//                     alert("Authentication successful!");
//                     setAuthSuccess(true);
//                 } else {
//                     alert(data.message);
//                 }
//             })
//             .catch(() => {
//                 setLoading(false);
//                 alert("Authentication failed due to a server error. Please try again.");
//             });
//     };

//     const handleSave = () => {
//         const { instanceUrl } = credentials;

//         fetch("http://127.0.0.1:5001/save", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
//             },
//             body: JSON.stringify({
//                 system: "ServiceNow",
//                 instance_url: instanceUrl,
//                 password: credentials.password, // Use the same password
//             }),
//         })
//             .then((res) => res.json())
//             .then((data) => {
//                 if (data.success) {
//                     alert("Data saved successfully!");
//                 } else {
//                     alert(data.message);
//                 }
//             })
//             .catch(() => alert("Error connecting to the server."));
//     };

//     return (
//         <div className="ticket-container">
//             <h1>ServiceNow Admin Portal</h1>
//             <div className="credentials-step">
//                 <label>
//                     Instance URL:
//                     <input
//                         type="text"
//                         value={credentials.instanceUrl}
//                         onChange={(e) =>
//                             setCredentials({ ...credentials, instanceUrl: e.target.value })
//                         }
//                     />
//                 </label>
//                 <label>
//                     Username:
//                     <input
//                         type="text"
//                         value={credentials.username}
//                         onChange={(e) =>
//                             setCredentials({ ...credentials, username: e.target.value })
//                         }
//                     />
//                 </label>
//                 <label>
//                     Password:
//                     <input
//                         type="password"
//                         value={credentials.password}
//                         onChange={(e) =>
//                             setCredentials({ ...credentials, password: e.target.value })
//                         }
//                     />
//                 </label>
//                 {urlError && <div className="error-message">{urlError}</div>}
//                 {loading ? (
//                     <div className="spinner">Authenticating...</div>
//                 ) : (
//                     <button onClick={handleSubmit}>Authenticate</button>
//                 )}
//             </div>

//             {authSuccess && (
//                 <div className="save-step">
//                     <button onClick={handleSave}>Save Data</button>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default Ticket;


import React, { useState } from "react";
import axios from "axios";

const Ticket = () => {
  const [credentials, setCredentials] = useState({ username: "", password: "", instanceUrl: "" });
  const [authSuccess, setAuthSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [urlError, setUrlError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({ ...credentials, [name]: value });
  };

  const handleAuthenticate = async () => {
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

    try {
      const response = await axios.post("http://127.0.0.1:5106/authenticate", {
        instance_url: instanceUrl,
        username: username,
        password: password,
      });

      if (response.data.success) {
        setMessage("Authenticated successfully!");
        setAuthSuccess(true);
      } else {
        setMessage(`Authentication failed: ${response.data.message}`);
        setAuthSuccess(false);
      }
    } catch (error) {
      setMessage("An error occurred while authenticating.");
      console.error(error);
      setAuthSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    const { instanceUrl, username, password } = credentials;

    try {
      const response = await axios.post("http://127.0.0.1:5106/save", {
        instance_url: instanceUrl,
        email: username,
        password: password,
      });

      if (response.data.success) {
        setMessage("Data saved successfully!");
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
      <h2>ServiceNow Authentication</h2>
      <div style={{ marginBottom: "10px" }}>
        <label>Instance URL:</label>
        <input
          type="text"
          name="instanceUrl"
          value={credentials.instanceUrl}
          onChange={handleChange}
          placeholder="https://yourcompany.service-now.com"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Username (Email):</label>
        <input
          type="text"
          name="username"
          value={credentials.username}
          onChange={handleChange}
          placeholder="admin@example.com"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      <div style={{ marginBottom: "10px" }}>
        <label>Password:</label>
        <input
          type="password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          placeholder="Enter your password"
          style={{ width: "100%", padding: "8px", marginBottom: "8px" }}
        />
      </div>
      {urlError && <div style={{ color: "red", marginBottom: "10px" }}>{urlError}</div>}
      {loading ? (
        <div style={{ textAlign: "center", marginBottom: "10px" }}>Authenticating...</div>
      ) : (
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
      )}
      {authSuccess && (
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
          Save Data
        </button>
      )}
      {message && <p style={{ color: authSuccess ? "green" : "red", textAlign: "center" }}>{message}</p>}
    </div>
  );
};

export default Ticket;
