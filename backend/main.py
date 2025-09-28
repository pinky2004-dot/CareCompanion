"""
CareCompanion AI - Main FastAPI application.
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from config import settings
from models import (
    DocumentProcessingResponse, 
    HealthCheckResponse, 
    ErrorResponse,
    ProcessingStatus
)
from services.document_processor import DocumentProcessor
from utils.validators import validate_file_extension, validate_file_size, validate_content_type
from utils.logger import logger

# Global variables
start_time = time.time()
document_processor = DocumentProcessor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting CareCompanion AI backend...")
    yield
    # Shutdown
    logger.info("Shutting down CareCompanion AI backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="AI-powered medical document processing and care plan generation",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP_ERROR",
            message=exc.detail,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_ERROR",
            message="An unexpected error occurred",
            details={"error": str(exc)},
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        ).model_dump()
    )


@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    uptime = time.time() - start_time
    return HealthCheckResponse(
        status="healthy",
        version=settings.version,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        uptime_seconds=uptime
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health():
    """Detailed health check endpoint."""
    return await health_check()


@app.post("/api/v1/process-document", response_model=DocumentProcessingResponse)
async def process_document(file: UploadFile = File(...)):
    """
    Process uploaded medical document and generate care plan.
    
    Args:
        file: Uploaded image file containing medical document
        
    Returns:
        DocumentProcessingResponse with extracted text and care plan
    """
    logger.info(f"Processing document: {file.filename}")
    
    try:
        # Validate file
        validate_file_extension(file.filename)
        validate_content_type(file.content_type)
        
        # Read file content
        content = await file.read()
        validate_file_size(len(content))
        
        # Process document
        status, response_data = await document_processor.process_document(
            content, file.filename
        )
        
        if status == ProcessingStatus.FAILED:
            logger.error(f"Document processing failed: {response_data.get('error_message')}")
            raise HTTPException(
                status_code=500,
                detail=f"Document processing failed: {response_data.get('error_message')}"
            )
        
        logger.info(f"Document processed successfully in {response_data['processing_time_seconds']:.2f}s")
        return DocumentProcessingResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.project_name,
        version=settings.version,
        description="AI-powered medical document processing and care plan generation",
        routes=app.routes,
    )
    
    # Add custom tags
    openapi_schema["tags"] = [
        {
            "name": "Health",
            "description": "Health check endpoints"
        },
        {
            "name": "Document Processing",
            "description": "Medical document processing and care plan generation"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )