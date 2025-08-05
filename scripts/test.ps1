# 🧪 AURA AI - Test Runner Script
# Bu script AURA AI sisteminin tüm testlerini çalıştırır

param(
    [Parameter(Position=0)]
    [ValidateSet("all", "unit", "integration", "e2e", "performance", "ai", "api")]
    [string]$TestType = "all",
    
    [string]$Service = "",
    [string]$TestPattern = "",
    [switch]$Coverage = $false,
    [switch]$Verbose = $false,
    [switch]$Parallel = $false,
    [switch]$StopOnFail = $false,
    [string]$OutputFormat = "terminal",
    [string]$ReportPath = "./test-reports",
    [switch]$Help = $false
)

# Script bilgileri
$ScriptVersion = "1.0.0"
$ScriptName = "AURA AI Test Runner"

# Renkli output için fonksiyonlar
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Blue }
function Write-Header { param($Message) Write-Host "`n🧪 $Message" -ForegroundColor Cyan }
function Write-TestResult { param($Message, $Status) 
    $icon = if ($Status -eq "PASS") { "✅" } elseif ($Status -eq "FAIL") { "❌" } else { "⚠️" }
    $color = if ($Status -eq "PASS") { "Green" } elseif ($Status -eq "FAIL") { "Red" } else { "Yellow" }
    Write-Host "   $icon $Message" -ForegroundColor $color
}

# Help gösterimi
if ($Help) {
    Write-Host "`n$ScriptName v$ScriptVersion" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Bu script AURA AI sisteminin testlerini çalıştırır ve raporlar." -ForegroundColor White
    Write-Host ""
    Write-Host "KULLANIM:" -ForegroundColor Yellow
    Write-Host "  .\scripts\test.ps1 [TEST_TYPE] [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "TEST TYPES:" -ForegroundColor Yellow
    Write-Host "  all           Tüm testleri çalıştır (default)" -ForegroundColor White
    Write-Host "  unit          Unit testler" -ForegroundColor White
    Write-Host "  integration   Integration testler" -ForegroundColor White
    Write-Host "  e2e           End-to-end testler" -ForegroundColor White
    Write-Host "  performance   Performance testleri" -ForegroundColor White
    Write-Host "  ai            AI model testleri" -ForegroundColor White
    Write-Host "  api           API endpoint testleri" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Service         Belirli bir servisin testlerini çalıştır" -ForegroundColor White
    Write-Host "  -TestPattern     Test dosya pattern'i (örn: '*auth*')" -ForegroundColor White
    Write-Host "  -Coverage        Code coverage raporu oluştur" -ForegroundColor White
    Write-Host "  -Verbose         Detaylı çıktı" -ForegroundColor White
    Write-Host "  -Parallel        Paralel test çalıştırma" -ForegroundColor White
    Write-Host "  -StopOnFail      İlk hatada dur" -ForegroundColor White
    Write-Host "  -OutputFormat    Rapor formatı (terminal, json, html)" -ForegroundColor White
    Write-Host "  -ReportPath      Rapor dizini" -ForegroundColor White
    Write-Host ""
    Write-Host "ÖRNEKLER:" -ForegroundColor Yellow
    Write-Host "  .\scripts\test.ps1 unit -Service image-processing -Coverage" -ForegroundColor White
    Write-Host "  .\scripts\test.ps1 e2e -Verbose" -ForegroundColor White
    Write-Host "  .\scripts\test.ps1 all -Parallel -OutputFormat html" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Header "$ScriptName v$ScriptVersion"
Write-Host "==========================================" -ForegroundColor Green

# Test environment hazırlığı
Write-Info "Test environment hazırlanıyor..."

# Python ve pytest kontrolü
try {
    $pythonVersion = (python --version 2>$null)
    if ($pythonVersion) {
        Write-Success "Python yüklü: $pythonVersion"
    } else {
        throw "Python bulunamadı"
    }
} catch {
    Write-Error "Python yüklü değil!"
    exit 1
}

# Virtual environment kontrolü
if ($env:VIRTUAL_ENV) {
    Write-Success "Virtual environment aktif: $env:VIRTUAL_ENV"
} else {
    Write-Warning "Virtual environment aktif değil!"
    Write-Info "Virtual environment aktifleştiriliyor..."
    
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
        Write-Success "Virtual environment aktifleştirildi"
    } else {
        Write-Error "Virtual environment bulunamadı! Önce 'python -m venv venv' çalıştırın."
        exit 1
    }
}

