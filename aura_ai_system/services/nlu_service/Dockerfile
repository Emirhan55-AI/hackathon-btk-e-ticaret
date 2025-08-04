# Use Python 3.9 slim image as the base
# Slim images provide a good balance between size and functionality
FROM python:3.9-slim

# Set the working directory inside the container
# All subsequent commands will be executed from this directory
WORKDIR /app

# Install system dependencies required for compiling Python packages
# gcc, g++: C/C++ compilers needed for packages like blis, spaCy
# python3-dev: Python development headers needed for compilation
# build-essential: Essential build tools and libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better Docker layer caching
# If dependencies don't change, Docker can reuse the cached layer
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir saves space by not storing pip cache
# --upgrade ensures pip itself is up to date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
# This includes main.py and any other Python files
COPY . .

# Expose port 8002 where the FastAPI application will listen
# This documents which port the container uses
EXPOSE 8002

# Define the startup command for the container
# uvicorn runs the FastAPI application with production settings
# --host 0.0.0.0 allows external connections to the container
# --port 8002 specifies the port to bind to
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
