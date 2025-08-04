# Aura AI Complete System - PowerShell Startup Script
# Advanced system initialization and management for Windows environments
# Built for BTK Hackathon 2025 - Complete AI-Powered E-Commerce Platform

param(
    [string]$Action = "start",
    [switch]$Build = $true,
    [switch]$Background = $true,
    [switch]$Health = $false,
    [switch]$Logs = $false,
    [string]$Service = ""
)

# Set console encoding for proper emoji and Unicode support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Define color functions for beautiful output
function Write-Header($text) {
    Write-Host "=" * 80 -ForegroundColor Cyan
    Write-Host $text -ForegroundColor Magenta
    Write-Host "=" * 80 -ForegroundColor Cyan
}

function Write-Success($text) {
    Write-Host "✅ $text" -ForegroundColor Green
}

function Write-Error($text) {
    Write-Host "❌ $text" -ForegroundColor Red
}

function Write-Warning($text) {
    Write-Host "⚠️ $text" -ForegroundColor Yellow
}

function Write-Info($text) {
    Write-Host "ℹ️ $text" -ForegroundColor Cyan
}

# Define all Aura AI services
$Services = @{
    'postgres' = @{
        Name = 'PostgreSQL Database'
        Port = 5432
        Container = 'aura_postgres'
        Description = 'Central database for e-commerce platform'
    }
    'redis' = @{
        Name = 'Redis Cache'
        Port = 6379
        Container = 'aura_redis'
        Description = 'High-performance caching layer'
    }
    'backend' = @{
        Name = 'E-Commerce Backend'
        Port = 8000
        Container = 'aura_backend'
        Description = 'Main e-commerce platform API'
        HealthUrl = 'http://localhost:8000/health'
    }
    'image-processing' = @{
        Name = 'Image Processing Service'
        Port = 8001
        Container = 'aura-image-processing'
        Description = 'Computer vision and image analysis AI'
        HealthUrl = 'http://localhost:8001/health'
    }
    'nlu' = @{
        Name = 'NLU Service'
        Port = 8002
        Container = 'aura-nlu'
        Description = 'Natural language understanding AI'
        HealthUrl = 'http://localhost:8002/health'
    }
    'style-profile' = @{
        Name = 'Style Profile Service'
        Port = 8003
        Container = 'aura-style-profile'
        Description = 'Advanced user style profiling AI'
        HealthUrl = 'http://localhost:8003/health'
    }
    'combination-engine' = @{
        Name = 'Combination Engine'
        Port = 8004
        Container = 'aura-combination-engine'
        Description = 'Intelligent outfit combination AI'
        HealthUrl = 'http://localhost:8004/health'
    }
    'recommendation-engine' = @{
        Name = 'Recommendation Engine'
        Port = 8005
        Container = 'aura-recommendation-engine'
        Description = 'FAISS-powered recommendation AI'
        HealthUrl = 'http://localhost:8005/health'
    }
    'orchestrator' = @{
        Name = 'Orchestrator Service'
        Port = 8006
        Container = 'aura-orchestrator'
        Description = 'Advanced workflow coordination'
        HealthUrl = 'http://localhost:8006/health'
    }
    'feedback-loop' = @{
        Name = 'Feedback Loop Service'
        Port = 8007
        Container = 'aura-feedback-loop'
        Description = 'Intelligent learning and adaptation'
        HealthUrl = 'http://localhost:8007/health'
    }
}

function Show-WelcomeBanner {
    Clear-Host
    Write-Header "🌟 AURA AI COMPLETE SYSTEM 🌟"
    Write-Host "Advanced AI-Powered E-Commerce Platform" -ForegroundColor Cyan
    Write-Host "BTK Hackathon 2025 - Full-Stack AI Integration" -ForegroundColor Green
    Write-Host "System initialized at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host ""
}

function Test-Prerequisites {
    Write-Info "Checking system prerequisites..."
    
    # Check Docker
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Write-Success "Docker available: $dockerVersion"
        } else {
            Write-Error "Docker not found. Please install Docker Desktop."
            return $false
        }
    } catch {
        Write-Error "Docker not accessible. Please ensure Docker is running."
        return $false
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version 2>$null
        if ($composeVersion) {
            Write-Success "Docker Compose available: $composeVersion"
        } else {
            Write-Error "Docker Compose not found."
            return $false
        }
    } catch {
        Write-Error "Docker Compose not accessible."
        return $false
    }
    
    # Check docker-compose.yml
    if (Test-Path "docker-compose.yml") {
        Write-Success "docker-compose.yml found"
    } else {
        Write-Error "docker-compose.yml not found in current directory"
        return $false
    }
    
    return $true
}

