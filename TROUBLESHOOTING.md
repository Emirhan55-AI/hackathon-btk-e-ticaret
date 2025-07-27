# 🔧 Aura AI System - Troubleshooting Guide

## 🚨 Common Issues and Solutions

### Issue 1: Docker Desktop Not Running
**Error:** `error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/..."`

**Solution:**
1. **Start Docker Desktop**
   - Open Start Menu → Search "Docker Desktop" → Click to start
   - Wait for Docker Desktop to fully initialize (whale icon in system tray)
   - Docker icon should show "Docker Desktop is running" when ready

2. **Verify Docker is Running**
   ```powershell
   docker --version
   docker ps
   ```

3. **Try System Startup Again**
   ```powershell
   python run_aura.py
   ```

### Issue 2: Docker Desktop Not Installed
**Error:** `Docker not installed or not in PATH`

**Solution:**
1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Download Docker Desktop for Windows
   - Install with default settings

2. **Restart Your Computer**
   - Docker Desktop requires a restart to complete installation

3. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

### Issue 3: Insufficient System Resources
**Error:** System appears to start but services fail health checks

**Solution:**
1. **Check Available Resources**
   - Minimum: 8GB RAM, 4 CPU cores
   - Recommended: 16GB RAM, 8 CPU cores

2. **Allocate More Resources to Docker**
   - Open Docker Desktop → Settings → Resources
   - Increase Memory to at least 6GB
   - Increase CPUs to at least 4 cores

3. **Close Other Applications**
   - Free up system memory by closing unnecessary applications

### Issue 4: PyTorch/TorchVision Dependency Conflicts
**Error:** `Cannot install torch and torchvision because these package versions have conflicting dependencies`

**Solution:**
1. **Use Compatible Versions**
   - The issue occurs when PyTorch and TorchVision versions don't match
   - We've fixed this by using `torch==2.0.1` and `torchvision==0.15.2`

2. **CLIP Package Conflicts**
   - `clip-by-openai` requires old PyTorch versions (1.7.x) 
   - We've temporarily disabled it in favor of transformers CLIP implementation

3. **If Issues Persist**
   ```powershell
   # Clean Docker build cache
   docker system prune -f
   docker-compose build --no-cache
   ```

### Issue 5: SQLite3 Installation Error
**Error:** `ERROR: No matching distribution found for sqlite3`

**Solution:**
1. **Remove sqlite3 from requirements.txt**
   - `sqlite3` is a built-in Python module and shouldn't be installed via pip
   - We've fixed this by removing it from feedback_loop_service requirements

2. **Use aiosqlite instead**
   - For async SQLite operations, use `aiosqlite` package
   - This is already correctly configured in the requirements

### Issue 6: Missing Dependency Injector
**Error:** `ModuleNotFoundError: No module named 'dependency_injector'`

**Solution:**
1. **Add missing dependency**
   - The backend requires `dependency-injector==4.41.0` package
   - We've fixed this by adding it to requirements.txt

2. **Rebuild the service**
   ```powershell
   docker-compose up -d --build backend
   ```

### Issue 7: Missing Build Tools for Python Packages
**Error:** `error: [Errno 2] No such file or directory: 'gcc'` or similar compilation errors

**Solution:**
1. **The issue occurs with packages that need compilation**
   - Packages like `blis`, `spaCy`, and some ML libraries need C/C++ compilation
   - Python slim images don't include build tools by default

2. **Fixed by adding build dependencies to Dockerfiles**
   ```dockerfile
   RUN apt-get update && apt-get install -y \
       gcc \
       g++ \
       python3-dev \
       build-essential \
       && rm -rf /var/lib/apt/lists/*
   ```

3. **Clean and rebuild if needed**
   ```powershell
   docker system prune -f
   docker-compose build --no-cache
   ```

## 🔄 Alternative Startup Methods

### Method 1: Manual Service Startup (If Docker Issues Persist)

