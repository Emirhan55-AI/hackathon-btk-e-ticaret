# 🔍 AURA AI - Monitoring & Health Check Script
# Bu script sistemin sağlık durumunu izler ve raporlar

param(
    [Parameter(Position=0)]
    [ValidateSet("status", "health", "metrics", "logs", "performance", "alerts", "report")]
    [string]$Action = "status",
    
    [string]$Service = "",
    [string]$Duration = "1h",
    [string]$OutputPath = "./monitoring-reports",
    [switch]$Watch = $false,
    [switch]$Detailed = $false,
    [switch]$Export = $false,
    [switch]$Help = $false
)

# Script bilgileri
$ScriptVersion = "1.0.0"
$ScriptName = "AURA AI Monitoring & Health Check"

# Renkli output için fonksiyonlar
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Blue }
function Write-Header { param($Message) Write-Host "`n🔍 $Message" -ForegroundColor Cyan }
function Write-Metric { param($Name, $Value, $Unit = "", $Status = "INFO") 
    $icon = switch ($Status) {
        "GOOD" { "✅" }
        "WARNING" { "⚠️" }
        "CRITICAL" { "🚨" }
        default { "📊" }
    }
    $color = switch ($Status) {
        "GOOD" { "Green" }
        "WARNING" { "Yellow" }
        "CRITICAL" { "Red" }
        default { "White" }
    }
    Write-Host "   $icon $Name`: $Value$Unit" -ForegroundColor $color
}

