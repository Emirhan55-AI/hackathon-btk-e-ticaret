# 🐳 Multi-Modal Coordinator Service Dockerfile
# AURA AI Çok Modlu Sorgu Koordinatörü Container Configuration

# Python base image kullan - Multi-stage build için
FROM python:3.11-slim as base

# Container metadata - Maintainer ve açıklama bilgileri
LABEL maintainer="AURA AI Development Team <dev@aura-ai.com>"
LABEL description="Multi-Modal Coordinator Service for AURA AI Fashion Assistant"
LABEL version="1.0.0"
LABEL service="multi_modal_coordinator"
LABEL port="8009"

# Environment variables - Python ve container optimizasyonları
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Working directory oluştur - Tüm işlemler burada yapılacak
WORKDIR /app

# System dependencies yükle - OpenCV ve image processing için gerekli
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies için requirements dosyası oluştur
COPY requirements.txt .

# Python packages yükle - Cache layer'ı optimize et
RUN pip install --no-cache-dir -r requirements.txt

# Application source code kopyala
COPY . .

# Non-root user oluştur - Security best practice
RUN groupadd -r aura && useradd -r -g aura aura && \
    chown -R aura:aura /app

# User'ı switch et - Root olarak çalıştırma
USER aura

# Health check script tanımla - Container health monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8009/', timeout=5)" || exit 1

# Port expose et - Multi-Modal Coordinator service port
EXPOSE 8009

# Logging directory oluştur
RUN mkdir -p /app/logs

# Startup command - FastAPI uygulamasını başlat
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009", "--workers", "1"]
