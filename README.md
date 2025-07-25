# Aura Backend API

AI-powered Personal Style Assistant backend service built with FastAPI, Clean Architecture, and PostgreSQL.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Update the `.env` file with your settings
4. Start the services:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   alembic upgrade head
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🏗️ Architecture

This project follows **Clean Architecture** with a **Feature-First** approach:

- **Domain Layer**: Business entities and rules
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: External concerns (database, APIs)
- **Presentation Layer**: API endpoints and request/response handling

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/              # Shared utilities, config, DI
│   ├── features/          # Feature modules
│   │   ├── auth/          # Authentication
│   │   ├── style_quiz/    # Style DNA quiz
│   │   ├── wardrobe/      # Wardrobe management
│   │   ├── recommendations/ # Outfit recommendations
│   │   └── ecommerce/     # E-commerce integration
│   └── alembic/           # Database migrations
├── tests/                 # Test suite
├── docker-compose.yml     # Docker services
├── Dockerfile            # API container
└── requirements.txt      # Python dependencies
```

## 🧪 Testing

Run tests with:
```bash
pytest
```

## 📊 Database

The application uses PostgreSQL with SQLAlchemy 2.0 and Alembic for migrations.

## 🔐 Authentication

JWT-based authentication with HttpOnly cookies for security.

## 🤖 AI Integration

Integrates with external AI service for clothing item tagging and analysis.

## 📝 API Documentation

Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).
