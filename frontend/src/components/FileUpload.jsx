import { useState, useRef } from 'react';
import axios from 'axios';
import './FileUpload.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
      setMessage('');
    } else {
      setFile(null);
      setError('Please select a valid PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setMessage('');
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage(response.data.message || 'File uploaded successfully!');
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <h3 className="file-upload-title">Upload New Policy (PDF)</h3>
      <div className="file-upload-input-group">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          ref={fileInputRef}
          className="file-input"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="file-label">
          {file ? file.name : 'Choose a PDF file'}
        </label>
        <button 
          onClick={handleUpload} 
          disabled={!file || loading}
          className={`upload-button ${!file || loading ? 'disabled' : ''}`}
        >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}
