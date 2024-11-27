// KnowledgeBase.js
import React, { useState } from 'react';
import { Upload, FileText, Send } from 'lucide-react';
import "./Styles/KnowledgeBase.css"

const FileUploadForm = () => {
  const [department, setDepartment] = useState('IT');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const departments = [
    { value: 'IT', label: 'IT' },
    { value: 'FINANCE', label: 'Finance' },
    { value: 'HR', label: 'HR' },
    { value: 'OTHERS', label: 'Others' },
  ];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setUploadMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('department', department);

    setIsUploading(true);
    setUploadMessage('');

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setUploadMessage(result.message || 'File uploaded successfully');
        setFile(null);
        document.getElementById('fileInput').value = '';
      } else {
        setUploadMessage(result.error || 'Failed to upload the file');
      }
    } catch (error) {
      setUploadMessage(`Upload failed: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    
      <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
       <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4"> <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Document</h2>
          <p className="text-gray-600">Welcome to the document upload section</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-2">
              Select Department
            </label>
            <select
              id="department"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {departments.map((dept) => (
                <option key={dept.value} value={dept.value}>
                  {dept.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="fileInput" className="block text-sm font-medium text-gray-700 mb-2">
              Choose File
            </label>
            <div className="flex items-center">
              <input
                type="file"
                id="fileInput"
                onChange={handleFileChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              {file && <FileText className="ml-2 text-blue-500" size={24} />}
            </div>
          </div>

          {uploadMessage && (
            <div
              className={`p-3 rounded-md text-sm ${
                uploadMessage.includes('successfully')
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {uploadMessage}
            </div>
          )}

          <button
            type="submit"
            disabled={isUploading}
            className={`w-full flex items-center justify-center py-2 rounded-md text-white transition-colors ${
              isUploading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500'
            }`}
          >
            {isUploading ? (
              <>
                <span className="mr-2">Uploading...</span>
                <Upload className="animate-pulse" size={20} />
              </>
            ) : (
              <>
                <span className="mr-2">Upload</span>
                <Send size={20} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default FileUploadForm;