# Test dependencies kontrolü
Write-Info "Test dependencies kontrol ediliyor..."
$testDeps = @("pytest", "pytest-asyncio", "pytest-cov", "pytest-html", "pytest-xdist")

foreach ($dep in $testDeps) {
    try {
        $installed = (pip show $dep 2>$null)
        if ($installed) {
            Write-Success "$dep yüklü"
        } else {
            Write-Warning "$dep yüklü değil, yükleniyor..."
            pip install $dep
        }
    } catch {
        Write-Error "$dep yüklenemedi!"
        exit 1
    }
}

# Test environment dosyası kontrolü
$testEnvFile = ".env.test"
if (-not (Test-Path $testEnvFile)) {
    Write-Warning "Test environment dosyası bulunamadı: $testEnvFile"
    if (Test-Path "environments\.env.test") {
        Copy-Item "environments\.env.test" $testEnvFile
        Write-Success "Test environment dosyası oluşturuldu"
    } else {
        Write-Warning "Default test environment template bulunamadı!"
    }
}

# Report dizini oluştur
if (-not (Test-Path $ReportPath)) {
    New-Item -ItemType Directory -Path $ReportPath -Force | Out-Null
    Write-Success "Report dizini oluşturuldu: $ReportPath"
}

# Test konfigürasyonları
$services = @(
    "orchestrator",
    "image_processing", 
    "nlu_service",
    "style_profile",
    "combination_engine",
    "recommendation_engine",
    "feedback_loop"
)

$testCategories = @{
    "unit" = @{
        "path" = "tests/unit"
        "marker" = "unit"
        "description" = "Unit Tests"
    }
    "integration" = @{
        "path" = "tests/integration"
        "marker" = "integration"
        "description" = "Integration Tests"
    }
    "e2e" = @{
        "path" = "tests/e2e"
        "marker" = "e2e"
        "description" = "End-to-End Tests"
    }
    "performance" = @{
        "path" = "tests/performance"
        "marker" = "slow"
        "description" = "Performance Tests"
    }
    "ai" = @{
        "path" = "tests/ai"
        "marker" = "ai_model"
        "description" = "AI Model Tests"
    }
    "api" = @{
        "path" = "tests/api"
        "marker" = "api"
        "description" = "API Tests"
    }
}

# Pytest argumentları oluştur
function Build-PytestArgs {
    param($Category, $ServiceName = "", $Pattern = "")
    
    $args = @("pytest")
    
    # Test yolu
    if ($Category -and $testCategories.ContainsKey($Category)) {
        $testPath = $testCategories[$Category].path
        
        if ($ServiceName) {
            $testPath = "$testPath/$ServiceName"
        }
        
        if (Test-Path $testPath) {
            $args += $testPath
        } else {
            Write-Warning "Test path bulunamadı: $testPath"
        }
    }
    
    # Test pattern
    if ($Pattern) {
        $args += "-k", $Pattern
    }
    
    # Marker
    if ($Category -and $testCategories[$Category].marker) {
        $args += "-m", $testCategories[$Category].marker
    }
    
    # Verbose
    if ($Verbose) {
        $args += "-v"
    } else {
        $args += "-q"
    }
    
    # Stop on fail
    if ($StopOnFail) {
        $args += "-x"
    }
    
    # Parallel execution
    if ($Parallel) {
        $args += "-n", "auto"
    }
    
    # Coverage
    if ($Coverage) {
        $args += "--cov=services", "--cov=shared"
        $args += "--cov-report=html:$ReportPath/coverage"
        $args += "--cov-report=xml:$ReportPath/coverage.xml"
        $args += "--cov-report=term-missing"
    }
    
    # Output format
    switch ($OutputFormat.ToLower()) {
        "json" {
            $args += "--json-report", "--json-report-file=$ReportPath/report.json"
        }
        "html" {
            $args += "--html=$ReportPath/report.html", "--self-contained-html"
        }
        "xml" {
            $args += "--junitxml=$ReportPath/junit.xml"
        }
    }
    
    return $args
}

