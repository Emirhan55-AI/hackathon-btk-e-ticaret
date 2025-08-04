# Dockerfile for Aura Service Orchestration Engine - Phase 7
# Containerized deployment for advanced multi-service workflow orchestration

# Use Python 3.11 slim image for optimal performance
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies for networking and performance
RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash orchestrator && \
    chown -R orchestrator:orchestrator /app
USER orchestrator

# Expose port for orchestration service
EXPOSE 8006

# Health check to ensure service is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8006/ || exit 1

# Command to run the orchestration service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--workers", "1"]
