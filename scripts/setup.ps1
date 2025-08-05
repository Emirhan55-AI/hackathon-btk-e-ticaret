# 🔧 AURA AI - Development Setup Script
# Bu script geliştirme ortamını otomatik olarak kurar

param(
    [switch]$FullSetup = $false,
    [switch]$SkipDocker = $false,
    [switch]$SkipPython = $false,
    [switch]$SkipDatabase = $false,
    [switch]$Force = $false,
    [string]$PythonVersion = "3.11",
    [switch]$Help = $false
)

# Script bilgileri
$ScriptVersion = "1.0.0"
$ScriptName = "AURA AI Development Setup"

# Renkli output için fonksiyonlar
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Blue }
function Write-Header { param($Message) Write-Host "`n🔧 $Message" -ForegroundColor Cyan }
function Write-Step { param($Step, $Message) Write-Host "[$Step] $Message" -ForegroundColor Magenta }

# Help gösterimi
if ($Help) {
    Write-Host "`n$ScriptName v$ScriptVersion" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bu script AURA AI geliştirme ortamını otomatik olarak kurar." -ForegroundColor White
    Write-Host ""
    Write-Host "KULLANIM:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup.ps1 [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -FullSetup       Tam kurulum (tüm bileşenler)" -ForegroundColor White
    Write-Host "  -SkipDocker      Docker kurulumunu atla" -ForegroundColor White
    Write-Host "  -SkipPython      Python kurulumunu atla" -ForegroundColor White
    Write-Host "  -SkipDatabase    Database kurulumunu atla" -ForegroundColor White
    Write-Host "  -Force           Mevcut kurulumları zorla güncelle" -ForegroundColor White
    Write-Host "  -PythonVersion   Python versiyonu (default: 3.11)" -ForegroundColor White
    Write-Host "  -Help            Bu yardım metnini göster" -ForegroundColor White
    Write-Host ""
    Write-Host "ÖRNEKLER:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup.ps1 -FullSetup" -ForegroundColor White
    Write-Host "  .\scripts\setup.ps1 -SkipDocker -PythonVersion 3.10" -ForegroundColor White
    Write-Host "  .\scripts\setup.ps1 -Force" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Header "$ScriptName v$ScriptVersion"
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Sistem bilgilerini kontrol et
Write-Step "1" "Sistem bilgileri kontrol ediliyor..."

$isWindows = $PSVersionTable.PSVersion.Major -ge 6 -and $IsWindows
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

Write-Info "İşletim Sistemi: Windows"
Write-Info "PowerShell Versiyonu: $($PSVersionTable.PSVersion)"

if (-not $isAdmin) {
    Write-Warning "Script yönetici yetkisi ile çalışmıyor!"
    Write-Info "Bazı kurulumlar için yönetici yetkisi gerekebilir."
}

# Temel dizinleri kontrol et
Write-Step "2" "Proje yapısı kontrol ediliyor..."

$requiredDirs = @(
    "services",
    "shared", 
    "tests",
    "docs",
    "scripts",
    "environments"
)

foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir)) {
        Write-Warning "Dizin bulunamadı: $dir"
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Success "Dizin oluşturuldu: $dir"
    } else {
        Write-Success "Dizin mevcut: $dir"
    }
}

# Python kurulumu kontrol et
if (-not $SkipPython) {
    Write-Step "3" "Python kurulumu kontrol ediliyor..."
    
    try {
        $pythonCmd = Get-Command python -ErrorAction Stop
        $currentVersion = (python --version 2>&1) -replace "Python ", ""
        Write-Success "Python yüklü: $currentVersion"
        
        # Version kontrolü
        $major, $minor = $currentVersion.Split('.')[0,1]
        $requiredMajor, $requiredMinor = $PythonVersion.Split('.')[0,1]
        
        if ([int]$major -lt [int]$requiredMajor -or ([int]$major -eq [int]$requiredMajor -and [int]$minor -lt [int]$requiredMinor)) {
            Write-Warning "Python versiyonu çok eski! Gereken: $PythonVersion+, Mevcut: $currentVersion"
            
            if ($Force) {
                Write-Info "Python güncellemesi önerilir."
            }
        }
        
    } catch {
        Write-Error "Python yüklü değil!"
        Write-Info "Python $PythonVersion indirip yükleyin: https://python.org/downloads/"
        
        if ($FullSetup) {
            Write-Info "Chocolatey ile Python yüklemeye çalışılıyor..."
            try {
                if (Get-Command choco -ErrorAction SilentlyContinue) {
                    & choco install python --version=$PythonVersion -y
                    Write-Success "Python başarıyla yüklendi!"
                } else {
                    Write-Warning "Chocolatey bulunamadı. Manuel Python yüklemesi gerekli."
                }
            } catch {
                Write-Error "Python yüklenemedi: $($_.Exception.Message)"
            }
        }
    }
}

