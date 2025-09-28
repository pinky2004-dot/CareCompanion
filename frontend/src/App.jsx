import React, { useState, useCallback } from 'react';
import axios from 'axios';
import './App.css';

// Components
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import CarePlanDisplay from './components/CarePlanDisplay';
import Footer from './components/Footer';

// Constants
const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileSelect = useCallback((file) => {
    setSelectedFile(file);
    setError(null);
    setResult(null);
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    // Reset state for new submission
    setResult(null);
    setError(null);
    setIsLoading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const response = await axios.post(`${API_BASE_URL}/api/v1/process-document`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });

      clearInterval(progressInterval);
      setUploadProgress(100);
      
      setResult(response.data);
    } catch (err) {
      let errorMessage = "An error occurred. Please try again.";
      
      if (err.response) {
        // Server responded with error status
        const errorData = err.response.data;
        errorMessage = errorData?.message || errorData?.detail || errorMessage;
      } else if (err.request) {
        // Network error
        errorMessage = "Unable to connect to the server. Please check your connection.";
      } else {
        // Other error
        errorMessage = err.message || errorMessage;
      }
      
      setError(errorMessage);
      console.error('Upload error:', err);
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  }, [selectedFile]);

  const handleReset = useCallback(() => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setUploadProgress(0);
  }, []);

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        <div className="container">
          <section className="hero-section">
            <h1 className="hero-title">
              CareCompanion AI
            </h1>
            <p className="hero-subtitle">
              Transform complex medical documents into simple, actionable care plans
            </p>
            <p className="hero-description">
              Upload your prescription, discharge summary, or lab results to get a personalized, 
              easy-to-understand health plan with medication reminders and lifestyle tips.
            </p>
          </section>

          <section className="upload-section">
            <FileUpload
              onFileSelect={handleFileSelect}
              selectedFile={selectedFile}
              onReset={handleReset}
            />
            
            {selectedFile && (
              <div className="file-info">
                <p><strong>Selected file:</strong> {selectedFile.name}</p>
                <p><strong>Size:</strong> {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            )}

            <button 
              className="analyze-button"
              onClick={handleSubmit}
              disabled={!selectedFile || isLoading}
            >
              {isLoading ? 'Analyzing Document...' : 'Analyze Document'}
            </button>
          </section>

          {isLoading && (
            <LoadingSpinner 
              progress={uploadProgress}
              message="Processing your document with AI..."
            />
          )}

          {error && (
            <ErrorMessage 
              message={error}
              onRetry={handleSubmit}
              onReset={handleReset}
            />
          )}

          {result && (
            <CarePlanDisplay 
              data={result}
              onReset={handleReset}
            />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;