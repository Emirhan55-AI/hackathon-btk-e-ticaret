# 🧪 COMPREHENSIVE SERVICE HEALTH CHECK

$services = @(
    @{name="E-commerce Backend"; port=8000; endpoint="/health"},
    @{name="Image Processing"; port=8001; endpoint="/"},
    @{name="NLU Service"; port=8002; endpoint="/"},
    @{name="Style Profile"; port=8003; endpoint="/"},
    @{name="Combination Engine"; port=8004; endpoint="/"},
    @{name="Recommendation Engine"; port=8005; endpoint="/"},
    @{name="Orchestrator"; port=8006; endpoint="/"},
    @{name="Feedback Loop"; port=8007; endpoint="/"}
)

Write-Host "🚀 AURA AI SYSTEM HEALTH CHECK" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

$workingServices = 0
$totalServices = $services.Count

foreach ($service in $services) {
    $url = "http://localhost:$($service.port)$($service.endpoint)"
    
    try {
        $response = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 8
        Write-Host "✅ $($service.name) (Port $($service.port)): WORKING - HTTP $($response.StatusCode)" -ForegroundColor Green
        $workingServices++
    }
    catch {
        $errorMsg = $_.Exception.Message
        if ($errorMsg -like "*connection*closed*" -or $errorMsg -like "*bağlantı*kapatıldı*") {
            Write-Host "❌ $($service.name) (Port $($service.port)): CONNECTION REFUSED" -ForegroundColor Red
        }
        elseif ($errorMsg -like "*timeout*" -or $errorMsg -like "*zaman*") {
            Write-Host "⏱️ $($service.name) (Port $($service.port)): TIMEOUT" -ForegroundColor Yellow
        }
        else {
            Write-Host "❌ $($service.name) (Port $($service.port)): $errorMsg" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "📊 SYSTEM SUMMARY:" -ForegroundColor Cyan
$percentage = [math]::Round(($workingServices/$totalServices)*100, 1)
Write-Host "Working Services: $workingServices/$totalServices ($percentage%)" -ForegroundColor $(if($workingServices -ge 6){"Green"}elseif($workingServices -ge 4){"Yellow"}else{"Red"})

if ($workingServices -eq $totalServices) {
    Write-Host "🎉 ALL SERVICES OPERATIONAL! System is 100% ready!" -ForegroundColor Green
}
elseif ($workingServices -ge 6) {
    Write-Host "🌟 Excellent! Core system + most AI services working!" -ForegroundColor Green
}
elseif ($workingServices -ge 4) {
    Write-Host "✅ Good! Core system + some AI services operational!" -ForegroundColor Yellow
}
else {
    Write-Host "⚠️ Need attention: Several services require troubleshooting" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔗 Quick Test URLs:" -ForegroundColor Cyan
Write-Host "- E-commerce Platform: http://localhost:8000/docs" -ForegroundColor White
Write-Host "- Image Processing: http://localhost:8001/docs" -ForegroundColor White
Write-Host "- AI Services: http://localhost:8005/docs (Recommendations)" -ForegroundColor White
