// import React, { useState } from "react";
// // import "./Styles/TicketChoose.css";

// const TicketChoose = ({ onNext }) => {
//     const [system, setSystem] = useState("");
//     const [credentials, setCredentials] = useState({ username: "", password: "" });

//     const handleNext = () => {
//         if (!system || !credentials.username || !credentials.password) {
//             alert("Please fill in all fields.");
//             return;
//         }
//         onNext(system, credentials); // Pass data to the next step
//     };

//     return (
//         <div className="TicketChoose-container">
//             <h1>Select System and Provide Credentials</h1>
//             <label>
//                 System:
//                 <select value={system} onChange={(e) => setSystem(e.target.value)}>
//                     <option value="">Select</option>
//                     <option value="ServiceNow">ServiceNow</option>
//                     <option value="Zendesk">Zendesk</option>
//                     <option value="Jira">Jira</option>
//                     <option value="Remedyforce">Remedyforce</option>
//                 </select>
//             </label>
//             <label>
//                 Username:
//                 <input
//                     type="text"
//                     value={credentials.username}
//                     onChange={(e) =>
//                         setCredentials({ ...credentials, username: e.target.value })
//                     }
//                 />
//             </label>
//             <label>
//                 Password:
//                 <input
//                     type="password"
//                     value={credentials.password}
//                     onChange={(e) =>
//                         setCredentials({ ...credentials, password: e.target.value })
//                     }
//                 />
//             </label>
//             <button onClick={handleNext}>Next</button>
//         </div>
//     );
// };

// export default TicketChoose;
