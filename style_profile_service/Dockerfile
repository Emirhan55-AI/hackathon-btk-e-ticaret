# Use Python 3.9 slim image as base
# Provides a lightweight foundation with essential Python tools
FROM python:3.9-slim

# Set working directory for the application
# All commands will execute from this location inside the container
WORKDIR /app

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

# Expose port 8000 for the FastAPI service
# This documents which port the container uses
EXPOSE 8000

# Define the command to start the service when container runs
# uvicorn is the ASGI server that hosts our FastAPI application
# --host 0.0.0.0 allows connections from outside the container
# --port 8000 binds to the exposed port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
