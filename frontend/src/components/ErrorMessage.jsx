import React from 'react';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry, onReset }) => {
  return (
    <div className="error-container">
      <div className="error-card">
        <div className="error-icon">⚠️</div>
        <h3 className="error-title">Something went wrong</h3>
        <p className="error-message">{message}</p>
        
        <div className="error-actions">
          <button 
            className="retry-button"
            onClick={onRetry}
          >
            Try Again
          </button>
          <button 
            className="reset-button"
            onClick={onReset}
          >
            Start Over
          </button>
        </div>
        
        <div className="error-help">
          <h4>Common solutions:</h4>
          <ul>
            <li>Make sure your file is a clear image (JPG, PNG, etc.)</li>
            <li>Check that the file size is under 10MB</li>
            <li>Ensure the text in the image is readable</li>
            <li>Try a different image if the current one is blurry</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
