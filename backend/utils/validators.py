"""
Validation utilities for CareCompanion AI.
"""
import os
from typing import List
from fastapi import HTTPException
from config import settings


def validate_file_extension(filename: str) -> None:
    """
    Validate file extension against allowed extensions.
    
    Args:
        filename: Name of the file to validate
        
    Raises:
        HTTPException: If file extension is not allowed
    """
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_extension = filename.lower().split('.')[-1]
    if file_extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_extension}' not allowed. Allowed types: {', '.join(settings.allowed_extensions)}"
        )


def validate_file_size(file_size: int) -> None:
    """
    Validate file size against maximum allowed size.
    
    Args:
        file_size: Size of the file in bytes
        
    Raises:
        HTTPException: If file size exceeds maximum
    """
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )


def validate_content_type(content_type: str) -> None:
    """
    Validate content type against allowed image types.
    
    Args:
        content_type: MIME type of the file
        
    Raises:
        HTTPException: If content type is not allowed
    """
    allowed_types = [
        "image/jpeg",
        "image/jpg", 
        "image/png",
        "image/gif",
        "image/bmp",
        "image/tiff",
        "image/webp"
    ]
    
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Content type '{content_type}' not allowed. Allowed types: {', '.join(allowed_types)}"
        )
