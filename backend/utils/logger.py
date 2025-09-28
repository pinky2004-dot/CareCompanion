"""
Logging configuration for CareCompanion AI.
"""
import logging
import sys
from datetime import datetime
from config import settings


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("carecompanion")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level.upper()))
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Add file handler in production
    if settings.environment == "production":
        file_handler = logging.FileHandler("carecompanion.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logging()
