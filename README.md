# CareCompanion

> Transform complex medical documents into simple, actionable care plans

CareCompanion is a sophisticated web application that addresses a critical accessibility gap in healthcare. Patients are often discharged with complex medical documents they cannot understand, leading to poor treatment adherence and negative health outcomes. This project implements a multi-agent AI system that processes medical document images and generates comprehensive, personalized care plans.

##  Key Features

###  Multi-Agent AI System
- **Scribe Agent**: Extracts text from medical document images using OCR
- **Translator Agent**: Explains medical terms in plain, understandable language
- **Resource Agent**: Finds cost-saving opportunities and support resources
- **Planner Agent**: Generates personalized daily care plans and checklists

###  Comprehensive Care Plans
- **Medication Management**: Detailed medication information with dosages, frequencies, and instructions
- **Medical Education**: Simplified explanations of complex medical terms
- **Action Items**: Prioritized daily tasks with clear timeframes
- **Lifestyle Tips**: Condition-specific health recommendations
- **Cost Savings**: Potential medication savings and discount program recommendations
- **Support Resources**: Links to relevant healthcare organizations and assistance programs

###  Modern User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Processing**: Live progress indicators during document analysis
- **Interactive UI**: Tabbed interface for easy navigation through care plan sections
- **Error Handling**: User-friendly error messages with recovery options
- **Accessibility**: ARIA labels, keyboard navigation, and screen reader support

##  System Architecture

### Backend (FastAPI + Python)
```
backend/
├── agents/                 # AI Agent implementations
│   ├── base_agent.py      # Base agent class
│   ├── scribe_agent.py    # Text extraction agent
│   ├── translator_agent.py # Medical term translation
│   ├── resource_agent.py  # Cost savings & resources
│   └── planner_agent.py   # Care plan generation
├── models/                 # Pydantic data models
├── services/               # Business logic services
├── utils/                  # Utility functions
├── tests/                  # Test suite
└── main.py                # FastAPI application
```

**Key Backend Features:**
- **RESTful API**: Well-documented endpoints with OpenAPI/Swagger
- **Input Validation**: Comprehensive file type, size, and content validation
- **Error Handling**: Global exception handling with detailed error responses
- **Logging**: Structured logging with configurable levels
- **Testing**: Comprehensive test suite with 80%+ coverage
- **Security**: CORS protection, input sanitization, and secure file handling

### Frontend (React + Vite)
```
frontend/src/
├── components/             # Reusable UI components
│   ├── Header.jsx         # Application header
│   ├── FileUpload.jsx     # Document upload interface
│   ├── LoadingSpinner.jsx # Processing indicators
│   ├── CarePlanDisplay.jsx # Care plan visualization
│   └── ...
├── assets/                # Static assets
├── test/                  # Test files
└── App.jsx               # Main application component
```

**Key Frontend Features:**
- **Component Architecture**: Modular, reusable, and well-tested components
- **State Management**: Efficient state handling with React hooks
- **Responsive Design**: Mobile-first approach with CSS Grid/Flexbox
- **Error Boundaries**: Graceful error handling and recovery
- **Performance**: Optimized rendering and lazy loading

##  Technology Stack

### Backend Technologies
- **FastAPI 0.104.1**: Modern, fast web framework for building APIs
- **Pydantic 2.5.0**: Data validation and settings management
- **Pillow 10.1.0**: Image processing and validation
- **Uvicorn**: ASGI server for production deployment
- **Pytest**: Testing framework with async support and coverage reporting

### Frontend Technologies
- **React 19.1.1**: Latest React with modern features and concurrent rendering
- **Vite 7.1.7**: Fast build tool and development server
- **Axios 1.12.2**: HTTP client for API communication
- **CSS3**: Modern styling with custom properties and responsive design
- **Vitest**: Fast unit testing framework with React Testing Library

### DevOps & Deployment
- **Docker**: Containerization for consistent deployment across environments
- **Docker Compose**: Multi-container orchestration and service management
- **Nginx**: Reverse proxy and static file serving for production
- **GitHub Actions**: CI/CD pipeline ready for automated testing and deployment

##  Prerequisites

Before running CareCompanion AI, ensure you have the following installed:

- **Node.js**: >= 18.0.0 (for frontend development)
- **Python**: >= 3.11 (for backend development)
- **Docker**: >= 20.0.0 (optional, for containerized deployment)
- **Git**: For version control and cloning the repository

##  Getting Started

### Option 1: Docker Compose (Recommended for Quick Start)

This is the fastest way to get CareCompanion AI running with minimal setup:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/carecompanion-ai.git
   cd carecompanion-ai
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

The Docker Compose setup includes:
- Backend API server with hot reload
- Frontend development server
- Nginx reverse proxy (optional)
- Automatic service discovery and networking

### Option 2: Local Development Setup

