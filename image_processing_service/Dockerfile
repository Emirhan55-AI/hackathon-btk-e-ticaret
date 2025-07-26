# Use Python 3.9 slim image as the base
# Slim images are smaller and more secure than full Python images
FROM python:3.9-slim

# Set the working directory inside the container
# This is where our application code will be stored
WORKDIR /app

# Copy the requirements file first (before copying all code)
# This allows Docker to cache the pip install step if dependencies haven't changed
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir prevents pip from storing cache, keeping the image smaller
# --upgrade ensures we get the latest compatible versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
# The . means copy everything from the current directory to /app
COPY . .

# Expose port 8000 for the FastAPI application
# This tells Docker that the container listens on port 8000
EXPOSE 8000

# Define the command to run when the container starts
# uvicorn is the ASGI server that runs our FastAPI application
# --host 0.0.0.0 allows connections from outside the container
# --port 8000 specifies the port to listen on
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
