"""
Tests for utility functions.
"""
import pytest
from fastapi import HTTPException
from utils.validators import validate_file_extension, validate_file_size, validate_content_type


class TestValidators:
    """Test validation utilities."""
    
    def test_validate_file_extension_valid(self):
        """Test valid file extension validation."""
        # Should not raise exception
        validate_file_extension("test.jpg")
        validate_file_extension("test.png")
        validate_file_extension("test.jpeg")

    def test_validate_file_extension_invalid(self):
        """Test invalid file extension validation."""
        with pytest.raises(HTTPException) as exc_info:
            validate_file_extension("test.txt")
        assert exc_info.value.status_code == 400
        assert "not allowed" in exc_info.value.detail

    def test_validate_file_extension_no_filename(self):
        """Test validation with no filename."""
        with pytest.raises(HTTPException) as exc_info:
            validate_file_extension("")
        assert exc_info.value.status_code == 400
        assert "No filename provided" in exc_info.value.detail

    def test_validate_file_size_valid(self):
        """Test valid file size validation."""
        # Should not raise exception for 5MB file
        validate_file_size(5 * 1024 * 1024)

    def test_validate_file_size_too_large(self):
        """Test file size validation with too large file."""
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(11 * 1024 * 1024)  # 11MB
        assert exc_info.value.status_code == 400
        assert "too large" in exc_info.value.detail

    def test_validate_content_type_valid(self):
        """Test valid content type validation."""
        # Should not raise exception
        validate_content_type("image/jpeg")
        validate_content_type("image/png")
        validate_content_type("image/gif")

    def test_validate_content_type_invalid(self):
        """Test invalid content type validation."""
        with pytest.raises(HTTPException) as exc_info:
            validate_content_type("text/plain")
        assert exc_info.value.status_code == 400
        assert "not allowed" in exc_info.value.detail
