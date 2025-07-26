# Phase 6: Enhanced Recommendation Engine Service Dockerfile
# This Dockerfile creates a containerized environment for the FAISS-enhanced recommendation service
# Includes all AI dependencies: FAISS, PyTorch, transformers, CLIP, scikit-learn

# Use Python 3.11 for better performance and compatibility with AI libraries
FROM python:3.11-slim

# Set the working directory inside the container to /app
# This is where all application files will be stored and executed
WORKDIR /app

# Install system dependencies required for AI libraries
# gcc and g++ are needed for compiling some Python packages
# libgomp1 is required for OpenMP support in scientific libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
# This file contains all Python dependencies including FAISS and AI libraries
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir prevents pip from storing cache, reducing image size
# --upgrade ensures we get the latest compatible versions
# --timeout increases timeout for large AI library downloads
RUN pip install --no-cache-dir --upgrade --timeout 300 -r requirements.txt

# Copy the enhanced application files to the container
# This includes the main FastAPI service and enhanced recommendation engine
COPY main.py .
COPY enhanced_recommender.py .

# Copy test files for development and debugging
COPY test_phase6_recommendations.py .

# Expose port 8005 to allow external connections to the service
# This is the port on which the enhanced recommendation service will listen
EXPOSE 8005

# Set environment variables for optimal AI library performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OMP_NUM_THREADS=1

# Set the command to run when the container starts
# This starts the FastAPI server using uvicorn with optimal configuration for AI workloads
# --host 0.0.0.0 allows connections from any IP address (necessary for containers)
# --port 8005 specifies the port to listen on
# --workers 1 ensures single worker for AI model consistency
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]
