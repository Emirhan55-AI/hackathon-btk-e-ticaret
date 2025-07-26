# Use Python 3.9 slim image as the foundation
# Slim images provide essential Python functionality while keeping size minimal
FROM python:3.9-slim

# Set the working directory inside the container
# This is where the application code will be stored and executed
WORKDIR /app

# Copy requirements file first for optimal Docker layer caching
# If dependencies don't change, Docker can reuse this cached layer
COPY requirements.txt .

# Install Python dependencies with optimizations
# --no-cache-dir prevents storing pip cache to reduce image size
# --upgrade ensures pip itself is up-to-date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source code into the container
# This includes main.py and any supporting modules
COPY . .

# Expose port 8000 where the FastAPI application will run
# This tells Docker which port the container will use
EXPOSE 8000

# Define the startup command when the container runs
# uvicorn serves the FastAPI application with production settings
# --host 0.0.0.0 allows external connections to reach the container
# --port 8000 binds to the exposed port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