function Start-AuraSystem {
    param([bool]$BuildImages = $true, [bool]$RunInBackground = $true)
    
    Write-Info "Starting Aura AI Complete System..."
    
    # Build command
    $cmd = @('docker-compose', 'up')
    if ($RunInBackground) { $cmd += '-d' }
    if ($BuildImages) { $cmd += '--build' }
    
    Write-Host "Executing: $($cmd -join ' ')" -ForegroundColor Gray
    
    try {
        & $cmd[0] $cmd[1..($cmd.Length-1)]
        if ($LASTEXITCODE -eq 0) {
            Write-Success "System started successfully!"
            Write-Host "🎉 All services are starting up!" -ForegroundColor Green
            return $true
        } else {
            Write-Error "Failed to start system (Exit code: $LASTEXITCODE)"
            return $false
        }
    } catch {
        Write-Error "Error starting system: $_"
        return $false
    }
}

function Test-ServiceHealth {
    param([string]$ServiceKey, [hashtable]$ServiceInfo)
    
    if ($ServiceInfo.HealthUrl) {
        try {
            $startTime = Get-Date
            $response = Invoke-WebRequest -Uri $ServiceInfo.HealthUrl -TimeoutSec 10 -UseBasicParsing
            $responseTime = [math]::Round(((Get-Date) - $startTime).TotalMilliseconds, 2)
            
            if ($response.StatusCode -eq 200) {
                return @{
                    Status = 'Healthy'
                    ResponseTime = $responseTime
                    Details = "HTTP $($response.StatusCode)"
                }
            } else {
                return @{
                    Status = 'Unhealthy'
                    ResponseTime = $responseTime
                    Details = "HTTP $($response.StatusCode)"
                }
            }
        } catch {
            return @{
                Status = 'Error'
                ResponseTime = 0
                Details = $_.Exception.Message
            }
        }
    } else {
        # Check container status for services without HTTP health checks
        try {
            $containerStatus = docker ps --filter "name=$($ServiceInfo.Container)" --format "table {{.Status}}" 2>$null
            if ($containerStatus -match "Up") {
                return @{
                    Status = 'Healthy'
                    ResponseTime = 0
                    Details = 'Container running'
                }
            } else {
                return @{
                    Status = 'Unhealthy'
                    ResponseTime = 0
                    Details = 'Container not running'
                }
            }
        } catch {
            return @{
                Status = 'Unknown'
                ResponseTime = 0
                Details = 'Unable to check container'
            }
        }
    }
}

function Show-SystemHealth {
    Write-Info "Checking system health..."
    Write-Host ""
    
    # Table header
    $headerFormat = "{0,-25} {1,-12} {2,-12} {3}"
    Write-Host ($headerFormat -f "Service", "Status", "Response", "Description") -ForegroundColor Yellow
    Write-Host ("-" * 80) -ForegroundColor Gray
    
    $healthyCount = 0
    $totalCount = $Services.Count
    
    foreach ($serviceKey in $Services.Keys) {
        $serviceInfo = $Services[$serviceKey]
        $healthResult = Test-ServiceHealth -ServiceKey $serviceKey -ServiceInfo $serviceInfo
        
        # Determine status display and color
        $statusColor = switch ($healthResult.Status) {
            'Healthy' { 'Green'; $healthyCount++; "✅ Healthy" }
            'Unhealthy' { 'Red'; "❌ Unhealthy" }
            'Error' { 'Yellow'; "⚠️ Error" }
            default { 'Gray'; "❓ Unknown" }
        }
        
        $responseTime = if ($healthResult.ResponseTime -gt 0) { "$($healthResult.ResponseTime)ms" } else { "N/A" }
        
        Write-Host ($headerFormat -f $serviceInfo.Name, $statusColor[1], $responseTime, $serviceInfo.Description) -ForegroundColor $statusColor[0]
    }
    
    Write-Host ("-" * 80) -ForegroundColor Gray
    
    # System summary
    $healthPercentage = ($healthyCount / $totalCount) * 100
    $summaryText = "System Status: $healthyCount/$totalCount services healthy ($([math]::Round($healthPercentage, 1))%)"
    
    $summaryColor = switch ($healthPercentage) {
        {$_ -eq 100} { 'Green'; "🎉 Perfect! $summaryText" }
        {$_ -ge 80} { 'Green'; "✅ Good - $summaryText" }
        {$_ -ge 60} { 'Yellow'; "⚠️ Degraded - $summaryText" }
        default { 'Red'; "❌ Critical - $summaryText" }
    }
    
    Write-Host $summaryColor[1] -ForegroundColor $summaryColor[0]
    Write-Host ""
    
    return $healthPercentage
}