For development and customization, run the services locally:

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv care_companion_venv
   
   # Activate virtual environment
   # On Windows:
   care_companion_venv\Scripts\activate
   # On macOS/Linux:
   source care_companion_venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

#### Frontend Setup

1. **Open a new terminal and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

The frontend will be available at:
- **Application URL**: http://localhost:5173
- **Hot Module Replacement**: Enabled for instant updates

##  Testing the Application

### Manual Testing

1. **Upload a Medical Document**
   - Use any medical document image (prescription, discharge summary, lab results)
   - Supported formats: JPG, PNG, GIF, BMP, TIFF, WEBP
   - Maximum file size: 10MB

2. **Verify AI Agent Processing**
   - Watch the progress indicators during processing
   - Check the browser console for any errors
   - Verify all four agents complete successfully

3. **Review Generated Care Plan**
   - **Overview Tab**: Summary of medications and key action items
   - **Medications Tab**: Detailed medication information
   - **Action Plan Tab**: Prioritized tasks and follow-up instructions
   - **Health Education Tab**: Simplified medical term explanations
   - **Resources & Savings Tab**: Cost savings and support resources

### Automated Testing

#### Backend Tests
```bash
cd backend

# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py -v

# Run tests with specific markers
pytest tests/ -m "not slow" -v
```

#### Frontend Tests
```bash
cd frontend

# Run all tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run tests with coverage
npm run test:coverage

# Run tests in UI mode
npm run test:ui
```

#### Integration Tests
```bash
# From project root - run all tests with Docker
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### API Testing

#### Health Check Endpoints
```bash
# Basic health check
curl http://localhost:8000/

# Detailed health information
curl http://localhost:8000/health
```

#### Document Processing Endpoint
```bash
# Process a medical document
curl -X POST "http://localhost:8000/api/v1/process-document" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/medical/document.jpg"
```

#### Expected Response Structure
```json
{
  "status": "completed",
  "document_type": "prescription",
  "raw_text": "Extracted text from document...",
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
        "explanation": "Blood pressure medication...",
        "importance": "Essential for controlling blood pressure...",
        "category": "medication"
      }
    ],
    "action_items": [
      {
        "title": "Take Morning Medication",
        "description": "Take one tablet every morning",
        "priority": "high",
        "timeframe": "Every morning",
        "completed": false
      }
    ],
    "lifestyle_tips": [
      "Monitor your blood pressure at home once a week",
      "Maintain a low-sodium diet"
    ],
    "follow_up_instructions": [
      "Schedule a follow-up appointment in 4-6 weeks"
    ],
    "emergency_contacts": [
      "Dr. Smith: (555) 123-4567",
      "Emergency Services: 911"
    ]
  },
  "processing_time_seconds": 3.2,
  "confidence_score": 0.92,
  "error_message": null,
  "agent_results": {
    "scribe": { "status": "success", "processing_time": 1.01 },
    "translator": { "status": "success", "processing_time": 0.81 },
    "resource": { "status": "success", "processing_time": 0.73 },
    "planner": { "status": "success", "processing_time": 0.85 }
  }
}
```

##  API Documentation

### Core Endpoints

#### Health Monitoring
- **`GET /`** - Basic health check with uptime information
- **`GET /health`** - Detailed health status and system metrics

#### Document Processing
- **`POST /api/v1/process-document`** - Process medical document images

**Request Parameters:**
- `file` (multipart/form-data): Medical document image file
- Supported formats: JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP
- Maximum file size: 10MB

**Response Codes:**
- `200 OK`: Document processed successfully
- `400 Bad Request`: Invalid file format or size
- `422 Unprocessable Entity`: Missing or invalid request data
- `500 Internal Server Error`: Processing failed

### Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": "HTTP_ERROR",
  "message": "Detailed error description",
  "details": {
    "field": "Additional error context"
  },
  "timestamp": "2024-09-28T00:00:00"
}
```

##  Configuration

### Environment Variables

Create a `.env` file in the backend directory to customize the application:

