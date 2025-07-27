# 📊 Real-Time Build Monitor Commands

## 🚀 **Quick Status Checks**

### **Core System Health**
```powershell
# Backend API Status
(Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).StatusCode

# All Running Containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Docker Compose Services Status
docker-compose ps
```

### **Build Progress Monitoring**
```powershell
# Check built images
docker images | findstr "btk-hackathon"

# Monitor specific service logs
docker-compose logs --tail=10 recommendation-engine-service
docker-compose logs --tail=10 orchestrator-service
docker-compose logs --tail=10 feedback-loop-service

# Follow logs in real-time
docker-compose logs -f --tail=5
```

## 🔄 **Continuous Monitoring Script**

Create this PowerShell script for automated monitoring:

```powershell
# monitor_builds.ps1
while ($true) {
    Clear-Host
    Write-Host "=== Aura AI Build Monitor ===" -ForegroundColor Cyan
    Write-Host "Time: $(Get-Date)" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Core Services Status:" -ForegroundColor Green
    docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -match "aura_" }
    
    Write-Host ""
    Write-Host "Built Images:" -ForegroundColor Green  
    docker images | findstr "btk-hackathon" | Select-Object -First 10
    
    Write-Host ""
    Write-Host "Services in docker-compose:" -ForegroundColor Green
    docker-compose ps --format "table {{.Name}}\t{{.Status}}"
    
    Write-Host ""
    Write-Host "Press Ctrl+C to stop monitoring..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}
```

## 📈 **Expected Build Timeline**

### **Completed (✅)**
- ✅ **Infrastructure Services**: PostgreSQL, Redis, Backend (0 minutes)
- ✅ **Image Processing Service**: Built successfully (~5 minutes)
- ✅ **NLU Service**: Completed with build tools fix (~25 minutes)
- ✅ **Style Profile Service**: Built successfully (~8 minutes)
- ✅ **Combination Engine Service**: Built successfully (~12 minutes)

### **Currently Building (🔄)**
- 🔄 **Recommendation Engine**: Building (~15-20 minutes total)
  - Status: Export phase (2.5+ minutes exporting)
  - Contains: FAISS, advanced ML, recommendation algorithms
  
- 🔄 **Orchestrator Service**: Building (~10-15 minutes total)
  - Status: Export phase
  - Contains: Workflow management, service coordination
  
- 🔄 **Feedback Loop Service**: Building (~10-15 minutes total)
  - Status: Export phase  
  - Contains: Advanced learning, user feedback processing

## 🎯 **Progress Indicators**

### **Build Stages**
1. **Load build context** (< 1 second)
2. **Install system dependencies** (cached after first build)
3. **Install Python packages** (cached after first build) 
4. **Copy application code** (< 1 second)
5. **Export to image** (2-5 minutes for large ML packages) ⏳ **Current Stage**
6. **Container startup** (< 30 seconds)

### **Export Phase Details**  
The export phase takes longer for AI services because:
- Large ML model files (PyTorch, transformers, FAISS)
- Complex dependency trees  
- Image layer compression
- **This is normal and expected!**

## 🚦 **Status Meanings**

### **Docker Compose Status**
- **Created**: Container ready but not started
- **Up**: Container running successfully  
- **Up (healthy)**: Container running with health checks passing
- **Exited**: Container stopped (check logs)
- **Building**: Currently building image

### **Build Output**
- **CACHED**: Layer reused from previous build (fast!)
- **exporting to image**: Final stage, writing image to disk
- **=> exporting layers**: Individual layer export progress

## 🔧 **Troubleshooting Commands**

### **If Builds Seem Stuck**
```powershell
# Check Docker resource usage
docker system df

# Check available disk space  
Get-PSDrive C

# View detailed build logs
docker-compose logs --tail=50 recommendation-engine-service
```

### **If Services Won't Start**
```powershell
# Check for port conflicts
netstat -ano | findstr ":8001"
netstat -ano | findstr ":8002"

# Restart specific service
docker-compose restart recommendation-engine-service

# Force rebuild if needed
docker-compose up -d --build --force-recreate recommendation-engine-service
```

## 📊 **Success Metrics to Watch**

### **✅ Build Successful When:**
- All services show "Up" or "Up (healthy)" status
- No error messages in logs
- Services respond to health checks
- Docker images exist for all services
- Memory usage stabilizes

### **🎯 Expected Final State:**
```
NAME                     STATUS
aura_postgres           Up (healthy)
aura_redis              Up (healthy)  
aura_backend            Up (healthy)
aura-image-processing   Up (healthy)
aura-nlu                Up (healthy)
aura-style-profile      Up (healthy)
aura-combination-engine Up (healthy)
aura-recommendation     Up (healthy)
aura-orchestrator       Up (healthy)
aura-feedback-loop      Up (healthy)
```

---

**Current Estimate: 5-10 minutes until full completion**

*The export phase is the final step - your AI services are almost ready!*
