"""
Document processing service for CareCompanion AI.
"""
import asyncio
import io
import time
from typing import Tuple
from PIL import Image
from models import (
    CarePlan, 
    MedicationInfo, 
    SimplifiedTerm, 
    ActionItem, 
    DocumentType,
    ProcessingStatus
)
from agents.scribe_agent import ScribeAgent
from agents.translator_agent import TranslatorAgent
from agents.resource_agent import ResourceAgent
from agents.planner_agent import PlannerAgent


class DocumentProcessor:
    """Handles document processing and AI agent coordination."""
    
    def __init__(self):
        self.start_time = time.time()
        # Initialize AI agents
        self.scribe_agent = ScribeAgent()
        self.translator_agent = TranslatorAgent()
        self.resource_agent = ResourceAgent()
        self.planner_agent = PlannerAgent()
    
    async def process_document(self, file_content: bytes, filename: str) -> Tuple[ProcessingStatus, dict]:
        """
        Process uploaded document and return structured care plan.
        
        Args:
            file_content: Raw file content
            filename: Name of the uploaded file
            
        Returns:
            Tuple of (status, response_data)
        """
        try:
            # Validate image
            await self._validate_image(file_content)
            
            # Initialize processing pipeline data
            pipeline_data = {
                'image_content': file_content,
                'filename': filename
            }
            
            # Step 1: Scribe Agent - Extract text from image
            scribe_result = await self.scribe_agent.execute(pipeline_data)
            if scribe_result['status'] != 'success':
                raise Exception(f"Scribe agent failed: {scribe_result['error']}")
            
            pipeline_data.update(scribe_result['result'])
            
            # Step 2: Translator Agent - Explain medical terms
            translator_result = await self.translator_agent.execute(pipeline_data)
            if translator_result['status'] != 'success':
                raise Exception(f"Translator agent failed: {translator_result['error']}")
            
            pipeline_data.update(translator_result['result'])
            
            # Step 3: Resource Agent - Find cost savings and resources
            resource_result = await self.resource_agent.execute(pipeline_data)
            if resource_result['status'] != 'success':
                raise Exception(f"Resource agent failed: {resource_result['error']}")
            
            pipeline_data.update(resource_result['result'])
            
            # Step 4: Planner Agent - Generate care plan
            planner_result = await self.planner_agent.execute(pipeline_data)
            if planner_result['status'] != 'success':
                raise Exception(f"Planner agent failed: {planner_result['error']}")
            
            # Extract care plan from planner result
            care_plan_data = planner_result['result']['care_plan']
            
            processing_time = time.time() - self.start_time
            
            return ProcessingStatus.COMPLETED, {
                "status": ProcessingStatus.COMPLETED,
                "document_type": pipeline_data.get('document_type', DocumentType.UNKNOWN),
                "raw_text": pipeline_data.get('raw_text', ''),
                "care_plan": care_plan_data,
                "processing_time_seconds": processing_time,
                "confidence_score": self._calculate_confidence_score(scribe_result, translator_result, resource_result, planner_result),
                "error_message": None,
                "agent_results": {
                    "scribe": scribe_result,
                    "translator": translator_result,
                    "resource": resource_result,
                    "planner": planner_result
                }
            }
            
        except Exception as e:
            processing_time = time.time() - self.start_time
            return ProcessingStatus.FAILED, {
                "status": ProcessingStatus.FAILED,
                "document_type": DocumentType.UNKNOWN,
                "raw_text": "",
                "care_plan": CarePlan(),
                "processing_time_seconds": processing_time,
                "confidence_score": 0.0,
                "error_message": str(e)
            }
    
    async def _validate_image(self, file_content: bytes) -> None:
        """Validate uploaded image file."""
        try:
            image_stream = io.BytesIO(file_content)
            image = Image.open(image_stream)
            image.verify()
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
    
    def _calculate_confidence_score(self, scribe_result: dict, translator_result: dict, 
                                  resource_result: dict, planner_result: dict) -> float:
        """Calculate overall confidence score based on agent results."""
        # Base confidence from each agent
        scribe_confidence = scribe_result.get('result', {}).get('confidence_score', 0.8)
        translator_confidence = translator_result.get('result', {}).get('translation_confidence', 0.8)
        
        # Resource agent doesn't have confidence score, use processing success
        resource_confidence = 0.9 if resource_result['status'] == 'success' else 0.5
        
        # Planner agent doesn't have confidence score, use processing success
        planner_confidence = 0.9 if planner_result['status'] == 'success' else 0.5
        
        # Calculate weighted average
        weights = [0.3, 0.3, 0.2, 0.2]  # Scribe and Translator are most important
        confidences = [scribe_confidence, translator_confidence, resource_confidence, planner_confidence]
        
        weighted_confidence = sum(w * c for w, c in zip(weights, confidences))
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, weighted_confidence))
