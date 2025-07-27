# Aura AI Services Health Check Script
# This script tests all AI services to determine their operational status

Write-Host "🔍 Checking Aura AI Services Status..." -ForegroundColor Cyan
Write-Host $("=" * 50)

# Define all AI services with their expected ports
$services = @(
    @{Name="Image Processing"; Port=8001; Endpoint="http://localhost:8001"},
    @{Name="NLU Service"; Port=8002; Endpoint="http://localhost:8002"},
    @{Name="Style Profile"; Port=8003; Endpoint="http://localhost:8003"},
    @{Name="Combination Engine"; Port=8004; Endpoint="http://localhost:8004"},
    @{Name="Recommendation Engine"; Port=8005; Endpoint="http://localhost:8005"},
    @{Name="Orchestrator"; Port=8006; Endpoint="http://localhost:8006"},
    @{Name="Feedback Loop"; Port=8007; Endpoint="http://localhost:8007"}
)

# Core services
$coreServices = @(
    @{Name="E-commerce Backend"; Port=8000; Endpoint="http://localhost:8000/health"},
    @{Name="PostgreSQL Database"; Port=5432; Endpoint=""},
    @{Name="Redis Cache"; Port=6379; Endpoint=""}
)

Write-Host "`n🎯 Core Infrastructure Status:" -ForegroundColor Yellow
foreach ($service in $coreServices) {
    Write-Host "Testing $($service.Name)..." -NoNewline
    
    if ($service.Endpoint -ne "") {
        try {
            $response = Invoke-WebRequest -Uri $service.Endpoint -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host " ✅ OPERATIONAL" -ForegroundColor Green
            } else {
                Write-Host " ⚠️ RESPONDING ($($response.StatusCode))" -ForegroundColor Yellow
            }
        } catch {
            Write-Host " ❌ NOT RESPONDING" -ForegroundColor Red
        }
    } else {
        # For database services, just check if port is listening
        try {
            $connection = New-Object System.Net.Sockets.TcpClient
            $connection.Connect("localhost", $service.Port)
            $connection.Close()
            Write-Host " ✅ OPERATIONAL" -ForegroundColor Green
        } catch {
            Write-Host " ❌ NOT RESPONDING" -ForegroundColor Red
        }
    }
}

Write-Host "`n🤖 AI Services Status:" -ForegroundColor Yellow
$operationalCount = 0
foreach ($service in $services) {
    Write-Host "Testing $($service.Name) (Port $($service.Port))..." -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri $service.Endpoint -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host " ✅ OPERATIONAL" -ForegroundColor Green
            $operationalCount++
        } else {
            Write-Host " ⚠️ RESPONDING ($($response.StatusCode))" -ForegroundColor Yellow
        }
    } catch {
        Write-Host " ❌ NOT RESPONDING" -ForegroundColor Red
    }
}

Write-Host "`n📊 Summary:" -ForegroundColor Cyan
Write-Host "AI Services Operational: $operationalCount/7" -ForegroundColor White

if ($operationalCount -eq 7) {
    Write-Host "🎉 ALL AI SERVICES ARE FULLY OPERATIONAL!" -ForegroundColor Green
    Write-Host "✅ Complete system integration achieved" -ForegroundColor Green
} elseif ($operationalCount -ge 4) {
    Write-Host "🔄 PARTIAL INTEGRATION - Some services still starting" -ForegroundColor Yellow
} else {
    Write-Host "⚠️ SYSTEM STARTING - Most services still initializing" -ForegroundColor Red
}

Write-Host "`n🔗 Quick Access URLs:" -ForegroundColor Cyan
Write-Host "E-commerce Platform: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Image Processing: http://localhost:8001" -ForegroundColor White
Write-Host "NLU Service: http://localhost:8002" -ForegroundColor White
Write-Host "Style Profile: http://localhost:8003" -ForegroundColor White
Write-Host "Combination Engine: http://localhost:8004" -ForegroundColor White
Write-Host "Recommendation Engine: http://localhost:8005" -ForegroundColor White
Write-Host "Orchestrator: http://localhost:8006" -ForegroundColor White
Write-Host "Feedback Loop: http://localhost:8007" -ForegroundColor White

Write-Host "`n$("=" * 50)"
Write-Host "Run this script anytime to check service status!" -ForegroundColor Cyan