# Virtual Environment kurulumu
Write-Step "4" "Virtual Environment kurulumu..."

if (Test-Path "venv") {
    if ($Force) {
        Write-Warning "Mevcut virtual environment siliniyor..."
        Remove-Item -Recurse -Force "venv"
    } else {
        Write-Success "Virtual environment mevcut"
    }
}

if (-not (Test-Path "venv") -or $Force) {
    Write-Info "Virtual environment oluşturuluyor..."
    
    try {
        & python -m venv venv
        Write-Success "Virtual environment oluşturuldu"
    } catch {
        Write-Error "Virtual environment oluşturulamadı: $($_.Exception.Message)"
        exit 1
    }
}

# Virtual environment aktifleştir
Write-Info "Virtual environment aktifleştiriliyor..."
try {
    & .\venv\Scripts\Activate.ps1
    Write-Success "Virtual environment aktifleştirildi"
} catch {
    Write-Error "Virtual environment aktifleştirilemedi!"
    exit 1
}

# Python dependencies yükle
Write-Step "5" "Python dependencies yükleniyor..."

$requirementFiles = @(
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-shared.txt"
)

foreach ($reqFile in $requirementFiles) {
    if (Test-Path $reqFile) {
        Write-Info "$reqFile yükleniyor..."
        try {
            & pip install -r $reqFile
            Write-Success "$reqFile başarıyla yüklendi"
        } catch {
            Write-Error "$reqFile yüklenemedi: $($_.Exception.Message)"
        }
    } else {
        Write-Warning "$reqFile bulunamadı"
    }
}

# Pre-commit hooks kurulumu
Write-Step "6" "Pre-commit hooks kurulumu..."

try {
    $precommitInstalled = (pip show pre-commit 2>$null)
    if (-not $precommitInstalled) {
        Write-Info "Pre-commit yükleniyor..."
        & pip install pre-commit
    }
    
    Write-Info "Pre-commit hooks kuruluyor..."
    & pre-commit install
    Write-Success "Pre-commit hooks kuruldu"
    
    # İlk çalıştırma
    Write-Info "Pre-commit hooks test ediliyor..."
    & pre-commit run --all-files
    
} catch {
    Write-Warning "Pre-commit hooks kurulamadı: $($_.Exception.Message)"
}

# Docker kurulumu kontrol et
if (-not $SkipDocker) {
    Write-Step "7" "Docker kurulumu kontrol ediliyor..."
    
    try {
        $dockerVersion = (docker --version 2>$null)
        if ($dockerVersion) {
            Write-Success "Docker yüklü: $dockerVersion"
            
            # Docker Compose kontrolü
            $composeVersion = (docker compose version 2>$null)
            if ($composeVersion) {
                Write-Success "Docker Compose yüklü: $composeVersion"
            } else {
                Write-Warning "Docker Compose bulunamadı!"
            }
            
            # Docker çalışıyor mu kontrol et
            try {
                & docker ps 2>$null | Out-Null
                Write-Success "Docker daemon çalışıyor"
            } catch {
                Write-Warning "Docker daemon çalışmıyor! Docker Desktop'ı başlatın."
            }
            
        } else {
            throw "Docker bulunamadı"
        }
        
    } catch {
        Write-Error "Docker yüklü değil!"
        Write-Info "Docker Desktop indirip yükleyin: https://docker.com/products/docker-desktop"
        
        if ($FullSetup) {
            Write-Info "Chocolatey ile Docker yüklemeye çalışılıyor..."
            try {
                if (Get-Command choco -ErrorAction SilentlyContinue) {
                    & choco install docker-desktop -y
                    Write-Success "Docker Desktop yüklendi! Bilgisayarı yeniden başlatın."
                } else {
                    Write-Warning "Chocolatey bulunamadı. Manuel Docker yüklemesi gerekli."
                }
            } catch {
                Write-Error "Docker yüklenemedi: $($_.Exception.Message)"
            }
        }
    }
}

# Environment dosyaları kurulumu
Write-Step "8" "Environment dosyaları kurulumu..."

$envFiles = @{
    ".env.development" = "environments\.env.development"
    ".env.test" = "environments\.env.test"
    ".env.staging" = "environments\.env.staging"
}

