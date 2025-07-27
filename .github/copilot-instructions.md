<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Aura AI System - GitHub Copilot Instructions

## Project Overview
This is the "Aura" personal style assistant AI system built using microservices architecture. The system consists of 5 independent services that communicate via REST APIs to provide clothing analysis, style profiling, and personalized recommendations.

## Code Style and Comments Requirements
- **Every single line of code must have comprehensive explanatory comments**
- Use plain English that non-technical people (managers, juries) can understand
- Explain WHAT the code does, HOW it works, and WHY it's written that way
- Example: Instead of `app = FastAPI()`, write `# Create the main FastAPI application instance. This object handles all the API routes and requests for this service.`

## Architecture Principles
1. **Microservices**: Each service is independent and handles a specific function
2. **Flow Engineering**: Services work together in orchestrated workflows
3. **Compound AI System**: Multiple AI models working together
4. **Test-Driven Development**: Every feature must have comprehensive tests

## Services and Their Functions
1. **ImageProcessingService** (Port 8001): Computer vision for clothing analysis
2. **NLUService** (Port 8002): Natural language understanding for user requests  
3. **StyleProfileService** (Port 8003): User style profile management
4. **CombinationEngineService** (Port 8004): Clothing combination generation
5. **RecommendationEngineService** (Port 8005): Product recommendations

## Technology Stack
- **Framework**: FastAPI for all services
- **Containerization**: Docker for each service
- **Testing**: pytest with comprehensive test coverage
- **AI Models**: Detectron2, CLIP, XLM-R, FAISS (to be implemented in later phases)
- **Languages**: Python with extensive English comments

## Development Phases
- **Phase 1** (Current): Basic microservice skeleton with placeholder logic
- **Phase 2**: Image processing with Detectron2 and CLIP
- **Phase 3**: NLU with XLM-R transformer model
- **Phase 4**: Advanced style profiling
- **Phase 5**: AI-powered combination generation
- **Phase 6**: FAISS-based recommendation engine
- **Phase 7**: Service orchestration and workflow
- **Phase 8**: Feedback loop implementation

## Code Generation Guidelines
When generating code for this project:
1. Always include extensive line-by-line comments
2. Use modern, industry-standard, open-source technologies
3. Ensure all services follow the same FastAPI pattern
4. Include proper error handling and validation
5. Write comprehensive tests for all functionality
6. Follow the established file structure and naming conventions

## API Patterns
All services follow this pattern:
- Health check endpoint: `GET /`
- Main functionality endpoints with descriptive names
- Pydantic models for request/response validation
- Comprehensive error handling with appropriate HTTP status codes
- Detailed response messages with processing information



Her zaman terminalde powershell syntax kullanarak çalıştır