# Help gösterimi
if ($Help) {
    Write-Host "`n$ScriptName v$ScriptVersion" -ForegroundColor Green
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bu script AURA AI sisteminin sağlık durumunu izler ve raporlar." -ForegroundColor White
    Write-Host ""
    Write-Host "KULLANIM:" -ForegroundColor Yellow
    Write-Host "  .\scripts\monitor.ps1 [ACTION] [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "ACTIONS:" -ForegroundColor Yellow
    Write-Host "  status        Genel sistem durumu (default)" -ForegroundColor White
    Write-Host "  health        Detaylı sağlık kontrolü" -ForegroundColor White
    Write-Host "  metrics       Performance metrikleri" -ForegroundColor White
    Write-Host "  logs          Son logları göster" -ForegroundColor White
    Write-Host "  performance   Performance analizi" -ForegroundColor White
    Write-Host "  alerts        Aktif alertleri göster" -ForegroundColor White
    Write-Host "  report        Detaylı rapor oluştur" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Service         Belirli bir servisi izle" -ForegroundColor White
    Write-Host "  -Duration        Metriklerin zaman aralığı (5m, 1h, 24h)" -ForegroundColor White
    Write-Host "  -OutputPath      Rapor çıktı dizini" -ForegroundColor White
    Write-Host "  -Watch           Sürekli izleme modu" -ForegroundColor White
    Write-Host "  -Detailed        Detaylı bilgi göster" -ForegroundColor White
    Write-Host "  -Export          Sonuçları dosyaya aktar" -ForegroundColor White
    Write-Host ""
    Write-Host "ÖRNEKLER:" -ForegroundColor Yellow
    Write-Host "  .\scripts\monitor.ps1 status -Detailed" -ForegroundColor White
    Write-Host "  .\scripts\monitor.ps1 health -Service image-processing" -ForegroundColor White
    Write-Host "  .\scripts\monitor.ps1 metrics -Duration 24h -Export" -ForegroundColor White
    Write-Host "  .\scripts\monitor.ps1 status -Watch" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Header "$ScriptName v$ScriptVersion"
Write-Host "===========================================" -ForegroundColor Green

# Servis konfigürasyonu
$services = @{
    "orchestrator" = @{
        "name" = "Orchestrator"
        "url" = "http://localhost:8007"
        "port" = 8007
        "container" = "aura-orchestrator-dev"
    }
    "image-processing" = @{
        "name" = "Image Processing"
        "url" = "http://localhost:8001"
        "port" = 8001
        "container" = "aura-image-processing-dev"
    }
    "nlu-service" = @{
        "name" = "NLU Service"
        "url" = "http://localhost:8002"
        "port" = 8002
        "container" = "aura-nlu-dev"
    }
    "style-profile" = @{
        "name" = "Style Profile"
        "url" = "http://localhost:8003"
        "port" = 8003
        "container" = "aura-style-profile-dev"
    }
    "combination-engine" = @{
        "name" = "Combination Engine"
        "url" = "http://localhost:8004"
        "port" = 8004
        "container" = "aura-combination-engine-dev"
    }
    "recommendation-engine" = @{
        "name" = "Recommendation Engine"
        "url" = "http://localhost:8005"
        "port" = 8005
        "container" = "aura-recommendation-engine-dev"
    }
    "feedback-loop" = @{
        "name" = "Feedback Loop"
        "url" = "http://localhost:8006"
        "port" = 8006
        "container" = "aura-feedback-loop-dev"
    }
}

$infrastructure = @{
    "postgres" = @{
        "name" = "PostgreSQL"
        "container" = "aura-postgres-dev"
        "port" = 5432
    }
    "redis" = @{
        "name" = "Redis"
        "container" = "aura-redis-dev"
        "port" = 6379
    }
    "prometheus" = @{
        "name" = "Prometheus"
        "url" = "http://localhost:9090"
        "container" = "aura-prometheus-dev"
        "port" = 9090
    }
    "grafana" = @{
        "name" = "Grafana"
        "url" = "http://localhost:3000"
        "container" = "aura-grafana-dev"
        "port" = 3000
    }
}

# Utility fonksiyonlar
function Test-ServiceHealth {
    param($ServiceConfig)
    
    try {
        if ($ServiceConfig.url) {
            $response = Invoke-RestMethod -Uri "$($ServiceConfig.url)/health" -Method Get -TimeoutSec 10 -ErrorAction Stop
            return @{
                "status" = if ($response.status -eq "healthy") { "HEALTHY" } else { "UNHEALTHY" }
                "response_time" = (Measure-Command { Invoke-RestMethod -Uri "$($ServiceConfig.url)/health" -Method Get -TimeoutSec 5 }).TotalMilliseconds
                "details" = $response
            }
        } else {
            # Container durumunu kontrol et
            $containerStatus = (docker ps --filter "name=$($ServiceConfig.container)" --format "{{.Status}}" 2>$null)
            if ($containerStatus -and $containerStatus.StartsWith("Up")) {
                return @{
                    "status" = "HEALTHY"
                    "details" = @{ "container_status" = $containerStatus }
                }
            } else {
                return @{
                    "status" = "UNHEALTHY"
                    "details" = @{ "container_status" = $containerStatus }
                }
            }
        }
    } catch {
        return @{
            "status" = "UNREACHABLE"
            "error" = $_.Exception.Message
        }
    }
}

function Get-ContainerStats {
    param($ContainerName)
    
    try {
        $stats = (docker stats $ContainerName --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" 2>$null)
        if ($stats) {
            $lines = $stats -split "`n"
            if ($lines.Length -gt 1) {
                $data = $lines[1] -split "`t"
                return @{
                    "cpu_percent" = $data[0] -replace "%", ""
                    "memory_usage" = $data[1]
                    "network_io" = $data[2]
                    "block_io" = $data[3]
                }
            }
        }
        return $null
    } catch {
        return $null
    }
}

function Get-SystemMetrics {
    try {
        # CPU bilgisi
        $cpu = Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property LoadPercentage -Average
        
        # Memory bilgisi
        $memory = Get-CimInstance -ClassName Win32_OperatingSystem
        $totalMemory = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
        $freeMemory = [math]::Round($memory.FreePhysicalMemory / 1MB, 2)
        $usedMemory = $totalMemory - $freeMemory
        $memoryPercent = [math]::Round(($usedMemory / $totalMemory) * 100, 2)
        
        # Disk bilgisi
        $disk = Get-CimInstance -ClassName Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | Select-Object -First 1
        $diskPercent = [math]::Round((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100, 2)
        
        return @{
            "cpu_percent" = $cpu.Average
            "memory_percent" = $memoryPercent
            "memory_used_gb" = $usedMemory
            "memory_total_gb" = $totalMemory
            "disk_percent" = $diskPercent
            "disk_free_gb" = [math]::Round($disk.FreeSpace / 1GB, 2)
            "disk_total_gb" = [math]::Round($disk.Size / 1GB, 2)
        }
    } catch {
        return @{
            "error" = "Sistem metrikleri alınamadı: $($_.Exception.Message)"
        }
    }
}

function Get-ServiceLogs {
    param($ServiceName, $Lines = 50)
    
    try {
        $containerName = $services[$ServiceName].container
        if ($containerName) {
            $logs = (docker logs $containerName --tail $Lines 2>&1)
            return $logs
        }
        return "Container bulunamadı"
    } catch {
        return "Loglar alınamadı: $($_.Exception.Message)"
    }
}

function Show-ServiceStatus {
    param($ServiceName = "")
    
    Write-Header "Servis Durumu Raporu"
    
    if ($ServiceName -and $services.ContainsKey($ServiceName)) {
        $serviceList = @{ $ServiceName = $services[$ServiceName] }
    } else {
        $serviceList = $services
    }
    
    $healthyCount = 0
    $totalCount = $serviceList.Count
    
    foreach ($service in $serviceList.GetEnumerator()) {
        $config = $service.Value
        $health = Test-ServiceHealth -ServiceConfig $config
        
        Write-Host "`n📡 $($config.name)" -ForegroundColor Cyan
        
        switch ($health.status) {
            "HEALTHY" {
                Write-Metric "Status" "Healthy" "" "GOOD"
                $healthyCount++
                
                if ($health.response_time) {
                    $responseStatus = if ($health.response_time -lt 500) { "GOOD" } elseif ($health.response_time -lt 2000) { "WARNING" } else { "CRITICAL" }
                    Write-Metric "Response Time" $health.response_time "ms" $responseStatus
                }
            }
            "UNHEALTHY" {
                Write-Metric "Status" "Unhealthy" "" "CRITICAL"
            }
            "UNREACHABLE" {
                Write-Metric "Status" "Unreachable" "" "CRITICAL"
                if ($health.error) {
                    Write-Host "     Error: $($health.error)" -ForegroundColor Red
                }
            }
        }
        
        # Container stats
        if ($config.container) {
            $stats = Get-ContainerStats -ContainerName $config.container
            if ($stats) {
                $cpuStatus = if ([float]$stats.cpu_percent -lt 50) { "GOOD" } elseif ([float]$stats.cpu_percent -lt 80) { "WARNING" } else { "CRITICAL" }
                Write-Metric "CPU Usage" $stats.cpu_percent "%" $cpuStatus
                Write-Metric "Memory" $stats.memory_usage
                Write-Metric "Network I/O" $stats.network_io
            }
        }
        
        if ($Detailed -and $health.details) {
            Write-Host "     Details:" -ForegroundColor Gray
            $health.details | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor Gray
        }
    }
    
    Write-Host "`n📊 Özet" -ForegroundColor Cyan
    Write-Metric "Sağlıklı Servis" "$healthyCount/$totalCount"
    
    $overallStatus = if ($healthyCount -eq $totalCount) { "GOOD" } elseif ($healthyCount -gt 0) { "WARNING" } else { "CRITICAL" }
    Write-Metric "Genel Durum" $(if ($overallStatus -eq "GOOD") { "Excellent" } elseif ($overallStatus -eq "WARNING") { "Degraded" } else { "Critical" }) "" $overallStatus
}

function Show-InfrastructureStatus {
    Write-Header "Infrastructure Durumu"
    
    foreach ($infra in $infrastructure.GetEnumerator()) {
        $config = $infra.Value
        Write-Host "`n🏗️  $($config.name)" -ForegroundColor Cyan
        
        $health = Test-ServiceHealth -ServiceConfig $config
        
        switch ($health.status) {
            "HEALTHY" {
                Write-Metric "Status" "Healthy" "" "GOOD"
                
                if ($health.response_time) {
                    $responseStatus = if ($health.response_time -lt 500) { "GOOD" } elseif ($health.response_time -lt 2000) { "WARNING" } else { "CRITICAL" }
                    Write-Metric "Response Time" $health.response_time "ms" $responseStatus
                }
            }
            "UNHEALTHY" {
                Write-Metric "Status" "Unhealthy" "" "CRITICAL"
            }
            "UNREACHABLE" {
                Write-Metric "Status" "Unreachable" "" "CRITICAL"
            }
        }
        
        # Container stats
        if ($config.container) {
            $stats = Get-ContainerStats -ContainerName $config.container
            if ($stats) {
                $cpuStatus = if ([float]$stats.cpu_percent -lt 50) { "GOOD" } elseif ([float]$stats.cpu_percent -lt 80) { "WARNING" } else { "CRITICAL" }
                Write-Metric "CPU Usage" $stats.cpu_percent "%" $cpuStatus
                Write-Metric "Memory" $stats.memory_usage
            }
        }
    }
}

function Show-SystemMetrics {
    Write-Header "Sistem Metrikleri"
    
    $metrics = Get-SystemMetrics
    
    if ($metrics.error) {
        Write-Error $metrics.error
        return
    }
    
    Write-Host "`n💻 Host System" -ForegroundColor Cyan
    
    $cpuStatus = if ($metrics.cpu_percent -lt 50) { "GOOD" } elseif ($metrics.cpu_percent -lt 80) { "WARNING" } else { "CRITICAL" }
    Write-Metric "CPU Usage" $metrics.cpu_percent "%" $cpuStatus
    
    $memStatus = if ($metrics.memory_percent -lt 70) { "GOOD" } elseif ($metrics.memory_percent -lt 90) { "WARNING" } else { "CRITICAL" }
    Write-Metric "Memory Usage" $metrics.memory_percent "%" $memStatus
    Write-Metric "Memory Used" "$($metrics.memory_used_gb)GB / $($metrics.memory_total_gb)GB"
    
    $diskStatus = if ($metrics.disk_percent -lt 80) { "GOOD" } elseif ($metrics.disk_percent -lt 95) { "WARNING" } else { "CRITICAL" }
    Write-Metric "Disk Usage" $metrics.disk_percent "%" $diskStatus
    Write-Metric "Disk Free" "$($metrics.disk_free_gb)GB / $($metrics.disk_total_gb)GB"
}

function Show-RecentLogs {
    param($ServiceName = "", $Lines = 20)
    
    Write-Header "Son Loglar"
    
    if ($ServiceName -and $services.ContainsKey($ServiceName)) {
        Write-Host "`n📋 $($services[$ServiceName].name) Logs" -ForegroundColor Cyan
        $logs = Get-ServiceLogs -ServiceName $ServiceName -Lines $Lines
        Write-Host $logs -ForegroundColor White
    } else {
        foreach ($service in $services.Keys) {
            Write-Host "`n📋 $($services[$service].name) Logs (Son 10 satır)" -ForegroundColor Cyan
            $logs = Get-ServiceLogs -ServiceName $service -Lines 10
            Write-Host $logs -ForegroundColor White
            Write-Host "─" * 80 -ForegroundColor Gray
        }
    }
}

function Show-Alerts {
    Write-Header "Aktif Alertler"
    
    $alerts = @()
    
    # Servis health check alertleri
    foreach ($service in $services.GetEnumerator()) {
        $health = Test-ServiceHealth -ServiceConfig $service.Value
        if ($health.status -ne "HEALTHY") {
            $alerts += @{
                "type" = "SERVICE_DOWN"
                "service" = $service.Value.name
                "severity" = "CRITICAL"
                "message" = "Service is $($health.status.ToLower())"
                "timestamp" = Get-Date
            }
        }
    }
    
    # Sistem metrikleri alertleri
    $metrics = Get-SystemMetrics
    if (-not $metrics.error) {
        if ($metrics.cpu_percent -gt 80) {
            $alerts += @{
                "type" = "HIGH_CPU"
                "severity" = "WARNING"
                "message" = "CPU usage is high: $($metrics.cpu_percent)%"
                "timestamp" = Get-Date
            }
        }
        
        if ($metrics.memory_percent -gt 90) {
            $alerts += @{
                "type" = "HIGH_MEMORY"
                "severity" = "CRITICAL"
                "message" = "Memory usage is critical: $($metrics.memory_percent)%"
                "timestamp" = Get-Date
            }
        }
        
        if ($metrics.disk_percent -gt 95) {
            $alerts += @{
                "type" = "HIGH_DISK"
                "severity" = "CRITICAL"
                "message" = "Disk usage is critical: $($metrics.disk_percent)%"
                "timestamp" = Get-Date
            }
        }
    }
    
    if ($alerts.Count -eq 0) {
        Write-Success "Aktif alert bulunamadı! 🎉"
    } else {
        foreach ($alert in $alerts) {
            $icon = if ($alert.severity -eq "CRITICAL") { "🚨" } else { "⚠️" }
            $color = if ($alert.severity -eq "CRITICAL") { "Red" } else { "Yellow" }
            
            Write-Host "`n$icon $($alert.type)" -ForegroundColor $color
            Write-Host "   Severity: $($alert.severity)" -ForegroundColor $color
            Write-Host "   Message: $($alert.message)" -ForegroundColor White
            Write-Host "   Time: $($alert.timestamp.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
            
            if ($alert.service) {
                Write-Host "   Service: $($alert.service)" -ForegroundColor White
            }
        }
    }
}

function Export-MonitoringReport {
    param($Data, $FileName)
    
    if (-not (Test-Path $OutputPath)) {
        New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filePath = Join-Path $OutputPath "$FileName`_$timestamp.json"
    
    $Data | ConvertTo-Json -Depth 10 | Out-File -FilePath $filePath -Encoding UTF8
    Write-Success "Rapor dışa aktarıldı: $filePath"
}

# Ana monitoring loop
function Start-MonitoringLoop {
    Write-Header "Sürekli İzleme Modu Başlatıldı"
    Write-Info "Çıkmak için Ctrl+C tuşlayın..."
    
    try {
        while ($true) {
            Clear-Host
            Write-Header "AURA AI Monitoring Dashboard - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            
            Show-ServiceStatus -ServiceName $Service
            Show-SystemMetrics
            
            if ($Detailed) {
                Show-InfrastructureStatus
            }
            
            Start-Sleep -Seconds 30
        }
    } catch {
        Write-Info "İzleme durduruldu."
    }
}

# Ana action switch
switch ($Action.ToLower()) {
    "status" {
        if ($Watch) {
            Start-MonitoringLoop
        } else {
            Show-ServiceStatus -ServiceName $Service
            Show-SystemMetrics
            
            if ($Export) {
                $statusData = @{
                    "timestamp" = Get-Date
                    "services" = @{}
                    "system_metrics" = Get-SystemMetrics
                }
                
                foreach ($service in $services.GetEnumerator()) {
                    $statusData.services[$service.Key] = Test-ServiceHealth -ServiceConfig $service.Value
                }
                
                Export-MonitoringReport -Data $statusData -FileName "status_report"
            }
        }
    }
    
    "health" {
        Show-ServiceStatus -ServiceName $Service
        Show-InfrastructureStatus
        Show-Alerts
    }
    
    "metrics" {
        Show-SystemMetrics
        
        if ($Detailed) {
            Write-Header "Container Metrikleri"
            
            foreach ($service in $services.GetEnumerator()) {
                if ($Service -and $service.Key -ne $Service) { continue }
                
                $stats = Get-ContainerStats -ContainerName $service.Value.container
                if ($stats) {
                    Write-Host "`n📊 $($service.Value.name)" -ForegroundColor Cyan
                    Write-Metric "CPU" $stats.cpu_percent "%"
                    Write-Metric "Memory" $stats.memory_usage
                    Write-Metric "Network I/O" $stats.network_io
                    Write-Metric "Block I/O" $stats.block_io
                }
            }
        }
    }
    
    "logs" {
        Show-RecentLogs -ServiceName $Service
    }
    
    "performance" {
        Write-Header "Performance Analizi"
        
        # API response time testi
        foreach ($service in $services.GetEnumerator()) {
            if ($Service -and $service.Key -ne $Service) { continue }
            
            if ($service.Value.url) {
                Write-Host "`n⚡ $($service.Value.name) Performance" -ForegroundColor Cyan
                
                $times = @()
                for ($i = 1; $i -le 5; $i++) {
                    try {
                        $responseTime = (Measure-Command { 
                            Invoke-RestMethod -Uri "$($service.Value.url)/health" -Method Get -TimeoutSec 10 
                        }).TotalMilliseconds
                        $times += $responseTime
                        Write-Host "   Test $i`: $([math]::Round($responseTime, 2))ms" -ForegroundColor White
                    } catch {
                        Write-Host "   Test $i`: Failed" -ForegroundColor Red
                    }
                }
                
                if ($times.Count -gt 0) {
                    $avgTime = ($times | Measure-Object -Average).Average
                    $minTime = ($times | Measure-Object -Minimum).Minimum
                    $maxTime = ($times | Measure-Object -Maximum).Maximum
                    
                    Write-Metric "Average" "$([math]::Round($avgTime, 2))" "ms"
                    Write-Metric "Min" "$([math]::Round($minTime, 2))" "ms"
                    Write-Metric "Max" "$([math]::Round($maxTime, 2))" "ms"
                }
            }
        }
    }
    
    "alerts" {
        Show-Alerts
    }
    
    "report" {
        Write-Header "Detaylı Sistem Raporu Oluşturuluyor..."
        
        $reportData = @{
            "timestamp" = Get-Date
            "system_info" = @{
                "hostname" = $env:COMPUTERNAME
                "os" = (Get-CimInstance Win32_OperatingSystem).Caption
                "powershell_version" = $PSVersionTable.PSVersion.ToString()
            }
            "services" = @{}
            "infrastructure" = @{}
            "system_metrics" = Get-SystemMetrics
            "alerts" = @()
        }
        
        # Servis durumları
        foreach ($service in $services.GetEnumerator()) {
            $health = Test-ServiceHealth -ServiceConfig $service.Value
            $stats = Get-ContainerStats -ContainerName $service.Value.container
            
            $reportData.services[$service.Key] = @{
                "health" = $health
                "stats" = $stats
                "config" = $service.Value
            }
        }
        
        # Infrastructure durumları
        foreach ($infra in $infrastructure.GetEnumerator()) {
            $health = Test-ServiceHealth -ServiceConfig $infra.Value
            $reportData.infrastructure[$infra.Key] = @{
                "health" = $health
                "config" = $infra.Value
            }
        }
        
        # Raporu göster
        Show-ServiceStatus
        Show-InfrastructureStatus
        Show-SystemMetrics
        Show-Alerts
        
        # Export
        Export-MonitoringReport -Data $reportData -FileName "comprehensive_report"
        
        Write-Success "Kapsamlı sistem raporu oluşturuldu!"
    }
    
    default {
        Write-Error "Geçersiz action: $Action"
        Write-Warning "Kullanılabilir action'lar: status, health, metrics, logs, performance, alerts, report"
        Write-Info "Yardım için: .\scripts\monitor.ps1 -Help"
        exit 1
    }
}

Write-Host ""
Write-Success "Monitoring scripti tamamlandı! 📊"