foreach ($envFile in $envFiles.GetEnumerator()) {
    $targetFile = $envFile.Key
    $sourceFile = $envFile.Value
    
    if (-not (Test-Path $targetFile) -or $Force) {
        if (Test-Path $sourceFile) {
            Copy-Item $sourceFile $targetFile
            Write-Success "Environment dosyası oluşturuldu: $targetFile"
        } else {
            Write-Warning "Template bulunamadı: $sourceFile"
            
            # Basic template oluştur
            $basicEnv = @"
# AURA AI Environment Configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://aura_dev:dev_password@localhost:5432/aura_ai_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET_KEY=development-secret-key-change-in-production
JWT_ALGORITHM=HS256

# AI Models
ENABLE_AI_MODELS=false
AI_MODEL_PATH=./models/dev
"@
            $basicEnv | Out-File -FilePath $targetFile -Encoding UTF8
            Write-Success "Basic environment dosyası oluşturuldu: $targetFile"
        }
    } else {
        Write-Success "Environment dosyası mevcut: $targetFile"
    }
}

# Database kurulumu
if (-not $SkipDatabase) {
    Write-Step "9" "Database kurulumu..."
    
    # PostgreSQL Docker container başlat
    try {
        $existingContainer = (docker ps -a --filter "name=aura-postgres-dev" --format "{{.Names}}" 2>$null)
        
        if ($existingContainer) {
            Write-Info "Mevcut PostgreSQL container bulundu"
            
            # Container çalışıyor mu kontrol et
            $runningContainer = (docker ps --filter "name=aura-postgres-dev" --format "{{.Names}}" 2>$null)
            
            if ($runningContainer) {
                Write-Success "PostgreSQL container çalışıyor"
            } else {
                Write-Info "PostgreSQL container başlatılıyor..."
                & docker start aura-postgres-dev
                Write-Success "PostgreSQL container başlatıldı"
            }
        } else {
            Write-Info "PostgreSQL container oluşturuluyor..."
            
            & docker run -d `
                --name aura-postgres-dev `
                -e POSTGRES_DB=aura_ai_dev `
                -e POSTGRES_USER=aura_dev `
                -e POSTGRES_PASSWORD=dev_password `
                -p 5432:5432 `
                postgres:15
            
            Write-Success "PostgreSQL container oluşturuldu ve başlatıldı"
            
            # Container'ın hazır olmasını bekle
            Write-Info "PostgreSQL'in hazır olması bekleniyor..."
            Start-Sleep -Seconds 10
        }
        
        # Redis container başlat
        $existingRedis = (docker ps -a --filter "name=aura-redis-dev" --format "{{.Names}}" 2>$null)
        
        if ($existingRedis) {
            $runningRedis = (docker ps --filter "name=aura-redis-dev" --format "{{.Names}}" 2>$null)
            
            if (-not $runningRedis) {
                & docker start aura-redis-dev
                Write-Success "Redis container başlatıldı"
            } else {
                Write-Success "Redis container çalışıyor"
            }
        } else {
            Write-Info "Redis container oluşturuluyor..."
            
            & docker run -d `
                --name aura-redis-dev `
                -p 6379:6379 `
                redis:7-alpine
            
            Write-Success "Redis container oluşturuldu ve başlatıldı"
        }
        
    } catch {
        Write-Error "Database container'ları başlatılamadı: $($_.Exception.Message)"
        Write-Warning "Manuel olarak Docker container'larını başlatmanız gerekebilir."
    }
    
    # Database migration
    Write-Info "Database migration kontrol ediliyor..."
    
    if (Test-Path "alembic.ini") {
        try {
            # Alembic yüklü mü kontrol et
            $alembicInstalled = (pip show alembic 2>$null)
            if (-not $alembicInstalled) {
                Write-Info "Alembic yükleniyor..."
                & pip install alembic
            }
            
            Write-Info "Database migration çalıştırılıyor..."
            Start-Sleep -Seconds 5  # Database'in hazır olması için bekle
            
            & alembic upgrade head
            Write-Success "Database migration tamamlandı"
            
        } catch {
            Write-Warning "Database migration başarısız: $($_.Exception.Message)"
            Write-Info "Migration'ı manuel olarak çalıştırmanız gerekebilir: alembic upgrade head"
        }
    } else {
        Write-Warning "alembic.ini bulunamadı. Database migration atlandı."
    }
}

# Git hooks kurulumu
Write-Step "10" "Git konfigürasyonu..."

if (Test-Path ".git") {
    Write-Success "Git repository mevcut"
    
    # Git kullanıcı bilgileri kontrol et
    try {
        $gitUser = (git config user.name 2>$null)
        $gitEmail = (git config user.email 2>$null)
        
        if (-not $gitUser -or -not $gitEmail) {
            Write-Warning "Git kullanıcı bilgileri eksik!"
            Write-Info "Git kullanıcı bilgilerini ayarlayın:"
            Write-Info "  git config user.name 'Your Name'"
            Write-Info "  git config user.email 'your.email@example.com'"
        } else {
            Write-Success "Git kullanıcı: $gitUser <$gitEmail>"
        }
    } catch {
        Write-Warning "Git konfigürasyonu okunamadı"
    }
} else {
    Write-Warning "Git repository bulunamadı!"
    Write-Info "Git repository başlatmak için: git init"
}

# Test kurulumu doğrula
Write-Step "11" "Test kurulumu doğrulanıyor..."

try {
    $pytestInstalled = (pip show pytest 2>$null)
    if ($pytestInstalled) {
        Write-Success "Pytest yüklü"
        
        # Test dizinleri kontrol et
        $testDirs = @("tests/unit", "tests/integration", "tests/e2e")
        foreach ($testDir in $testDirs) {
            if (-not (Test-Path $testDir)) {
                New-Item -ItemType Directory -Path $testDir -Force | Out-Null
                Write-Success "Test dizini oluşturuldu: $testDir"
            }
        }
        
        # conftest.py kontrol et
        if (-not (Test-Path "tests/conftest.py")) {
            $conftestContent = @"
"""
AURA AI Test Configuration
Global pytest configuration and fixtures
"""

import pytest
import asyncio
from typing import Generator

# Async test support
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Test environment setup
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    print("\n🧪 Setting up test environment...")
    yield
    print("\n🧹 Cleaning up test environment...")
"@
            $conftestContent | Out-File -FilePath "tests/conftest.py" -Encoding UTF8
            Write-Success "conftest.py oluşturuldu"
        }
        
    } else {
        Write-Warning "Pytest yüklü değil!"
        & pip install pytest pytest-asyncio pytest-cov
        Write-Success "Pytest yüklendi"
    }
} catch {
    Write-Error "Test kurulumu başarısız: $($_.Exception.Message)"
}

# Development scripts kurulumu
Write-Step "12" "Development scripts kontrol ediliyor..."

$devScripts = @{
    "deploy.ps1" = "Deployment script"
    "test.ps1" = "Test runner script"
    "setup.ps1" = "Setup script (bu script)"
}

foreach ($script in $devScripts.GetEnumerator()) {
    $scriptPath = "scripts/$($script.Key)"
    if (Test-Path $scriptPath) {
        Write-Success "$($script.Value) mevcut"
    } else {
        Write-Warning "$($script.Value) bulunamadı: $scriptPath"
    }
}

# VS Code konfigürasyonu
Write-Step "13" "VS Code konfigürasyonu..."

if (-not (Test-Path ".vscode")) {
    New-Item -ItemType Directory -Path ".vscode" -Force | Out-Null
}

# VS Code settings
$vscodeSettings = @{
    "python.defaultInterpreterPath" = "./venv/Scripts/python.exe"
    "python.formatting.provider" = "black"
    "python.linting.enabled" = $true
    "python.linting.pylintEnabled" = $true
    "python.testing.pytestEnabled" = $true
    "python.testing.pytestPath" = "./venv/Scripts/pytest.exe"
    "files.associations" = @{
        "*.env*" = "properties"
    }
    "editor.formatOnSave" = $true
    "editor.codeActionsOnSave" = @{
        "source.organizeImports" = $true
    }
}

$settingsJson = $vscodeSettings | ConvertTo-Json -Depth 10
$settingsJson | Out-File -FilePath ".vscode/settings.json" -Encoding UTF8
Write-Success "VS Code settings oluşturuldu"

# Kurulum özeti
Write-Header "Kurulum Tamamlandı! 🎉"
Write-Host "==========================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Kurulum Özeti:" -ForegroundColor Cyan
Write-Host "   ✅ Proje dizin yapısı" -ForegroundColor Green
Write-Host "   ✅ Virtual Environment" -ForegroundColor Green
Write-Host "   ✅ Python Dependencies" -ForegroundColor Green
Write-Host "   ✅ Environment dosyaları" -ForegroundColor Green

if (-not $SkipDocker) {
    Write-Host "   ✅ Docker container'ları" -ForegroundColor Green
}

if (-not $SkipDatabase) {
    Write-Host "   ✅ Database setup" -ForegroundColor Green
}

Write-Host "   ✅ Test konfigürasyonu" -ForegroundColor Green
Write-Host "   ✅ VS Code konfigürasyonu" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Sonraki Adımlar:" -ForegroundColor Yellow
Write-Host "   1. Servisleri başlat: .\scripts\deploy.ps1 up" -ForegroundColor White
Write-Host "   2. Testleri çalıştır: .\scripts\test.ps1 unit" -ForegroundColor White
Write-Host "   3. API dokümantasyonu: http://localhost:8007/docs" -ForegroundColor White
Write-Host "   4. Monitoring: http://localhost:3000 (Grafana)" -ForegroundColor White

Write-Host ""
Write-Success "AURA AI geliştirme ortamı hazır! Happy coding! 🎯"
