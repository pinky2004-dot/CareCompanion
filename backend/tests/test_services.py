"""
Tests for services.
"""
import pytest
from unittest.mock import patch, MagicMock
from services.document_processor import DocumentProcessor
from models import ProcessingStatus, DocumentType


class TestDocumentProcessor:
    """Test DocumentProcessor service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DocumentProcessor()
    
    @pytest.mark.asyncio
    async def test_process_document_success(self):
        """Test successful document processing."""
        # Mock image content
        image_content = b"fake_image_content"
        filename = "test.jpg"
        
        with patch('PIL.Image.open') as mock_image:
            mock_image.return_value.verify.return_value = None
            
            status, response = await self.processor.process_document(image_content, filename)
            
            assert status == ProcessingStatus.COMPLETED
            assert response["status"] == ProcessingStatus.COMPLETED
            assert response["document_type"] == DocumentType.PRESCRIPTION
            assert "care_plan" in response
            assert "processing_time_seconds" in response
            assert "confidence_score" in response
            assert response["error_message"] is None

    @pytest.mark.asyncio
    async def test_process_document_invalid_image(self):
        """Test processing with invalid image."""
        image_content = b"invalid_image_content"
        filename = "test.jpg"
        
        with patch('PIL.Image.open') as mock_image:
            mock_image.side_effect = Exception("Invalid image")
            
            status, response = await self.processor.process_document(image_content, filename)
            
            assert status == ProcessingStatus.FAILED
            assert response["status"] == ProcessingStatus.FAILED
            assert response["error_message"] is not None

    @pytest.mark.asyncio
    async def test_validate_image_success(self):
        """Test successful image validation."""
        image_content = b"valid_image_content"
        
        with patch('PIL.Image.open') as mock_image:
            mock_image.return_value.verify.return_value = None
            
            # Should not raise exception
            await self.processor._validate_image(image_content)

    @pytest.mark.asyncio
    async def test_validate_image_failure(self):
        """Test image validation failure."""
        image_content = b"invalid_image_content"
        
        with patch('PIL.Image.open') as mock_image:
            mock_image.side_effect = Exception("Invalid image")
            
            with pytest.raises(ValueError, match="Invalid image file"):
                await self.processor._validate_image(image_content)

    @pytest.mark.asyncio
    async def test_mock_ai_processing(self):
        """Test mock AI processing returns valid care plan."""
        care_plan = await self.processor._mock_ai_processing()
        
        assert care_plan is not None
        assert len(care_plan.medications) > 0
        assert len(care_plan.simplified_terms) > 0
        assert len(care_plan.action_items) > 0
        assert len(care_plan.lifestyle_tips) > 0
        assert len(care_plan.follow_up_instructions) > 0
        assert len(care_plan.emergency_contacts) > 0

    def test_get_mock_raw_text(self):
        """Test mock raw text generation."""
        raw_text = self.processor._get_mock_raw_text()
        
        assert isinstance(raw_text, str)
        assert len(raw_text) > 0
        assert "PHARMACY" in raw_text
        assert "LISINOPRIL" in raw_text