```env
# Environment Configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=CareCompanion AI
VERSION=1.0.0

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# File Upload Configuration
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]

# External API Integration (Future)
GOOGLE_VISION_API_KEY=your_google_vision_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Security Configuration
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuration Options

- **`ENVIRONMENT`**: Set to `production` for production deployment
- **`DEBUG`**: Enable/disable debug mode and detailed logging
- **`LOG_LEVEL`**: Set logging level (DEBUG, INFO, WARNING, ERROR)
- **`ALLOWED_ORIGINS`**: Configure CORS allowed origins for security
- **`MAX_FILE_SIZE_MB`**: Maximum file size for uploads
- **`ALLOWED_EXTENSIONS`**: Permitted file formats for uploads

##  Deployment

### Production Deployment with Docker

1. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy with production configuration**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Verify deployment**
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

### Environment-Specific Configurations

#### Development Environment
- Hot reload enabled for both frontend and backend
- Debug logging and detailed error messages
- CORS enabled for local development
- Source maps for debugging

#### Production Environment
- Optimized builds with minification
- Security headers and HTTPS support
- Error tracking and monitoring
- Performance optimizations

### Scaling and Performance

- **Horizontal Scaling**: Deploy multiple backend instances behind a load balancer
- **Caching**: Implement Redis for session and response caching
- **CDN**: Use a Content Delivery Network for static assets
- **Database**: Add PostgreSQL for persistent data storage (future enhancement)

##  Use Cases and Applications

### Primary Use Cases

#### Caregiver Support
- **Scenario**: Adult children caring for elderly parents
- **Pain Points**: Understanding complex medical instructions and medication schedules
- **Solution**: Clear, actionable care plans with simplified explanations

#### Patient Self-Management
- **Scenario**: Patients managing chronic conditions
- **Pain Points**: Interpreting lab results and medication changes
- **Solution**: Personalized lifestyle tips and medication management

#### Healthcare Provider Support
- **Scenario**: Doctors and nurses explaining treatments to patients
- **Pain Points**: Time constraints and complex medical terminology
- **Solution**: Automated patient education materials and care instructions

### Supported Document Types

#### Prescriptions
- Medication names, dosages, and frequencies
- Refill information and pharmacy details
- Special instructions and warnings

#### Discharge Summaries
- Diagnosis and treatment information
- Follow-up instructions and appointments
- Medication changes and new prescriptions

#### Lab Results
- Blood work and diagnostic test results
- Reference ranges and normal values
- Trend analysis and recommendations

#### Medical Instructions
- Post-procedure care instructions
- Lifestyle modifications and restrictions
- Warning signs and emergency contacts

##  Security and Privacy

### Data Protection
- **No Persistent Storage**: Documents are processed in memory and not stored
- **Ephemeral Processing**: All data is cleared after processing completion
- **Secure File Handling**: Temporary files are immediately deleted after processing

### Input Validation
- **File Type Validation**: Strict checking of allowed file formats
- **File Size Limits**: Maximum file size restrictions to prevent abuse
- **Content Validation**: Image format verification and corruption detection

### Network Security
- **CORS Protection**: Configured for specific allowed origins
- **HTTPS Ready**: Production deployment supports SSL/TLS encryption
- **Error Handling**: No sensitive information exposed in error messages

### Privacy Compliance
- **HIPAA Considerations**: Designed with healthcare privacy in mind
- **No Data Collection**: No personal information is collected or stored
- **Transparent Processing**: Clear indication of what data is processed

##  Development and Testing

### Code Quality Tools

#### Backend
- **Black**: Code formatting and style consistency
- **isort**: Import statement organization
- **flake8**: Linting and code quality checks
- **mypy**: Static type checking
- **pytest**: Testing framework with coverage reporting

#### Frontend
- **ESLint**: JavaScript/React linting and code quality
- **Prettier**: Code formatting and style consistency
- **Vitest**: Fast unit testing with React Testing Library
- **TypeScript**: Optional type checking for enhanced development

### Running Code Quality Checks

```bash
# Backend code quality
cd backend
black . --check
isort . --check-only
flake8 .
mypy .

# Frontend code quality
cd frontend
npm run lint
npm run format:check
npm run type-check
```

### Testing Strategy

#### Unit Tests
- **Backend**: Test individual functions and methods
- **Frontend**: Test React components in isolation
- **Coverage Target**: 80%+ code coverage

#### Integration Tests
- **API Testing**: Test complete request/response cycles
- **Component Testing**: Test component interactions
- **End-to-End**: Test complete user workflows

#### Performance Testing
- **Load Testing**: Test under various load conditions
- **Memory Testing**: Monitor memory usage and leaks
- **Response Time**: Ensure fast processing times

##  Contributing

### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/carecompanion-ai.git
   cd carecompanion-ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend && pytest tests/ -v
   
   # Frontend tests
   cd frontend && npm run test
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure all tests pass

### Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Write clear, self-documenting code
- Add comprehensive comments for complex logic

#### Testing Requirements
- Write tests for all new functionality
- Maintain or improve test coverage
- Include both positive and negative test cases
- Test error conditions and edge cases

#### Documentation
- Update README.md for user-facing changes
- Add docstrings for new functions and classes
- Update API documentation for endpoint changes
- Include examples for new features

### Issue Reporting

When reporting issues, please include:
- **Environment**: Operating system, Python/Node.js versions
- **Steps to Reproduce**: Clear, detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Error Messages**: Complete error messages and stack traces
- **Screenshots**: If applicable, include screenshots

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- **FastAPI Team**: For the excellent web framework and documentation
- **React Team**: For the powerful UI library and development tools
- **Open Source Community**: For the various dependencies and tools used
- **Healthcare Professionals**: For insights into real-world healthcare challenges

---

**Built with ❤️ for better healthcare accessibility and patient empowerment**