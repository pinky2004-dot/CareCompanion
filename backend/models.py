"""
Pydantic models for CareCompanion AI.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ProcessingStatus(str, Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(str, Enum):
    """Document type enumeration."""
    PRESCRIPTION = "prescription"
    DISCHARGE_SUMMARY = "discharge_summary"
    LAB_RESULTS = "lab_results"
    UNKNOWN = "unknown"


class MedicationInfo(BaseModel):
    """Medication information model."""
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Dosage information")
    frequency: str = Field(..., description="How often to take the medication")
    instructions: str = Field(..., description="Additional instructions")
    quantity: Optional[int] = Field(None, description="Quantity prescribed")
    refills: Optional[int] = Field(None, description="Number of refills")


class SimplifiedTerm(BaseModel):
    """Simplified medical term explanation."""
    term: str = Field(..., description="The medical term")
    explanation: str = Field(..., description="Simple explanation of the term")
    importance: str = Field(..., description="Why this is important for the patient")


class ActionItem(BaseModel):
    """Individual action item in the care plan."""
    title: str = Field(..., description="Title of the action")
    description: str = Field(..., description="Detailed description")
    priority: str = Field(..., description="Priority level (high, medium, low)")
    timeframe: str = Field(..., description="When to perform this action")
    completed: bool = Field(False, description="Whether the action is completed")


class CarePlan(BaseModel):
    """Complete care plan model."""
    medications: List[MedicationInfo] = Field(default_factory=list)
    simplified_terms: List[SimplifiedTerm] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    lifestyle_tips: List[str] = Field(default_factory=list)
    follow_up_instructions: List[str] = Field(default_factory=list)
    emergency_contacts: List[str] = Field(default_factory=list)


class DocumentProcessingRequest(BaseModel):
    """Request model for document processing."""
    file_name: str = Field(..., description="Name of the uploaded file")
    file_size: int = Field(..., description="Size of the file in bytes")
    content_type: str = Field(..., description="MIME type of the file")
    
    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v):
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError(f"File size too large. Maximum allowed: {max_size} bytes")
        return v


class DocumentProcessingResponse(BaseModel):
    """Response model for document processing."""
    status: ProcessingStatus = Field(..., description="Processing status")
    document_type: DocumentType = Field(..., description="Type of document detected")
    raw_text: str = Field(..., description="Extracted text from the document")
    care_plan: CarePlan = Field(..., description="Generated care plan")
    processing_time_seconds: float = Field(..., description="Time taken to process")
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")
