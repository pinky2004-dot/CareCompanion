"""
Base agent class for all AI agents.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import asyncio
import time
from utils.logger import logger


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    async def execute(self, input_data: Any) -> Dict[str, Any]:
        """
        Execute the agent with timing and error handling.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dictionary containing processing results
        """
        self.start_time = time.time()
        logger.info(f"Starting {self.name} agent processing")
        
        try:
            result = await self.process(input_data)
            self.end_time = time.time()
            processing_time = self.end_time - self.start_time
            
            logger.info(f"{self.name} agent completed in {processing_time:.2f}s")
            
            return {
                "agent_name": self.name,
                "status": "success",
                "processing_time": processing_time,
                "result": result,
                "error": None
            }
            
        except Exception as e:
            self.end_time = time.time()
            processing_time = self.end_time - self.start_time
            
            logger.error(f"{self.name} agent failed after {processing_time:.2f}s: {str(e)}")
            
            return {
                "agent_name": self.name,
                "status": "error",
                "processing_time": processing_time,
                "result": None,
                "error": str(e)
            }
    
    def get_processing_time(self) -> float:
        """Get the processing time for this agent."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