function Show-AccessInformation {
    Write-Info "System Access Information:"
    Write-Host ""
    
    $accessFormat = "{0,-25} {1,-35} {2}"
    Write-Host ($accessFormat -f "Component", "URL", "Purpose") -ForegroundColor Yellow
    Write-Host ("-" * 80) -ForegroundColor Gray
    
    $accessInfo = @(
        @("E-Commerce Platform", "http://localhost:8000", "Main shopping platform")
        @("AI Orchestrator", "http://localhost:8006", "AI workflow coordination")
        @("Image Analysis AI", "http://localhost:8001", "Computer vision analysis")
        @("Language AI", "http://localhost:8002", "Natural language processing")
        @("Style Profiling AI", "http://localhost:8003", "User style analysis")
        @("Combination AI", "http://localhost:8004", "Outfit generation")
        @("Recommendation AI", "http://localhost:8005", "Product recommendations")
        @("Learning AI", "http://localhost:8007", "Feedback processing")
        @("System Monitor", "http://localhost:8080", "System dashboard")
    )
    
    foreach ($info in $accessInfo) {
        Write-Host ($accessFormat -f $info[0], $info[1], $info[2]) -ForegroundColor Cyan
    }
    
    Write-Host ("-" * 80) -ForegroundColor Gray
    Write-Host "📚 API Documentation: Add '/docs' to any service URL" -ForegroundColor Green
    Write-Host ""
}

function Show-ManagementCommands {
    Write-Info "System Management Commands:"
    Write-Host ""
    
    $commands = @(
        @("Health Check", ".\start_aura.ps1 -Health", "Check all service health")
        @("Start System", ".\start_aura.ps1 -Action start", "Start all services")
        @("Stop System", ".\start_aura.ps1 -Action stop", "Stop all services")
        @("View Logs", ".\start_aura.ps1 -Logs -Service [name]", "View service logs")
        @("System Status", "docker-compose ps", "Check container status")
        @("Restart Service", "docker-compose restart [service]", "Restart specific service")
        @("Scale Service", "docker-compose up --scale [service]=3", "Scale specific service")
        @("Remove All Data", "docker-compose down -v", "Clear all volumes")
    )
    
    $cmdFormat = "{0,-20} {1,-40} {2}"
    Write-Host ($cmdFormat -f "Command", "Usage", "Description") -ForegroundColor Yellow
    Write-Host ("-" * 80) -ForegroundColor Gray
    
    foreach ($cmd in $commands) {
        Write-Host ($cmdFormat -f $cmd[0], $cmd[1], $cmd[2]) -ForegroundColor White
    }
    
    Write-Host ""
}

function Stop-AuraSystem {
    Write-Info "Stopping Aura AI Complete System..."
    
    try {
        docker-compose down
        if ($LASTEXITCODE -eq 0) {
            Write-Success "System stopped successfully!"
            return $true
        } else {
            Write-Error "Failed to stop system (Exit code: $LASTEXITCODE)"
            return $false
        }
    } catch {
        Write-Error "Error stopping system: $_"
        return $false
    }
}

function Show-ServiceLogs {
    param([string]$ServiceName = "")
    
    if ($ServiceName) {
        Write-Info "Showing logs for service: $ServiceName"
        docker-compose logs -f $ServiceName
    } else {
        Write-Info "Showing logs for all services"
        docker-compose logs -f
    }
}

# Main execution logic
function Main {
    Show-WelcomeBanner
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        Write-Error "Prerequisites not met. Please install Docker Desktop and try again."
        exit 1
    }
    
    # Handle different actions
    switch ($Action.ToLower()) {
        "start" {
            Write-Info "Starting complete system initialization..."
            
            if (Start-AuraSystem -BuildImages $Build -RunInBackground $Background) {
                if ($Background) {
                    Write-Warning "Waiting for services to initialize (30 seconds)..."
                    Start-Sleep -Seconds 30
                }
                
                $healthPercentage = Show-SystemHealth
                Show-AccessInformation
                
                if ($healthPercentage -ge 80) {
                    Write-Success "🎉 System is ready! All AI services are operational."
                } else {
                    Write-Warning "⚠️ System started but some services may need more time to initialize."
                }
                
                Show-ManagementCommands
                
                Write-Host ""
                Write-Host "🌟 Aura AI Complete System is now running!" -ForegroundColor Magenta
                Write-Host "🌐 Access the main platform at: http://localhost:8000" -ForegroundColor Cyan
                Write-Host "🤖 Access AI services at: http://localhost:8006" -ForegroundColor Cyan
            }
        }
        
        "stop" {
            Stop-AuraSystem
        }
        
        "status" {
            Show-SystemHealth | Out-Null
        }
        
        "restart" {
            Write-Info "Restarting Aura AI System..."
            Stop-AuraSystem
            Start-Sleep -Seconds 5
            Start-AuraSystem -BuildImages $false -RunInBackground $Background
        }
        
        default {
            Write-Error "Unknown action: $Action"
            Write-Host "Available actions: start, stop, status, restart" -ForegroundColor Yellow
            Show-ManagementCommands
        }
    }
    
    # Handle additional flags
    if ($Health) {
        Show-SystemHealth | Out-Null
    }
    
    if ($Logs) {
        Show-ServiceLogs -ServiceName $Service
    }
}

# Execute main function
Main