#### Start Individual Services
```powershell
# Start core infrastructure first
docker-compose up -d postgres redis

# Wait 30 seconds for databases to initialize
Start-Sleep -Seconds 30

# Start e-commerce backend
docker-compose up -d backend

# Start AI services one by one
docker-compose up -d image-processing-service
docker-compose up -d nlu-service
docker-compose up -d style-profile-service
docker-compose up -d combination-engine-service
docker-compose up -d recommendation-engine-service
docker-compose up -d orchestrator-service
docker-compose up -d feedback-loop-service
```

### Method 2: Selective Service Startup
```powershell
# Start only essential services for demo
docker-compose up -d postgres redis backend orchestrator-service
```

### Method 3: Development Mode (Single Services)
```powershell
# Navigate to specific service directory and run individually
cd image_processing_service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```

## 🔍 Diagnostic Commands

### Check Docker Status
```powershell
# Verify Docker is running
docker info

# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# Check Docker Compose services
docker-compose ps
```

### Check System Resources
```powershell
# Check memory usage
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check Docker resource usage
docker stats --no-stream
```

### View Service Logs
```powershell
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs orchestrator-service

# Follow logs in real-time
docker-compose logs -f orchestrator-service
```

## 🛠️ Step-by-Step Docker Desktop Setup

### 1. Download and Install Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer with admin privileges
4. Accept license and install with default settings
5. **Restart your computer** when prompted

### 2. Configure Docker Desktop
1. Start Docker Desktop from Start Menu
2. Wait for initialization (may take 2-3 minutes first time)
3. Open Docker Desktop Settings
4. Go to Resources → Advanced
5. Set Memory to at least 6GB (8GB recommended)
6. Set CPUs to at least 4 cores
7. Click "Apply & Restart"

### 3. Verify Installation
```powershell
# Check Docker version
docker --version

# Check Docker Compose version  
docker-compose --version

# Test Docker with hello-world
docker run hello-world
```

## 🎯 Quick Fixes for Common Scenarios

### Scenario 1: "Docker Desktop is starting..."
**Wait 2-3 minutes** for Docker Desktop to fully initialize, then try again.

### Scenario 2: Services start but health checks fail
```powershell
# Wait longer for services to initialize
Start-Sleep -Seconds 60

# Check service health manually
python run_aura.py --health
```

### Scenario 3: Port conflicts
```powershell
# Check what's using ports
netstat -ano | findstr :8000
netstat -ano | findstr :8006

# Kill conflicting processes if necessary
taskkill /PID <process_id> /F
```

## 📞 Support Commands

### Get System Information
```powershell
# System info for troubleshooting
systeminfo | findstr /B /C:"OS Name" /C:"Total Physical Memory"
docker version
docker-compose version
```

### Generate Debug Report
```powershell
# Create debug information file
echo "=== Aura AI Debug Report ===" > debug_report.txt
echo "Date: $(Get-Date)" >> debug_report.txt
echo "" >> debug_report.txt
echo "=== System Info ===" >> debug_report.txt
systeminfo | findstr /B /C:"OS Name" /C:"Total Physical Memory" >> debug_report.txt
echo "" >> debug_report.txt
echo "=== Docker Info ===" >> debug_report.txt
docker version >> debug_report.txt 2>&1
echo "" >> debug_report.txt
docker ps -a >> debug_report.txt 2>&1
echo "" >> debug_report.txt
echo "=== Docker Compose Status ===" >> debug_report.txt
docker-compose ps >> debug_report.txt 2>&1
```

## 🎉 Success Checklist

When everything is working correctly, you should see:

✅ Docker Desktop running (whale icon in system tray)  
✅ `docker ps` command works without errors  
✅ All containers show "Up" status in `docker-compose ps`  
✅ Health checks pass when running `python run_aura.py --health`  
✅ Web interfaces accessible:
- E-commerce: http://localhost:8000
- AI Services: http://localhost:8006  
- Monitor: http://localhost:8080

---

**Need more help?** Check the main README.md for additional documentation and system requirements.
