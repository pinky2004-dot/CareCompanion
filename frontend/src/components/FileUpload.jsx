import React, { useRef, useCallback } from 'react';
import './FileUpload.css';

const FileUpload = ({ onFileSelect, selectedFile, onReset }) => {
  const fileInputRef = useRef(null);

  const handleFileChange = useCallback((event) => {
    const file = event.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleReset = useCallback((event) => {
    event.stopPropagation();
    onReset();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [onReset]);

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${selectedFile ? 'has-file' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="file-input"
        />
        
        {selectedFile ? (
          <div className="file-selected">
            <div className="file-icon">📄</div>
            <div className="file-details">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <button 
              className="remove-file-btn"
              onClick={handleReset}
              type="button"
            >
              ✕
            </button>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">📁</div>
            <h3>Upload Medical Document</h3>
            <p>Drag and drop your image here, or click to browse</p>
            <p className="supported-formats">
              Supports: JPG, PNG, GIF, BMP, TIFF, WEBP
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