# Test database hazırlama
function Setup-TestDatabase {
    Write-Info "Test database hazırlanıyor..."
    
    try {
        # Test database oluştur
        & docker run -d --name aura-test-db `
            -e POSTGRES_DB=aura_ai_test `
            -e POSTGRES_USER=test_user `
            -e POSTGRES_PASSWORD=test_pass `
            -p 5433:5432 `
            postgres:15 2>$null
        
        Start-Sleep -Seconds 10
        
        # Migration çalıştır
        $env:DATABASE_URL = "postgresql://test_user:test_pass@localhost:5433/aura_ai_test"
        & alembic upgrade head
        
        Write-Success "Test database hazırlandı"
        return $true
    } catch {
        Write-Warning "Test database hazırlanamadı: $($_.Exception.Message)"
        return $false
    }
}

# Test database temizleme
function Cleanup-TestDatabase {
    Write-Info "Test database temizleniyor..."
    
    try {
        & docker stop aura-test-db 2>$null
        & docker rm aura-test-db 2>$null
        Write-Success "Test database temizlendi"
    } catch {
        Write-Warning "Test database temizlenemedi"
    }
}

# Test çalıştırma fonksiyonu
function Run-Tests {
    param($Category, $ServiceName = "")
    
    $categoryInfo = if ($Category) { $testCategories[$Category] } else { $null }
    $displayName = if ($categoryInfo) { $categoryInfo.description } else { "All Tests" }
    
    if ($ServiceName) {
        $displayName += " - $ServiceName"
    }
    
    Write-Header "Çalıştırılıyor: $displayName"
    
    # Test yolu kontrolü
    $testPath = if ($categoryInfo) { $categoryInfo.path } else { "tests/" }
    if ($ServiceName) {
        $testPath = "$testPath/$ServiceName"
    }
    
    if (-not (Test-Path $testPath)) {
        Write-Warning "Test dosyası bulunamadı: $testPath"
        return @{ "status" = "SKIP"; "message" = "Test files not found" }
    }
    
    # Pytest argumentları oluştur
    $pytestArgs = Build-PytestArgs -Category $Category -ServiceName $ServiceName -Pattern $TestPattern
    
    Write-Info "Test komutu: $($pytestArgs -join ' ')"
    
    # Test çalıştır
    $testStartTime = Get-Date
    
    try {
        & $pytestArgs[0] $pytestArgs[1..($pytestArgs.Length-1)]
        $testExitCode = $LASTEXITCODE
    } catch {
        $testExitCode = 1
        Write-Error "Test çalıştırma hatası: $($_.Exception.Message)"
    }
    
    $testEndTime = Get-Date
    $testDuration = ($testEndTime - $testStartTime).TotalSeconds
    
    # Sonuç analizi
    if ($testExitCode -eq 0) {
        Write-TestResult "$displayName - PASSED (${testDuration}s)" "PASS"
        return @{ 
            "status" = "PASS"; 
            "duration" = $testDuration;
            "category" = $Category;
            "service" = $ServiceName
        }
    } else {
        Write-TestResult "$displayName - FAILED (${testDuration}s)" "FAIL"
        return @{ 
            "status" = "FAIL"; 
            "duration" = $testDuration;
            "category" = $Category;
            "service" = $ServiceName;
            "exit_code" = $testExitCode
        }
    }
}

# Test sonuçları özeti
function Show-TestSummary {
    param($Results)
    
    Write-Header "Test Sonuçları Özeti"
    
    $totalTests = $Results.Count
    $passedTests = ($Results | Where-Object { $_.status -eq "PASS" }).Count
    $failedTests = ($Results | Where-Object { $_.status -eq "FAIL" }).Count
    $skippedTests = ($Results | Where-Object { $_.status -eq "SKIP" }).Count
    
    $totalDuration = ($Results | Measure-Object -Property duration -Sum).Sum
    
    Write-Host ""
    Write-Host "📊 Test İstatistikleri:" -ForegroundColor Cyan
    Write-Host "   Toplam Test Kategorisi: $totalTests" -ForegroundColor White
    Write-Host "   Başarılı: $passedTests" -ForegroundColor Green
    Write-Host "   Başarısız: $failedTests" -ForegroundColor Red
    Write-Host "   Atlanan: $skippedTests" -ForegroundColor Yellow
    Write-Host "   Toplam Süre: $([math]::Round($totalDuration, 2))s" -ForegroundColor White
    
    Write-Host ""
    if ($failedTests -eq 0) {
        Write-Success "Tüm testler başarıyla geçti! 🎉"
        $exitCode = 0
    } else {
        Write-Error "Bazı testler başarısız! 🚨"
        $exitCode = 1
        
        Write-Host ""
        Write-Header "Başarısız Testler:"
        $Results | Where-Object { $_.status -eq "FAIL" } | ForEach-Object {
            $name = if ($_.service) { "$($_.category) - $($_.service)" } else { $_.category }
            Write-Host "   ❌ $name" -ForegroundColor Red
        }
    }
    
    # Coverage raporu varsa göster
    if ($Coverage -and (Test-Path "$ReportPath/coverage")) {
        Write-Host ""
        Write-Info "Coverage raporu: $ReportPath/coverage/index.html"
    }
    
    # HTML raporu varsa göster
    if ($OutputFormat -eq "html" -and (Test-Path "$ReportPath/report.html")) {
        Write-Info "HTML raporu: $ReportPath/report.html"
    }
    
    return $exitCode
}

# Ana test logic
try {
    $testResults = @()
    $overallStartTime = Get-Date
    
    # Test database setup (integration ve e2e testler için)
    $needsDatabase = ($TestType -in @("all", "integration", "e2e", "api"))
    if ($needsDatabase) {
        $dbSetup = Setup-TestDatabase
        if (-not $dbSetup) {
            Write-Warning "Database setup başarısız, database gerektiren testler atlanacak"
        }
    }
    
    # Test tipine göre çalıştır
    switch ($TestType.ToLower()) {
        "all" {
            Write-Header "Tüm testler çalıştırılıyor..."
            
            foreach ($category in $testCategories.Keys) {
                if ($Service) {
                    $result = Run-Tests -Category $category -ServiceName $Service
                    $testResults += $result
                } else {
                    # Her kategori için tüm servisleri test et
                    $result = Run-Tests -Category $category
                    $testResults += $result
                }
            }
        }
        
        default {
            if ($testCategories.ContainsKey($TestType)) {
                if ($Service) {
                    $result = Run-Tests -Category $TestType -ServiceName $Service
                    $testResults += $result
                } else {
                    $result = Run-Tests -Category $TestType
                    $testResults += $result
                }
            } else {
                Write-Error "Geçersiz test tipi: $TestType"
                exit 1
            }
        }
    }
    
    $overallEndTime = Get-Date
    $overallDuration = ($overallEndTime - $overallStartTime).TotalSeconds
    
    Write-Host ""
    Write-Success "Test süreci tamamlandı! (Toplam süre: $([math]::Round($overallDuration, 2))s)"
    
    # Sonuçları göster
    $exitCode = Show-TestSummary -Results $testResults
    
} finally {
    # Cleanup
    if ($needsDatabase) {
        Cleanup-TestDatabase
    }
}

exit $exitCode
