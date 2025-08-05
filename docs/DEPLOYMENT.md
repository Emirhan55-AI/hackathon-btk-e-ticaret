# 🚀 AURA AI - Deployment Kılavuzu

## 📋 İçindekiler

1. [Deployment Genel Bakış](#deployment-genel-bakış)
2. [Environment Konfigürasyonu](#environment-konfigürasyonu)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Monitoring ve Logging](#monitoring-ve-logging)
7. [Security Konfigürasyonu](#security-konfigürasyonu)
8. [Backup ve Recovery](#backup-ve-recovery)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Deployment Genel Bakış

AURA AI sistemi mikroservis mimarisi kullanır ve aşağıdaki deployment seçenekleri sunar:

### Deployment Seçenekleri

| Seçenek | Açıklama | Önerilen Kullanım |
|---------|----------|-------------------|
| **Development** | Local development environment | Geliştirme ve test |
| **Docker Compose** | Single-machine container deployment | Demo ve proof-of-concept |
| **Kubernetes** | Orchestrated container deployment | Production ve scaling |
| **Cloud Native** | Managed cloud services | Enterprise deployment |

### Sistem Gereksinimleri

#### Minimum Gereksinimler (Development)
```
CPU: 4 cores
RAM: 8GB
Disk: 20GB SSD
Network: 1 Gbps
```

#### Önerilen Gereksinimler (Production)
```
CPU: 16 cores (AI workloads için)
RAM: 32GB
Disk: 100GB SSD (Database + Model storage)
GPU: NVIDIA GPU (opsiyonel, AI performance için)
Network: 10 Gbps
```

---

## ⚙️ Environment Konfigürasyonu

### 1. Environment Dosyaları

Her environment için ayrı konfigürasyon dosyaları:

```powershell
# Environment dosyalarını oluştur
Copy-Item environments\.env.development .env.development
Copy-Item environments\.env.staging .env.staging  
Copy-Item environments\.env.production .env.production
```

#### Development Environment (.env.development)

```env
# =================================
# AURA AI - Development Environment
# =================================

# Environment Info
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database Configuration
DATABASE_URL=postgresql://aura_dev:dev_password@localhost:5432/aura_ai_dev
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# Security Configuration
JWT_SECRET_KEY=development-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# Service URLs (Development)
ORCHESTRATOR_URL=http://localhost:8007
IMAGE_PROCESSING_URL=http://localhost:8001
NLU_SERVICE_URL=http://localhost:8002
STYLE_PROFILE_URL=http://localhost:8003
COMBINATION_ENGINE_URL=http://localhost:8004
RECOMMENDATION_ENGINE_URL=http://localhost:8005
FEEDBACK_LOOP_URL=http://localhost:8006

# AI Model Configuration
ENABLE_AI_MODELS=false  # Development'ta mock models
AI_MODEL_PATH=./models/dev
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-key

# File Upload Configuration
UPLOAD_MAX_SIZE=50MB
UPLOAD_ALLOWED_TYPES=jpg,jpeg,png,gif
UPLOAD_STORAGE_PATH=./uploads/dev

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
ENABLE_TRACING=false

# External Services (Development)
ENABLE_EMAIL_SERVICE=false
ENABLE_SMS_SERVICE=false
ENABLE_ANALYTICS=false
```

#### Staging Environment (.env.staging)

```env
# =================================
# AURA AI - Staging Environment
# =================================

# Environment Info
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://aura_staging:${DB_PASSWORD}@staging-db:5432/aura_ai_staging
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis Configuration
REDIS_URL=redis://staging-redis:6379/0
REDIS_PASSWORD=${REDIS_PASSWORD}

# Security Configuration
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=12

# Service URLs (Staging)
ORCHESTRATOR_URL=http://orchestrator:8007
IMAGE_PROCESSING_URL=http://image-processing:8001
NLU_SERVICE_URL=http://nlu-service:8002
STYLE_PROFILE_URL=http://style-profile:8003
COMBINATION_ENGINE_URL=http://combination-engine:8004
RECOMMENDATION_ENGINE_URL=http://recommendation-engine:8005
FEEDBACK_LOOP_URL=http://feedback-loop:8006

# AI Model Configuration
ENABLE_AI_MODELS=true
AI_MODEL_PATH=/app/models
OPENAI_API_KEY=${OPENAI_API_KEY}
HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}

# File Upload Configuration
UPLOAD_MAX_SIZE=10MB
UPLOAD_ALLOWED_TYPES=jpg,jpeg,png
UPLOAD_STORAGE_PATH=/app/uploads
UPLOAD_STORAGE_TYPE=s3
S3_BUCKET_NAME=aura-ai-staging-uploads

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
ENABLE_TRACING=true
JAEGER_ENDPOINT=http://jaeger:14268/api/traces

# External Services (Staging)
ENABLE_EMAIL_SERVICE=true
ENABLE_SMS_SERVICE=false
ENABLE_ANALYTICS=true
```

#### Production Environment (.env.production)

```env
# =================================
# AURA AI - Production Environment
# =================================

# Environment Info
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Database Configuration
DATABASE_URL=postgresql://aura_prod:${DB_PASSWORD}@prod-db-cluster:5432/aura_ai
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=50
DATABASE_SSL_MODE=require

# Redis Configuration
REDIS_URL=rediss://prod-redis-cluster:6380/0
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_SSL=true

# Security Configuration
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=8
CORS_ALLOWED_ORIGINS=https://aura-ai.com,https://api.aura-ai.com
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=5000

# Service URLs (Production)
ORCHESTRATOR_URL=https://orchestrator.internal.aura-ai.com
IMAGE_PROCESSING_URL=https://image-processing.internal.aura-ai.com
NLU_SERVICE_URL=https://nlu.internal.aura-ai.com
STYLE_PROFILE_URL=https://style-profile.internal.aura-ai.com
COMBINATION_ENGINE_URL=https://combination-engine.internal.aura-ai.com
RECOMMENDATION_ENGINE_URL=https://recommendation.internal.aura-ai.com
FEEDBACK_LOOP_URL=https://feedback.internal.aura-ai.com

# AI Model Configuration
ENABLE_AI_MODELS=true
AI_MODEL_PATH=/app/models
OPENAI_API_KEY=${OPENAI_API_KEY}
HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
MODEL_CACHE_SIZE=1000
ENABLE_GPU=true

# File Upload Configuration
UPLOAD_MAX_SIZE=5MB
UPLOAD_ALLOWED_TYPES=jpg,jpeg,png
UPLOAD_STORAGE_TYPE=s3
S3_BUCKET_NAME=aura-ai-prod-uploads
S3_REGION=us-east-1
CDN_URL=https://cdn.aura-ai.com

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
ENABLE_TRACING=true
JAEGER_ENDPOINT=https://jaeger.monitoring.aura-ai.com/api/traces
PROMETHEUS_ENDPOINT=https://prometheus.monitoring.aura-ai.com

# External Services (Production)
ENABLE_EMAIL_SERVICE=true
ENABLE_SMS_SERVICE=true
ENABLE_ANALYTICS=true
ENABLE_ERROR_TRACKING=true
SENTRY_DSN=${SENTRY_DSN}
```

---

## 🐳 Docker Deployment

### 1. Docker Compose Setup

#### Development Docker Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # =================
  # Infrastructure
  # =================
  
  postgres:
    image: postgres:15
    container_name: aura-postgres-dev
    environment:
      POSTGRES_DB: aura_ai_dev
      POSTGRES_USER: aura_dev
      POSTGRES_PASSWORD: dev_password
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - aura-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aura_dev"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: aura-redis-dev
    command: redis-server --appendonly yes
    volumes:
      - redis_data_dev:/data
    ports:
      - "6379:6379"
    networks:
      - aura-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =================
  # AURA AI Services
  # =================

  orchestrator:
    build:
      context: .
      dockerfile: services/orchestrator/Dockerfile
      target: development
    container_name: aura-orchestrator-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/orchestrator:/app
      - ./shared:/app/shared
    ports:
      - "8007:8007"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  image-processing:
    build:
      context: .
      dockerfile: services/image_processing/Dockerfile
      target: development
    container_name: aura-image-processing-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/image_processing:/app
      - ./shared:/app/shared
      - ./models:/app/models
      - ./uploads:/app/uploads
    ports:
      - "8001:8001"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped
    # GPU support için (opsiyonel)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

  nlu-service:
    build:
      context: .
      dockerfile: services/nlu_service/Dockerfile
      target: development
    container_name: aura-nlu-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/nlu_service:/app
      - ./shared:/app/shared
      - ./models:/app/models
    ports:
      - "8002:8002"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  style-profile:
    build:
      context: .
      dockerfile: services/style_profile/Dockerfile
      target: development
    container_name: aura-style-profile-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/style_profile:/app
      - ./shared:/app/shared
    ports:
      - "8003:8003"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  combination-engine:
    build:
      context: .
      dockerfile: services/combination_engine/Dockerfile
      target: development
    container_name: aura-combination-engine-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/combination_engine:/app
      - ./shared:/app/shared
    ports:
      - "8004:8004"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  recommendation-engine:
    build:
      context: .
      dockerfile: services/recommendation_engine/Dockerfile
      target: development
    container_name: aura-recommendation-engine-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/recommendation_engine:/app
      - ./shared:/app/shared
    ports:
      - "8005:8005"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  feedback-loop:
    build:
      context: .
      dockerfile: services/feedback_loop/Dockerfile
      target: development
    container_name: aura-feedback-loop-dev
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    volumes:
      - ./services/feedback_loop:/app
      - ./shared:/app/shared
    ports:
      - "8006:8006"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - aura-network
    restart: unless-stopped

  # =================
  # Monitoring Stack
  # =================

  prometheus:
    image: prom/prometheus:latest
    container_name: aura-prometheus-dev
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data_dev:/prometheus
    ports:
      - "9090:9090"
    networks:
      - aura-network
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: aura-grafana-dev
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data_dev:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
    networks:
      - aura-network
    restart: unless-stopped

networks:
  aura-network:
    driver: bridge

volumes:
  postgres_data_dev:
  redis_data_dev:
  prometheus_data_dev:
  grafana_data_dev:
```

### 2. Multi-Stage Dockerfile Template

```dockerfile
# services/image_processing/Dockerfile

# =================
# Base Stage
# =================
FROM python:3.11-slim as base

# Sistem paketlerini güncelle ve gerekli dependencies yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Working directory oluştur
WORKDIR /app

# =================
# Dependencies Stage  
# =================
FROM base as dependencies

# Requirements dosyalarını kopyala
COPY services/image_processing/requirements.txt .
COPY requirements-shared.txt .

# Python dependencies yükle
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-shared.txt

# =================
# Development Stage
# =================
FROM dependencies as development

# Development dependencies ekle
COPY services/image_processing/requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Shared kod kopyala
COPY shared/ ./shared/

# Service kodunu kopyala
COPY services/image_processing/ .

# Non-root user oluştur
RUN groupadd -r aura && useradd -r -g aura aura
RUN chown -R aura:aura /app
USER aura

# Health check ekle
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Port expose et
EXPOSE 8001

# Development server başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

# =================
# Production Stage
# =================
FROM dependencies as production

# Shared kod kopyala
COPY shared/ ./shared/

# Service kodunu kopyala
COPY services/image_processing/ .

# Non-root user oluştur
RUN groupadd -r aura && useradd -r -g aura aura
RUN chown -R aura:aura /app
USER aura

# Health check ekle
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Port expose et
EXPOSE 8001

# Production server başlat
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]
```

### 3. Docker Deployment Scripts

#### Development Deployment Script

```powershell
# scripts/deploy-development.ps1

param(
    [string]$Action = "up",
    [switch]$Build = $false,
    [switch]$Force = $false
)

Write-Host "🚀 AURA AI Development Deployment Script" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

# Environment kontrolü
if (-not (Test-Path ".env.development")) {
    Write-Host "❌ .env.development dosyası bulunamadı!" -ForegroundColor Red
    Write-Host "Önce environment dosyasını oluşturun:" -ForegroundColor Yellow
    Write-Host "Copy-Item environments\.env.development .env.development" -ForegroundColor Yellow
    exit 1
}

# Docker ve Docker Compose kontrolü
try {
    $dockerVersion = docker --version
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
    Write-Host "✅ Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker veya Docker Compose yüklü değil!" -ForegroundColor Red
    exit 1
}

# Deployment action'ına göre işlem yap
switch ($Action.ToLower()) {
    "up" {
        Write-Host "🔄 Development environment başlatılıyor..." -ForegroundColor Blue
        
        $composeArgs = @(
            "-f", "docker-compose.dev.yml",
            "up", "-d"
        )
        
        if ($Build) {
            $composeArgs += "--build"
        }
        
        if ($Force) {
            $composeArgs += "--force-recreate"
        }
        
        & docker-compose $composeArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Development environment başarıyla başlatıldı!" -ForegroundColor Green
            Write-Host "" 
            Write-Host "📊 Servis URL'leri:" -ForegroundColor Cyan
            Write-Host "   Orchestrator:         http://localhost:8007" -ForegroundColor White
            Write-Host "   Image Processing:     http://localhost:8001" -ForegroundColor White
            Write-Host "   NLU Service:          http://localhost:8002" -ForegroundColor White
            Write-Host "   Style Profile:        http://localhost:8003" -ForegroundColor White
            Write-Host "   Combination Engine:   http://localhost:8004" -ForegroundColor White
            Write-Host "   Recommendation:       http://localhost:8005" -ForegroundColor White
            Write-Host "   Feedback Loop:        http://localhost:8006" -ForegroundColor White
            Write-Host ""
            Write-Host "📈 Monitoring:" -ForegroundColor Cyan
            Write-Host "   Prometheus:           http://localhost:9090" -ForegroundColor White
            Write-Host "   Grafana:              http://localhost:3000 (admin/admin)" -ForegroundColor White
        } else {
            Write-Host "❌ Deployment başarısız!" -ForegroundColor Red
            exit 1
        }
    }
    
    "down" {
        Write-Host "🔄 Development environment durduruluyor..." -ForegroundColor Blue
        
        $downArgs = @("-f", "docker-compose.dev.yml", "down")
        
        if ($Force) {
            $downArgs += "-v"  # Volume'ları da sil
            Write-Host "⚠️  Volume'lar da silinecek!" -ForegroundColor Yellow
        }
        
        & docker-compose $downArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Development environment başarıyla durduruldu!" -ForegroundColor Green
        }
    }
    
    "restart" {
        Write-Host "🔄 Development environment yeniden başlatılıyor..." -ForegroundColor Blue
        & docker-compose -f docker-compose.dev.yml restart
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Development environment başarıyla yeniden başlatıldı!" -ForegroundColor Green
        }
    }
    
    "logs" {
        Write-Host "📋 Servis logları görüntüleniyor..." -ForegroundColor Blue
        & docker-compose -f docker-compose.dev.yml logs -f
    }
    
    "status" {
        Write-Host "📊 Servis durumları:" -ForegroundColor Blue
        & docker-compose -f docker-compose.dev.yml ps
        
        Write-Host ""
        Write-Host "🔍 Health check sonuçları:" -ForegroundColor Blue
        
        $services = @(
            @{name="Orchestrator"; url="http://localhost:8007/health"},
            @{name="Image Processing"; url="http://localhost:8001/health"},
            @{name="NLU Service"; url="http://localhost:8002/health"},
            @{name="Style Profile"; url="http://localhost:8003/health"},
            @{name="Combination Engine"; url="http://localhost:8004/health"},
            @{name="Recommendation"; url="http://localhost:8005/health"},
            @{name="Feedback Loop"; url="http://localhost:8006/health"}
        )
        
        foreach ($service in $services) {
            try {
                $response = Invoke-RestMethod -Uri $service.url -Method Get -TimeoutSec 5
                if ($response.status -eq "healthy") {
                    Write-Host "   ✅ $($service.name): Healthy" -ForegroundColor Green
                } else {
                    Write-Host "   ⚠️  $($service.name): $($response.status)" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "   ❌ $($service.name): Unreachable" -ForegroundColor Red
            }
        }
    }
    
    "clean" {
        Write-Host "🧹 Docker sistem temizliği yapılıyor..." -ForegroundColor Blue
        
        & docker-compose -f docker-compose.dev.yml down -v
        & docker system prune -f
        & docker volume prune -f
        
        Write-Host "✅ Sistem temizliği tamamlandı!" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ Geçersiz action: $Action" -ForegroundColor Red
        Write-Host ""
        Write-Host "Kullanılabilir action'lar:" -ForegroundColor Yellow
        Write-Host "  up      - Environment'ı başlat" -ForegroundColor White
        Write-Host "  down    - Environment'ı durdur" -ForegroundColor White  
        Write-Host "  restart - Environment'ı yeniden başlat" -ForegroundColor White
        Write-Host "  logs    - Logları görüntüle" -ForegroundColor White
        Write-Host "  status  - Servis durumlarını kontrol et" -ForegroundColor White
        Write-Host "  clean   - Docker temizliği yap" -ForegroundColor White
        Write-Host ""
        Write-Host "Örnek kullanım:" -ForegroundColor Yellow
        Write-Host "  .\scripts\deploy-development.ps1 -Action up -Build" -ForegroundColor White
        exit 1
    }
}
```

---

## 🌐 Production Deployment

### 1. Kubernetes Deployment

#### Namespace ve ConfigMap

```yaml
# k8s/namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: aura-ai
  labels:
    name: aura-ai
    environment: production

---
# k8s/configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aura-ai-config
  namespace: aura-ai
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  ENABLE_METRICS: "true"
  METRICS_PORT: "9090"
  # Non-sensitive configuration values
```

#### Secret Management

```yaml
# k8s/secrets.yml
apiVersion: v1
kind: Secret
metadata:
  name: aura-ai-secrets
  namespace: aura-ai
type: Opaque
data:
  # Base64 encoded values
  DATABASE_URL: <base64-encoded-database-url>
  JWT_SECRET_KEY: <base64-encoded-jwt-secret>
  REDIS_PASSWORD: <base64-encoded-redis-password>
  OPENAI_API_KEY: <base64-encoded-openai-key>
  HUGGINGFACE_API_KEY: <base64-encoded-hf-key>
```

#### Service Deployment Template

```yaml
# k8s/image-processing-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-processing
  namespace: aura-ai
  labels:
    app: image-processing
    component: ai-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: image-processing
  template:
    metadata:
      labels:
        app: image-processing
        component: ai-service
    spec:
      containers:
      - name: image-processing
        image: aura-ai/image-processing:latest
        ports:
        - containerPort: 8001
        env:
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: aura-ai-config
              key: ENVIRONMENT
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: aura-ai-secrets
              key: DATABASE_URL
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: aura-ai-secrets
              key: REDIS_URL
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi" 
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
        - name: upload-storage
          mountPath: /app/uploads
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-storage-pvc
      - name: upload-storage
        persistentVolumeClaim:
          claimName: upload-storage-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: image-processing-service
  namespace: aura-ai
spec:
  selector:
    app: image-processing
  ports:
  - protocol: TCP
    port: 8001
    targetPort: 8001
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: image-processing-ingress
  namespace: aura-ai
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.aura-ai.com
    secretName: aura-ai-tls
  rules:
  - host: api.aura-ai.com
    http:
      paths:
      - path: /image-processing
        pathType: Prefix
        backend:
          service:
            name: image-processing-service
            port:
              number: 8001
```

### 2. Database Migration

#### Alembic Production Migration Script

```powershell
# scripts/migrate-production.ps1

param(
    [string]$Environment = "production",
    [string]$Action = "upgrade",
    [string]$Revision = "head"
)

Write-Host "🗃️  AURA AI Database Migration - $Environment" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Environment dosyasını yükle
$envFile = ".env.$Environment"
if (-not (Test-Path $envFile)) {
    Write-Host "❌ Environment dosyası bulunamadı: $envFile" -ForegroundColor Red
    exit 1
}

# Database connection test
Write-Host "🔍 Database bağlantısı test ediliyor..." -ForegroundColor Blue

try {
    # Alembic ile database durumunu kontrol et
    $currentRevision = alembic current 2>&1
    Write-Host "📊 Mevcut revision: $currentRevision" -ForegroundColor Cyan
    
    # Pending migration'ları kontrol et
    $pending = alembic heads 2>&1
    Write-Host "📈 Hedef revision: $pending" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Database bağlantısı başarısız: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Migration action'ına göre işlem yap
switch ($Action.ToLower()) {
    "upgrade" {
        Write-Host "⬆️  Database upgrade işlemi başlatılıyor..." -ForegroundColor Blue
        
        # Backup önce al (production için)
        if ($Environment -eq "production") {
            Write-Host "💾 Production database backup alınıyor..." -ForegroundColor Yellow
            $backupFile = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
            & pg_dump $env:DATABASE_URL > $backupFile
            Write-Host "✅ Backup alındı: $backupFile" -ForegroundColor Green
        }
        
        # Migration'ı çalıştır
        & alembic upgrade $Revision
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database upgrade başarılı!" -ForegroundColor Green
        } else {
            Write-Host "❌ Database upgrade başarısız!" -ForegroundColor Red
            exit 1
        }
    }
    
    "downgrade" {
        if ($Environment -eq "production") {
            Write-Host "⚠️  Production environment'ta downgrade tehlikeli!" -ForegroundColor Red
            $confirm = Read-Host "Devam etmek istediğinizden emin misiniz? (yes/no)"
            if ($confirm -ne "yes") {
                Write-Host "❌ İşlem iptal edildi." -ForegroundColor Yellow
                exit 0
            }
        }
        
        Write-Host "⬇️  Database downgrade işlemi başlatılıyor..." -ForegroundColor Blue
        & alembic downgrade $Revision
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database downgrade başarılı!" -ForegroundColor Green
        } else {
            Write-Host "❌ Database downgrade başarısız!" -ForegroundColor Red
            exit 1
        }
    }
    
    "status" {
        Write-Host "📊 Database migration durumu:" -ForegroundColor Blue
        & alembic current
        & alembic history
    }
    
    default {
        Write-Host "❌ Geçersiz action: $Action" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Migration işlemi tamamlandı!" -ForegroundColor Green
```

---

## ☁️ Cloud Deployment

### 1. AWS Deployment

#### ECS Task Definition

```json
{
  "family": "aura-ai-image-processing",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/aura-ai-task-role",
  "containerDefinitions": [
    {
      "name": "image-processing",
      "image": "your-ecr-repo/aura-ai/image-processing:latest",
      "portMappings": [
        {
          "containerPort": 8001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:aura-ai/database-url"
        },
        {
          "name": "JWT_SECRET_KEY", 
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:aura-ai/jwt-secret"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/aura-ai/image-processing",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:8001/health || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

#### Terraform Infrastructure

```hcl
# infrastructure/aws/main.tf

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "aura-ai-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = true
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "aura_ai" {
  name = "aura-ai-cluster"
  
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight           = 1
  }
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "aura_ai" {
  identifier = "aura-ai-database"
  
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.t3.medium"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type         = "gp2"
  storage_encrypted    = true
  
  db_name  = "aura_ai"
  username = "aura_admin"
  password = var.database_password
  
  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.aura_ai.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "aura-ai-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

# ElastiCache Redis
resource "aws_elasticache_replication_group" "aura_ai" {
  replication_group_id       = "aura-ai-redis"
  description                = "AURA AI Redis Cache"
  
  node_type            = "cache.t3.micro"
  port                 = 6379
  parameter_group_name = "default.redis7"
  
  num_cache_clusters = 2
  
  subnet_group_name = aws_elasticache_subnet_group.aura_ai.name
  security_group_ids = [aws_security_group.cache.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                = var.redis_auth_token
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

# Application Load Balancer
resource "aws_lb" "aura_ai" {
  name               = "aura-ai-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = true
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

# S3 Bucket for file uploads
resource "aws_s3_bucket" "uploads" {
  bucket = "aura-ai-uploads-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = "aura-ai"
  }
}

resource "aws_s3_bucket_versioning" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
```

### 2. Azure Deployment

#### ARM Template Snippet

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {
      "type": "string",
      "defaultValue": "production"
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-03-01",
      "name": "aura-ai-services",
      "location": "[parameters('location')]",
      "properties": {
        "containers": [
          {
            "name": "image-processing",
            "properties": {
              "image": "auraaiacr.azurecr.io/image-processing:latest",
              "ports": [
                {
                  "port": 8001,
                  "protocol": "TCP"
                }
              ],
              "environmentVariables": [
                {
                  "name": "ENVIRONMENT",
                  "value": "[parameters('environment')]"
                }
              ],
              "resources": {
                "requests": {
                  "cpu": 1,
                  "memoryInGB": 2
                }
              }
            }
          }
        ],
        "osType": "Linux",
        "restartPolicy": "Always",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "port": 8001,
              "protocol": "TCP"
            }
          ]
        }
      }
    }
  ]
}
```

Bu deployment kılavuzu, AURA AI sisteminin farklı ortamlarda güvenli ve ölçeklenebilir şekilde deploy edilmesini sağlar.
