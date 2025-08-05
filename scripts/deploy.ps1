# 🚀 AURA AI - Deployment Script
# Bu script AURA AI sisteminin development environment'ını başlatır

param(
    [Parameter(Position=0)]
    [ValidateSet("up", "down", "restart", "logs", "status", "clean", "test")]
    [string]$Action = "up",
    
    [switch]$Build = $false,
    [switch]$Force = $false,
    [switch]$Detach = $true,
    [string]$Service = "",
    [switch]$Help = $false
)

# Script bilgileri
$ScriptVersion = "1.0.0"
$ScriptName = "AURA AI Development Deployment"

# Renkli output için fonksiyonlar
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Blue }
function Write-Header { param($Message) Write-Host "`n🚀 $Message" -ForegroundColor Cyan }

# Help gösterimi
if ($Help) {
    Write-Host "`n$ScriptName v$ScriptVersion" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bu script AURA AI mikroservis sistemini Docker Compose ile yönetir." -ForegroundColor White
    Write-Host ""
    Write-Host "KULLANIM:" -ForegroundColor Yellow
    Write-Host "  .\scripts\deploy.ps1 [ACTION] [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "ACTIONS:" -ForegroundColor Yellow
    Write-Host "  up        Servisleri başlat (default)" -ForegroundColor White
    Write-Host "  down      Servisleri durdur" -ForegroundColor White
    Write-Host "  restart   Servisleri yeniden başlat" -ForegroundColor White
    Write-Host "  logs      Servis loglarını göster" -ForegroundColor White
    Write-Host "  status    Servis durumlarını kontrol et" -ForegroundColor White
    Write-Host "  clean     Docker sistemini temizle" -ForegroundColor White
    Write-Host "  test      Servislerin sağlık kontrolünü yap" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Build         Container'ları yeniden build et" -ForegroundColor White
    Write-Host "  -Force         Zorla yeniden oluştur" -ForegroundColor White
    Write-Host "  -Service       Belirli bir servisle işlem yap" -ForegroundColor White
    Write-Host "  -Help          Bu yardım metnini göster" -ForegroundColor White
    Write-Host ""
    Write-Host "ÖRNEKLER:" -ForegroundColor Yellow
    Write-Host "  .\scripts\deploy.ps1 up -Build" -ForegroundColor White
    Write-Host "  .\scripts\deploy.ps1 logs -Service image-processing" -ForegroundColor White
    Write-Host "  .\scripts\deploy.ps1 down -Force" -ForegroundColor White
    Write-Host "  .\scripts\deploy.ps1 status" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Header "$ScriptName v$ScriptVersion"
Write-Host "============================================" -ForegroundColor Green

# Environment kontrolleri
Write-Info "Sistem gereksinimleri kontrol ediliyor..."

# Docker kontrolü
try {
    $dockerVersion = (docker --version 2>$null)
    if ($dockerVersion) {
        Write-Success "Docker yüklü: $dockerVersion"
    } else {
        throw "Docker bulunamadı"
    }
} catch {
    Write-Error "Docker yüklü değil veya çalışmıyor!"
    Write-Warning "Lütfen Docker Desktop'ı yükleyip başlatın."
    exit 1
}

# Docker Compose kontrolü
try {
    $composeVersion = (docker compose version 2>$null)
    if ($composeVersion) {
        Write-Success "Docker Compose yüklü: $composeVersion"
    } else {
        throw "Docker Compose bulunamadı"
    }
} catch {
    Write-Error "Docker Compose yüklü değil!"
    exit 1
}

# Environment dosyası kontrolü
$envFile = ".env.development"
if (-not (Test-Path $envFile)) {
    Write-Warning "Environment dosyası bulunamadı: $envFile"
    Write-Info "Default environment dosyası oluşturuluyor..."
    
    if (Test-Path "environments\.env.development") {
        Copy-Item "environments\.env.development" $envFile
        Write-Success "Environment dosyası oluşturuldu"
    } else {
        Write-Error "Default environment template bulunamadı!"
        Write-Warning "Lütfen .env.development dosyasını manuel olarak oluşturun."
        exit 1
    }
}

# Docker Compose dosyası kontrolü
$composeFile = "docker-compose.dev.yml"
if (-not (Test-Path $composeFile)) {
    Write-Error "Docker Compose dosyası bulunamadı: $composeFile"
    exit 1
}

# Service URL'leri tanımla
$services = @{
    "Orchestrator" = "http://localhost:8007"
    "Image Processing" = "http://localhost:8001"
    "NLU Service" = "http://localhost:8002"
    "Style Profile" = "http://localhost:8003"
    "Combination Engine" = "http://localhost:8004"
    "Recommendation Engine" = "http://localhost:8005"
    "Feedback Loop" = "http://localhost:8006"
}

$monitoringServices = @{
    "Prometheus" = "http://localhost:9090"
    "Grafana" = "http://localhost:3000"
}

# Health check fonksiyonu
function Test-ServiceHealth {
    param($ServiceName, $Url)
    
    try {
        $response = Invoke-RestMethod -Uri "$Url/health" -Method Get -TimeoutSec 10 -ErrorAction Stop
        if ($response.status -eq "healthy") {
            Write-Host "   ✅ $ServiceName" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ⚠️  $ServiceName - Status: $($response.status)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "   ❌ $ServiceName - Unreachable" -ForegroundColor Red
        return $false
    }
}

# Ana action switch
switch ($Action.ToLower()) {
    "up" {
        Write-Header "AURA AI servisleri başlatılıyor..."
        
        # Docker Compose argumentları hazırla
        $composeArgs = @("-f", $composeFile, "up")
        
        if ($Detach) {
            $composeArgs += "-d"
        }
        
        if ($Build) {
            $composeArgs += "--build"
            Write-Info "Container'lar yeniden build edilecek..."
        }
        
        if ($Force) {
            $composeArgs += "--force-recreate"
            Write-Warning "Tüm container'lar zorla yeniden oluşturulacak..."
        }
        
        if ($Service) {
            $composeArgs += $Service
            Write-Info "Sadece '$Service' servisi başlatılacak..."
        }
        
        # Docker Compose çalıştır
        Write-Info "Docker Compose komutu çalıştırılıyor..."
        & docker compose $composeArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Servisler başarıyla başlatıldı!"
            
            if ($Detach) {
                Start-Sleep -Seconds 5
                Write-Header "Servis URL'leri:"
                
                foreach ($service in $services.GetEnumerator()) {
                    Write-Host "   $($service.Key): " -NoNewline -ForegroundColor White
                    Write-Host "$($service.Value)" -ForegroundColor Cyan
                }
                
                Write-Host ""
                Write-Header "Monitoring Dashboard'ları:"
                foreach ($monitor in $monitoringServices.GetEnumerator()) {
                    Write-Host "   $($monitor.Key): " -NoNewline -ForegroundColor White
                    Write-Host "$($monitor.Value)" -ForegroundColor Cyan
                }
                
                Write-Host ""
                Write-Info "Servis durumunu kontrol etmek için: .\scripts\deploy.ps1 status"
                Write-Info "Logları görmek için: .\scripts\deploy.ps1 logs"
            }
        } else {
            Write-Error "Servis başlatma başarısız!"
            Write-Warning "Hataları kontrol etmek için logları inceleyiniz."
            exit 1
        }
    }
    
    "down" {
        Write-Header "AURA AI servisleri durduruluyor..."
        
        $downArgs = @("-f", $composeFile, "down")
        
        if ($Force) {
            $downArgs += "-v"
            Write-Warning "Volume'lar da silinecek!"
        }
        
        if ($Service) {
            Write-Error "Belirli servis durdurma desteklenmiyor. Tüm servisler durdurulacak."
        }
        
        & docker compose $downArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Servisler başarıyla durduruldu!"
            
            if ($Force) {
                Write-Success "Volume'lar da temizlendi!"
            }
        } else {
            Write-Error "Servis durdurma başarısız!"
            exit 1
        }
    }
    
    "restart" {
        Write-Header "AURA AI servisleri yeniden başlatılıyor..."
        
        if ($Service) {
            Write-Info "Sadece '$Service' servisi yeniden başlatılacak..."
            & docker compose -f $composeFile restart $Service
        } else {
            & docker compose -f $composeFile restart
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Servisler başarıyla yeniden başlatıldı!"
        } else {
            Write-Error "Servis yeniden başlatma başarısız!"
            exit 1
        }
    }
    
    "logs" {
        Write-Header "Servis logları görüntüleniyor..."
        
        $logArgs = @("-f", $composeFile, "logs", "-f", "--tail=100")
        
        if ($Service) {
            $logArgs += $Service
            Write-Info "Sadece '$Service' servisinin logları gösteriliyor..."
        } else {
            Write-Info "Tüm servislerin logları gösteriliyor... (Ctrl+C ile çıkış)"
        }
        
        & docker compose $logArgs
    }
    
    "status" {
        Write-Header "Servis durumları kontrol ediliyor..."
        
        # Docker container durumları
        Write-Info "Container durumları:"
        & docker compose -f $composeFile ps
        
        Write-Host ""
        Write-Header "Health Check Sonuçları:"
        
        $healthyCount = 0
        $totalCount = $services.Count
        
        foreach ($service in $services.GetEnumerator()) {
            if (Test-ServiceHealth -ServiceName $service.Key -Url $service.Value) {
                $healthyCount++
            }
            Start-Sleep -Milliseconds 500  # Rate limiting için bekle
        }
        
        Write-Host ""
        Write-Header "Monitoring Servisleri:"
        foreach ($monitor in $monitoringServices.GetEnumerator()) {
            try {
                $response = Invoke-WebRequest -Uri $monitor.Value -Method Head -TimeoutSec 5 -ErrorAction Stop
                Write-Host "   ✅ $($monitor.Key)" -ForegroundColor Green
            } catch {
                Write-Host "   ❌ $($monitor.Key) - Unreachable" -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Header "Sistem Özeti:"
        Write-Host "   Sağlıklı Servis: $healthyCount/$totalCount" -ForegroundColor $(if ($healthyCount -eq $totalCount) { "Green" } else { "Yellow" })
        
        if ($healthyCount -eq $totalCount) {
            Write-Success "Tüm servisler sağlıklı çalışıyor! 🎉"
        } elseif ($healthyCount -gt 0) {
            Write-Warning "Bazı servisler çalışmıyor. Logları kontrol edin."
        } else {
            Write-Error "Hiçbir servis çalışmıyor!"
        }
    }
    
    "test" {
        Write-Header "Sistem entegrasyon testleri çalıştırılıyor..."
        
        # Önce servis durumlarını kontrol et
        $allHealthy = $true
        foreach ($service in $services.GetEnumerator()) {
            if (-not (Test-ServiceHealth -ServiceName $service.Key -Url $service.Value)) {
                $allHealthy = $false
            }
        }
        
        if (-not $allHealthy) {
            Write-Error "Bazı servisler sağlıklı değil. Önce servisleri başlatın."
            exit 1
        }
        
        Write-Success "Tüm servisler sağlıklı!"
        
        # Basit API testleri
        Write-Info "Temel API testleri çalıştırılıyor..."
        
        try {
            # Orchestrator workflow test
            Write-Host "   Testing Orchestrator..." -NoNewline
            $response = Invoke-RestMethod -Uri "http://localhost:8007/health" -Method Get
            Write-Host " ✅" -ForegroundColor Green
            
            # Image Processing test
            Write-Host "   Testing Image Processing..." -NoNewline
            $response = Invoke-RestMethod -Uri "http://localhost:8001/models" -Method Get
            Write-Host " ✅" -ForegroundColor Green
            
            Write-Success "Temel API testleri başarılı!"
            
        } catch {
            Write-Error "API testleri başarısız: $($_.Exception.Message)"
            exit 1
        }
    }
    
    "clean" {
        Write-Header "Docker sistem temizliği yapılıyor..."
        
        Write-Warning "Bu işlem tüm AURA AI container'larını, image'larını ve volume'larını silecek!"
        $confirm = Read-Host "Devam etmek istediğinizden emin misiniz? (y/N)"
        
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            Write-Info "Servisler durduruluyor..."
            & docker compose -f $composeFile down -v --rmi all
            
            Write-Info "Docker sistem temizliği..."
            & docker system prune -f
            
            Write-Info "Kullanılmayan volume'lar temizleniyor..."
            & docker volume prune -f
            
            Write-Info "Kullanılmayan network'ler temizleniyor..."
            & docker network prune -f
            
            Write-Success "Sistem temizliği tamamlandı!"
        } else {
            Write-Info "İşlem iptal edildi."
        }
    }
    
    default {
        Write-Error "Geçersiz action: $Action"
        Write-Warning "Kullanılabilir action'lar: up, down, restart, logs, status, clean, test"
        Write-Info "Yardım için: .\scripts\deploy.ps1 -Help"
        exit 1
    }
}

Write-Host ""
Write-Success "Script başarıyla tamamlandı! 🎉"
