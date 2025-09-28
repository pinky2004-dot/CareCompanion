import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ progress, message }) => {
  return (
    <div className="loading-container">
      <div className="loading-card">
        <div className="spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </div>
        
        <h3 className="loading-title">Processing Document</h3>
        <p className="loading-message">{message}</p>
        
        <div className="progress-container">
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className="progress-text">{progress}%</span>
        </div>
        
        <div className="loading-steps">
          <div className="step active">
            <div className="step-icon">🔍</div>
            <span>Extracting text</span>
          </div>
          <div className="step active">
            <div className="step-icon">🧠</div>
            <span>AI analysis</span>
          </div>
          <div className="step">
            <div className="step-icon">📋</div>
            <span>Generating plan</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
