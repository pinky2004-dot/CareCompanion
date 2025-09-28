"""
Scribe Agent - Extracts text from medical document images using OCR.
"""
import asyncio
import io
from typing import Dict, Any
from PIL import Image
from agents.base_agent import BaseAgent
from utils.logger import logger


class ScribeAgent(BaseAgent):
    """Agent responsible for extracting text from medical document images."""
    
    def __init__(self):
        super().__init__("Scribe")
        self.supported_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract text from medical document image.
        
        Args:
            input_data: Dictionary containing 'image_content' and 'filename'
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        image_content = input_data.get('image_content')
        filename = input_data.get('filename', 'unknown')
        
        if not image_content:
            raise ValueError("No image content provided")
        
        logger.info(f"Extracting text from {filename}")
        
        # For now, we'll use mock OCR since Google Vision API is not available
        # In production, this would integrate with Google Vision API
        extracted_text = await self._mock_ocr_extraction(image_content, filename)
        
        # Basic text cleaning and validation
        cleaned_text = self._clean_extracted_text(extracted_text)
        
        # Detect document type based on content
        document_type = self._detect_document_type(cleaned_text)
        
        return {
            "raw_text": cleaned_text,
            "document_type": document_type,
            "confidence_score": 0.95,  # Mock confidence score
            "extraction_metadata": {
                "filename": filename,
                "file_size": len(image_content),
                "text_length": len(cleaned_text),
                "processing_method": "mock_ocr"
            }
        }
    
    async def _mock_ocr_extraction(self, image_content: bytes, filename: str) -> str:
        """
        Mock OCR extraction - simulates Google Vision API.
        
        In production, this would be replaced with actual Google Vision API calls.
        """
        # Simulate processing delay
        await asyncio.sleep(1.0)
        
        # Validate image
        try:
            image_stream = io.BytesIO(image_content)
            image = Image.open(image_stream)
            image.verify()
        except Exception as e:
            logger.warning(f"Image validation failed: {e}")
        
        # Return mock extracted text based on filename or content
        if 'prescription' in filename.lower():
            return self._get_mock_prescription_text()
        elif 'discharge' in filename.lower():
            return self._get_mock_discharge_text()
        elif 'lab' in filename.lower():
            return self._get_mock_lab_text()
        else:
            return self._get_mock_prescription_text()  # Default to prescription
    
    def _get_mock_prescription_text(self) -> str:
        """Return mock prescription text."""
        return """YOUR PHARMACY
123 Healthy Street
City, State 12345
Phone: (555) 123-4567

Rx# 1234567-90
Date: 09/27/2024

Patient: JOHN DOE
DOB: 01/15/1950
Address: 456 Main St, City, State 12345

PRESCRIPTION

LISINOPRIL 10 MG TABLET
TAKE 1 TABLET BY MOUTH EVERY DAY
QTY: 30 TABLETS
REFILLS: 12

Dr. Bob Smith, MD
License: MD123456
DEA: BS1234567

Pharmacy Notes:
- Take with food if stomach upset occurs
- Monitor blood pressure regularly
- Contact doctor if side effects persist
"""
    
    def _get_mock_discharge_text(self) -> str:
        """Return mock discharge summary text."""
        return """DISCHARGE SUMMARY

Patient: JOHN DOE
DOB: 01/15/1950
Admission Date: 09/25/2024
Discharge Date: 09/27/2024
Attending Physician: Dr. Bob Smith, MD

DIAGNOSIS:
- Hypertension (I10)
- Type 2 Diabetes (E11.9)

DISCHARGE MEDICATIONS:
1. Lisinopril 10mg daily
2. Metformin 500mg twice daily
3. Atorvastatin 20mg daily

FOLLOW-UP INSTRUCTIONS:
- Follow up with Dr. Smith in 2 weeks
- Monitor blood pressure daily
- Check blood sugar levels
- Continue low-sodium diet
- Exercise 30 minutes daily

EMERGENCY CONTACTS:
- Dr. Smith: (555) 123-4567
- Emergency: 911
"""
    
    def _get_mock_lab_text(self) -> str:
        """Return mock lab results text."""
        return """LABORATORY RESULTS

Patient: JOHN DOE
DOB: 01/15/1950
Collection Date: 09/26/2024
Report Date: 09/27/2024

COMPREHENSIVE METABOLIC PANEL:
Glucose: 145 mg/dL (High)
Creatinine: 1.2 mg/dL (Normal)
BUN: 18 mg/dL (Normal)
Sodium: 140 mEq/L (Normal)
Potassium: 4.2 mEq/L (Normal)

LIPID PANEL:
Total Cholesterol: 220 mg/dL (High)
HDL: 45 mg/dL (Normal)
LDL: 150 mg/dL (High)
Triglycerides: 180 mg/dL (High)

HEMOGLOBIN A1C: 7.8% (High)

REFERENCE RANGES:
Glucose: 70-100 mg/dL
Cholesterol: <200 mg/dL
LDL: <100 mg/dL
A1C: <7.0%
"""
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(lines)
        
        # Basic text normalization
        cleaned_text = cleaned_text.replace('\t', ' ')
        cleaned_text = ' '.join(cleaned_text.split())  # Normalize spaces
        
        return cleaned_text
    
    def _detect_document_type(self, text: str) -> str:
        """Detect document type based on content."""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['rx#', 'prescription', 'pharmacy', 'refills']):
            return 'prescription'
        elif any(keyword in text_lower for keyword in ['discharge', 'admission', 'follow-up']):
            return 'discharge_summary'
        elif any(keyword in text_lower for keyword in ['lab', 'glucose', 'cholesterol', 'reference ranges']):
            return 'lab_results'
        else:
            return 'unknown'
