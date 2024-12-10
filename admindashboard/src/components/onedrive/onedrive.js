// onedrive.js
import React, { useState } from 'react';
import axios from 'axios';
import '../Styles/KnowledgeBase.css';

const FileUploadForm = () => {
  const [fileName, setFileName] = useState('');
  const [department, setDepartment] = useState('IT');
  const [message, setMessage] = useState('');

  const handleFileDownload = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5001/download-file', {
        file_name: fileName,
        department,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Something went wrong.');
    }
  };

  return (
    <div>
      <h2>Download File</h2>
      <input
        type="text"
        placeholder="Enter file name"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
      />
      <select value={department} onChange={(e) => setDepartment(e.target.value)}>
        <option value="IT">IT</option>
        <option value="FINANCE">Finance</option>
        <option value="HR">HR</option>
        <option value="OTHERS">Others</option>
      </select>
      <button onClick={handleFileDownload}>Download and Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUploadForm;
