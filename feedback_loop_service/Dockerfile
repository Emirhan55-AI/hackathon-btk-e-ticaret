# Phase 8: Feedback Loop Service Dockerfile
# Container configuration for intelligent feedback processing and learning system
# Optimized for machine learning workloads and real-time processing

# Use Python 3.11 slim image for optimal performance and security
FROM python:3.11-slim

# Set metadata labels for container identification and management
LABEL service="aura-feedback-loop-service"
LABEL phase="8"
LABEL description="Advanced intelligent feedback processing and system learning"
LABEL version="8.0.0"
LABEL maintainer="Aura AI Development Team"

# Set environment variables for Python optimization and service configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV FEEDBACK_SERVICE_PORT=8007
ENV FEEDBACK_DB_PATH=/app/data/feedback.db
ENV PYTHON_PATH=/app

# Create application directory and data directory for persistent storage
WORKDIR /app
RUN mkdir -p /app/data && \
    mkdir -p /app/logs && \
    mkdir -p /app/models

# Create non-root user for security best practices
# This prevents potential security issues from running as root
RUN groupadd -r aura && \
    useradd -r -g aura -d /app -s /sbin/nologin aura

# Install system dependencies required for machine learning and data processing
# These packages are needed for scientific computing and ML libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements file first for better Docker layer caching
# This allows pip install to be cached if requirements don't change
COPY requirements.txt .

# Install Python dependencies with optimization flags
# Use specific pip options for faster, more reliable installs in containers
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
# Copy all necessary files for the feedback loop service
COPY advanced_feedback_processor.py .
COPY main.py .
COPY phase8_demo.py .
COPY test_phase8_feedback.py .

# Copy any additional configuration files if they exist
COPY *.md ./docs/ 2>/dev/null || true

# Set proper ownership of application files
# Ensure the aura user owns all application files
RUN chown -R aura:aura /app

# Switch to non-root user for security
USER aura

# Create health check script for container orchestration
# This allows container platforms to monitor service health
RUN echo '#!/bin/bash\ncurl -f http://localhost:${FEEDBACK_SERVICE_PORT}/ || exit 1' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Configure container health check
# Kubernetes and Docker can use this to determine if the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${FEEDBACK_SERVICE_PORT}/health || exit 1

# Expose the service port for external access
# This documents which port the service uses and allows port mapping
EXPOSE ${FEEDBACK_SERVICE_PORT}

# Set up volume for persistent data storage
# This allows feedback data and models to persist across container restarts
VOLUME ["/app/data", "/app/logs", "/app/models"]

# Define the default command to run the feedback loop service
# Uses uvicorn with production-ready settings for FastAPI
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8007", \
     "--workers", "1", \
     "--log-level", "info", \
     "--access-log", \
     "--use-colors", \
     "--loop", "asyncio"]

# Alternative command options for different deployment scenarios:
# Development mode with auto-reload:
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007", "--reload"]
# 
# Production mode with multiple workers:
# CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8007"]
# 
# Debug mode for troubleshooting:
# CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007", "--log-level", "debug"]

# Build instructions:
# docker build -t aura-feedback-loop-service:8.0.0 .
# 
# Run instructions:
# docker run -d \
#   --name aura-feedback-loop \
#   -p 8007:8007 \
#   -v feedback_data:/app/data \
#   -v feedback_logs:/app/logs \
#   -v feedback_models:/app/models \
#   --restart unless-stopped \
#   aura-feedback-loop-service:8.0.0
# 
# Development run with live code updates:
# docker run -d \
#   --name aura-feedback-loop-dev \
#   -p 8007:8007 \
#   -v $(pwd):/app \
#   -v feedback_data:/app/data \
#   --restart unless-stopped \
#   aura-feedback-loop-service:8.0.0 \
#   uvicorn main:app --host 0.0.0.0 --port 8007 --reload
