# Use Python 3.9 slim image as base
# Provides a lightweight foundation with essential Python tools
FROM python:3.9-slim

# Set working directory for the application
# All commands will execute from this location inside the container
WORKDIR /app

# Install system dependencies required for compiling Python packages  
# gcc, g++: C/C++ compilers needed for packages like scikit-learn
# python3-dev: Python development headers needed for compilation
# build-essential: Essential build tools and libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file before other code for better caching
# Docker can reuse this layer if dependencies haven't changed
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing pip cache
# --upgrade ensures latest compatible versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code into the container
# This includes main.py and any supporting Python files
COPY . .

# Expose port 8003 for the FastAPI service
# This documents which port the container uses
EXPOSE 8003

# Define the command to start the service when container runs
# uvicorn is the ASGI server that hosts our FastAPI application
# --host 0.0.0.0 allows connections from outside the container
# --port 8003 binds to the exposed port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
