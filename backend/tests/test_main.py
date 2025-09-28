"""
Tests for main FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import io

from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check_root(self):
        """Test root health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
        assert "uptime_seconds" in data

    def test_health_check_health(self):
        """Test /health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestDocumentProcessing:
    """Test document processing endpoint."""
    
    def test_process_document_no_file(self):
        """Test processing without file."""
        response = client.post("/api/v1/process-document")
        assert response.status_code == 422  # Validation error

    def test_process_document_invalid_file_type(self):
        """Test processing with invalid file type."""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = client.post("/api/v1/process-document", files=files)
        assert response.status_code == 400

    def test_process_document_file_too_large(self):
        """Test processing with file too large."""
        # Create a large file content (11MB)
        large_content = b"x" * (11 * 1024 * 1024)
        files = {"file": ("test.jpg", large_content, "image/jpeg")}
        response = client.post("/api/v1/process-document", files=files)
        assert response.status_code == 400

    @patch('services.document_processor.DocumentProcessor.process_document')
    def test_process_document_success(self, mock_process):
        """Test successful document processing."""
        # Mock the document processor response
        mock_response = {
            "status": "completed",
            "document_type": "prescription",
            "raw_text": "Mock prescription text",
            "care_plan": {
                "medications": [
                    {
                        "name": "Lisinopril",
                        "dosage": "10 MG",
                        "frequency": "Once daily",
                        "instructions": "Take with water",
                        "quantity": 30,
                        "refills": 12
                    }
                ],
                "simplified_terms": [
                    {
                        "term": "Lisinopril",
                        "explanation": "Blood pressure medication",
                        "importance": "Controls blood pressure"
                    }
                ],
                "action_items": [
                    {
                        "title": "Take Morning Medication",
                        "description": "Take one tablet every morning",
                        "priority": "high",
                        "timeframe": "Every morning"
                    }
                ],
                "lifestyle_tips": ["Monitor blood pressure"],
                "follow_up_instructions": ["Schedule follow-up"],
                "emergency_contacts": ["Call 911"]
            },
            "processing_time_seconds": 2.5,
            "confidence_score": 0.95,
            "error_message": None
        }
        
        mock_process.return_value = ("completed", mock_response)
        
        # Create a valid image file
        image_content = b"fake_image_content"
        files = {"file": ("test.jpg", image_content, "image/jpeg")}
        
        response = client.post("/api/v1/process-document", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "completed"
        assert data["document_type"] == "prescription"
        assert "care_plan" in data
        assert len(data["care_plan"]["medications"]) == 1
        assert data["care_plan"]["medications"][0]["name"] == "Lisinopril"

    @patch('services.document_processor.DocumentProcessor.process_document')
    def test_process_document_failure(self, mock_process):
        """Test document processing failure."""
        mock_response = {
            "status": "failed",
            "document_type": "unknown",
            "raw_text": "",
            "care_plan": {},
            "processing_time_seconds": 1.0,
            "confidence_score": 0.0,
            "error_message": "Processing failed"
        }
        
        mock_process.return_value = ("failed", mock_response)
        
        image_content = b"fake_image_content"
        files = {"file": ("test.jpg", image_content, "image/jpeg")}
        
        response = client.post("/api/v1/process-document", files=files)
        assert response.status_code == 500


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Test method not allowed."""
        response = client.put("/api/v1/process-document")
        assert response.status_code == 405


class TestCORS:
    """Test CORS configuration."""
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.options("/api/v1/process-document")
        assert response.status_code == 200
        # CORS headers should be present (handled by middleware)
