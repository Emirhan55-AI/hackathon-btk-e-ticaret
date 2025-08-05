# 🧪 Multi-Modal Coordinator Service Test Script
# AURA AI Çok Modlu Sorgu Koordinatörü PowerShell Test Automation

<#
.SYNOPSIS
    Multi-Modal Coordinator Service'i test etmek için PowerShell scripti

.DESCRIPTION
    Bu script AURA AI Multi-Modal Coordinator servisinin tüm özelliklerini
    test eder ve kapsamlı bir test raporu oluşturur.

.PARAMETER TestMode
    Test modu: "quick", "full", "performance"

.EXAMPLE
    .\test_multi_modal_coordinator.ps1 -TestMode "quick"
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("quick", "full", "performance")]
    [string]$TestMode = "quick"
)

# Script configuration - Test parametreleri ve yapılandırma
$ErrorActionPreference = "Continue"
$WarningPreference = "Continue"

# Test constants - Servis bilgileri ve endpoint'ler
$SERVICE_NAME = "Multi-Modal Coordinator Service"
$SERVICE_PORT = 8009
$SERVICE_URL = "http://localhost:$SERVICE_PORT"
$TEST_TIMEOUT = 30

# Color output functions - Renkli konsol çıktısı için
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️ $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Info { param($Message) Write-Host "ℹ️ $Message" -ForegroundColor Cyan }
function Write-Header { param($Message) Write-Host "`n🎯 $Message" -ForegroundColor Magenta -BackgroundColor Black }

# Test results tracking - Test sonuçlarını izlemek için
$Global:TestResults = @{
    Total = 0
    Passed = 0
    Failed = 0
    Skipped = 0
    StartTime = Get-Date
    Details = @()
}

function Add-TestResult {
    param(
        [string]$TestName,
        [string]$Status,
        [string]$Message = "",
        [double]$Duration = 0
    )
    
    $Global:TestResults.Total++
    switch ($Status) {
        "PASS" { $Global:TestResults.Passed++ }
        "FAIL" { $Global:TestResults.Failed++ }
        "SKIP" { $Global:TestResults.Skipped++ }
    }
    
    $Global:TestResults.Details += @{
        Name = $TestName
        Status = $Status
        Message = $Message
        Duration = $Duration
        Timestamp = Get-Date
    }
}

function Test-ServiceHealth {
    """Multi-Modal Coordinator servisinin health durumunu test eder"""
    Write-Header "Testing Service Health"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        # Health check endpoint'ine istek gönder
        Write-Info "Checking service health at $SERVICE_URL/"
        $response = Invoke-RestMethod -Uri "$SERVICE_URL/" -Method GET -TimeoutSec $TEST_TIMEOUT
        
        $stopwatch.Stop()
        $duration = $stopwatch.ElapsedMilliseconds
        
        # Response validation
        if ($response.service -eq "AURA AI Multi-Modal Coordinator Service" -and $response.status -eq "healthy") {
            Write-Success "Service is healthy and operational"
            Write-Info "Response time: $duration ms"
            Write-Info "Components status: $($response.components | ConvertTo-Json -Compress)"
            Add-TestResult -TestName "Service Health Check" -Status "PASS" -Duration $duration
            return $true
        } else {
            Write-Warning "Service health check returned unexpected response"
            Add-TestResult -TestName "Service Health Check" -Status "FAIL" -Message "Unexpected response format"
            return $false
        }
    }
    catch {
        Write-Error "Health check failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Service Health Check" -Status "FAIL" -Message $_.Exception.Message
        return $false
    }
}

function Test-ServiceCapabilities {
    """Service capabilities endpoint'ini test eder"""
    Write-Header "Testing Service Capabilities"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        Write-Info "Requesting service capabilities"
        $response = Invoke-RestMethod -Uri "$SERVICE_URL/capabilities" -Method GET -TimeoutSec $TEST_TIMEOUT
        
        $stopwatch.Stop()
        $duration = $stopwatch.ElapsedMilliseconds
        
        # Validate capabilities response
        $requiredFields = @("service_name", "supported_query_types", "supported_image_formats", "processing_capabilities")
        $missingFields = @()
        
        foreach ($field in $requiredFields) {
            if (-not $response.PSObject.Properties.Name.Contains($field)) {
                $missingFields += $field
            }
        }
        
        if ($missingFields.Count -eq 0) {
            Write-Success "Service capabilities retrieved successfully"
            Write-Info "Supported query types: $($response.supported_query_types.Count)"
            Write-Info "Supported image formats: $($response.supported_image_formats -join ', ')"
            Write-Info "Response time: $duration ms"
            Add-TestResult -TestName "Service Capabilities" -Status "PASS" -Duration $duration
            return $true
        } else {
            Write-Warning "Missing required fields in capabilities: $($missingFields -join ', ')"
            Add-TestResult -TestName "Service Capabilities" -Status "FAIL" -Message "Missing fields: $($missingFields -join ', ')"
            return $false
        }
    }
    catch {
        Write-Error "Capabilities test failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Service Capabilities" -Status "FAIL" -Message $_.Exception.Message
        return $false
    }
}

function Create-TestImageBase64 {
    """Test için basit bir base64 encoded image oluşturur"""
    
    # Basit bir 1x1 pixel transparent PNG image (base64 encoded)
    # Bu minimal bir test image'dir ve gerçek CLIP işlemesi için yeterlidir
    $testImageBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    return $testImageBase64
}

function Test-MultiModalQuery {
    """Multi-modal query endpoint'ini test eder"""
    Write-Header "Testing Multi-Modal Query Processing"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        # Test request hazırla
        $testImageBase64 = Create-TestImageBase64
        $requestBody = @{
            image_base64 = $testImageBase64
            text_query = "Bu mavi gömlekle ne giyebilirim?"
            user_id = "test_user_powershell"
            context = @{
                test_scenario = "powershell_test"
                test_timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            }
        } | ConvertTo-Json -Depth 3
        
        Write-Info "Sending multi-modal query request"
        Write-Info "Query: 'Bu mavi gömlekle ne giyebilirim?'"
        
        # Multi-modal query endpoint'ine POST isteği gönder
        $response = Invoke-RestMethod -Uri "$SERVICE_URL/query" -Method POST -Body $requestBody -ContentType "application/json" -TimeoutSec $TEST_TIMEOUT
        
        $stopwatch.Stop()
        $duration = $stopwatch.ElapsedMilliseconds
        
        # Response validation
        $requiredFields = @("query_id", "success", "unified_intent", "visual_analysis", "textual_analysis", "recommendations")
        $missingFields = @()
        
        foreach ($field in $requiredFields) {
            if (-not $response.PSObject.Properties.Name.Contains($field)) {
                $missingFields += $field
            }
        }
        
        if ($missingFields.Count -eq 0 -and $response.success -eq $true) {
            Write-Success "Multi-modal query processed successfully"
            Write-Info "Query ID: $($response.query_id)"
            Write-Info "Unified Intent: $($response.unified_intent)"
            Write-Info "Fusion Confidence: $($response.fusion_confidence)"
            Write-Info "Recommendations Count: $($response.recommendations.Count)"
            Write-Info "Processing Time: $($response.processing_time_ms) ms"
            Write-Info "Total Response Time: $duration ms"
            Add-TestResult -TestName "Multi-Modal Query" -Status "PASS" -Duration $duration
            return $true
        } else {
            $errorMsg = if ($missingFields.Count -gt 0) { "Missing fields: $($missingFields -join ', ')" } else { "Query processing failed" }
            Write-Warning $errorMsg
            Add-TestResult -TestName "Multi-Modal Query" -Status "FAIL" -Message $errorMsg
            return $false
        }
    }
    catch {
        Write-Error "Multi-modal query test failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Multi-Modal Query" -Status "FAIL" -Message $_.Exception.Message
        return $false
    }
}

function Test-BuiltInScenarios {
    """Built-in test scenarios'ları çalıştırır"""
    Write-Header "Testing Built-In Scenarios"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        Write-Info "Running built-in test scenarios"
        $response = Invoke-RestMethod -Uri "$SERVICE_URL/test-scenarios" -Method POST -TimeoutSec ($TEST_TIMEOUT * 2)
        
        $stopwatch.Stop()
        $duration = $stopwatch.ElapsedMilliseconds
        
        # Test results validation
        if ($response.test_summary -and $response.individual_results) {
            $summary = $response.test_summary
            $successRate = $summary.success_rate_percent
            
            Write-Success "Built-in scenarios completed"
            Write-Info "Total Scenarios: $($summary.total_scenarios)"
            Write-Info "Successful Tests: $($summary.successful_tests)"
            Write-Info "Success Rate: $successRate%"
            Write-Info "System Status: $($summary.system_status)"
            Write-Info "Execution Time: $duration ms"
            
            # Individual test results
            foreach ($result in $response.individual_results) {
                $status = if ($result.success) { "✅" } else { "❌" }
                Write-Host "  $status $($result.scenario_name)"
            }
            
            if ($successRate -ge 80) {
                Add-TestResult -TestName "Built-In Scenarios" -Status "PASS" -Duration $duration -Message "Success rate: $successRate%"
                return $true
            } else {
                Add-TestResult -TestName "Built-In Scenarios" -Status "FAIL" -Duration $duration -Message "Low success rate: $successRate%"
                return $false
            }
        } else {
            Write-Warning "Invalid test scenarios response format"
            Add-TestResult -TestName "Built-In Scenarios" -Status "FAIL" -Message "Invalid response format"
            return $false
        }
    }
    catch {
        Write-Error "Built-in scenarios test failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Built-In Scenarios" -Status "FAIL" -Message $_.Exception.Message
        return $false
    }
}

function Test-QueryStatistics {
    """Query statistics endpoint'ini test eder"""
    Write-Header "Testing Query Statistics"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        
        Write-Info "Requesting query statistics"
        $response = Invoke-RestMethod -Uri "$SERVICE_URL/stats" -Method GET -TimeoutSec $TEST_TIMEOUT
        
        $stopwatch.Stop()
        $duration = $stopwatch.ElapsedMilliseconds
        
        # Statistics validation
        $requiredFields = @("total_queries_processed", "average_processing_time_ms", "success_rate_percent", "most_common_query_types")
        $missingFields = @()
        
        foreach ($field in $requiredFields) {
            if (-not $response.PSObject.Properties.Name.Contains($field)) {
                $missingFields += $field
            }
        }
        
        if ($missingFields.Count -eq 0) {
            Write-Success "Query statistics retrieved successfully"
            Write-Info "Total Queries: $($response.total_queries_processed)"
            Write-Info "Average Processing Time: $($response.average_processing_time_ms) ms"
            Write-Info "Success Rate: $($response.success_rate_percent)%"
            Write-Info "Common Query Types: $($response.most_common_query_types -join ', ')"
            Write-Info "Response Time: $duration ms"
            Add-TestResult -TestName "Query Statistics" -Status "PASS" -Duration $duration
            return $true
        } else {
            Write-Warning "Missing required fields in statistics: $($missingFields -join ', ')"
            Add-TestResult -TestName "Query Statistics" -Status "FAIL" -Message "Missing fields: $($missingFields -join ', ')"
            return $false
        }
    }
    catch {
        Write-Error "Statistics test failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Query Statistics" -Status "FAIL" -Message $_.Exception.Message
        return $false
    }
}

function Test-ErrorHandling {
    """Error handling test'lerini çalıştırır"""
    Write-Header "Testing Error Handling"
    
    # Test 1: Invalid JSON request
    try {
        Write-Info "Testing invalid JSON request handling"
        $invalidJson = "{ invalid json }"
        
        try {
            Invoke-RestMethod -Uri "$SERVICE_URL/query" -Method POST -Body $invalidJson -ContentType "application/json" -TimeoutSec $TEST_TIMEOUT
            Write-Warning "Invalid JSON was accepted (unexpected)"
            Add-TestResult -TestName "Invalid JSON Handling" -Status "FAIL" -Message "Invalid JSON accepted"
        }
        catch {
            if ($_.Exception.Response.StatusCode -eq 400 -or $_.Exception.Response.StatusCode -eq 422) {
                Write-Success "Invalid JSON correctly rejected"
                Add-TestResult -TestName "Invalid JSON Handling" -Status "PASS"
            } else {
                Write-Warning "Unexpected error code for invalid JSON: $($_.Exception.Response.StatusCode)"
                Add-TestResult -TestName "Invalid JSON Handling" -Status "FAIL" -Message "Unexpected error code"
            }
        }
    }
    catch {
        Write-Error "Error testing invalid JSON: $($_.Exception.Message)"
        Add-TestResult -TestName "Invalid JSON Handling" -Status "FAIL" -Message $_.Exception.Message
    }
    
    # Test 2: Empty text query
    try {
        Write-Info "Testing empty text query handling"
        $emptyQueryRequest = @{
            image_base64 = Create-TestImageBase64
            text_query = ""
            user_id = "test_user"
        } | ConvertTo-Json
        
        try {
            Invoke-RestMethod -Uri "$SERVICE_URL/query" -Method POST -Body $emptyQueryRequest -ContentType "application/json" -TimeoutSec $TEST_TIMEOUT
            Write-Warning "Empty text query was accepted (unexpected)"
            Add-TestResult -TestName "Empty Query Handling" -Status "FAIL" -Message "Empty query accepted"
        }
        catch {
            if ($_.Exception.Response.StatusCode -eq 422) {
                Write-Success "Empty text query correctly rejected"
                Add-TestResult -TestName "Empty Query Handling" -Status "PASS"
            } else {
                Write-Warning "Unexpected error code for empty query: $($_.Exception.Response.StatusCode)"
                Add-TestResult -TestName "Empty Query Handling" -Status "FAIL" -Message "Unexpected error code"
            }
        }
    }
    catch {
        Write-Error "Error testing empty query: $($_.Exception.Message)"
        Add-TestResult -TestName "Empty Query Handling" -Status "FAIL" -Message $_.Exception.Message
    }
}

function Test-Performance {
    """Performance test'lerini çalıştırır"""
    Write-Header "Testing Performance"
    
    if ($TestMode -ne "performance" -and $TestMode -ne "full") {
        Write-Info "Skipping performance tests (run with -TestMode 'performance' or 'full')"
        Add-TestResult -TestName "Performance Tests" -Status "SKIP" -Message "Not requested in test mode"
        return
    }
    
    try {
        Write-Info "Running concurrent request performance test"
        
        # Concurrent requests test
        $concurrentRequests = 5
        $testImageBase64 = Create-TestImageBase64
        
        $jobs = @()
        $startTime = Get-Date
        
        # Start concurrent jobs
        for ($i = 1; $i -le $concurrentRequests; $i++) {
            $job = Start-Job -ScriptBlock {
                param($ServiceUrl, $ImageBase64, $RequestId)
                
                $requestBody = @{
                    image_base64 = $ImageBase64
                    text_query = "Performance test query $RequestId"
                    user_id = "perf_test_user_$RequestId"
                    context = @{ test_type = "performance"; request_id = $RequestId }
                } | ConvertTo-Json -Depth 3
                
                try {
                    $response = Invoke-RestMethod -Uri "$ServiceUrl/query" -Method POST -Body $requestBody -ContentType "application/json" -TimeoutSec 30
                    return @{ Success = $true; RequestId = $RequestId; Response = $response }
                }
                catch {
                    return @{ Success = $false; RequestId = $RequestId; Error = $_.Exception.Message }
                }
            } -ArgumentList $SERVICE_URL, $testImageBase64, $i
            
            $jobs += $job
        }
        
        # Wait for all jobs to complete
        $results = $jobs | Wait-Job | Receive-Job
        $jobs | Remove-Job
        
        $endTime = Get-Date
        $totalDuration = ($endTime - $startTime).TotalMilliseconds
        
        # Analyze results
        $successfulRequests = ($results | Where-Object { $_.Success }).Count
        $failedRequests = $concurrentRequests - $successfulRequests
        $successRate = ($successfulRequests / $concurrentRequests) * 100
        
        Write-Success "Performance test completed"
        Write-Info "Concurrent Requests: $concurrentRequests"
        Write-Info "Successful Requests: $successfulRequests"
        Write-Info "Failed Requests: $failedRequests"
        Write-Info "Success Rate: $successRate%"
        Write-Info "Total Duration: $totalDuration ms"
        Write-Info "Average Request Time: $($totalDuration / $concurrentRequests) ms"
        
        if ($successRate -ge 80 -and $totalDuration -lt 10000) {
            Add-TestResult -TestName "Performance Test" -Status "PASS" -Duration $totalDuration -Message "Success rate: $successRate%"
        } else {
            Add-TestResult -TestName "Performance Test" -Status "FAIL" -Duration $totalDuration -Message "Performance below threshold"
        }
    }
    catch {
        Write-Error "Performance test failed: $($_.Exception.Message)"
        Add-TestResult -TestName "Performance Test" -Status "FAIL" -Message $_.Exception.Message
    }
}

function Show-TestSummary {
    """Test sonuçlarının özet raporunu gösterir"""
    Write-Header "Test Summary Report"
    
    $endTime = Get-Date
    $totalDuration = ($endTime - $Global:TestResults.StartTime).TotalSeconds
    
    # Overall statistics
    Write-Host "`n📊 Overall Test Statistics:" -ForegroundColor Cyan
    Write-Host "  Total Tests: $($Global:TestResults.Total)" -ForegroundColor White
    Write-Host "  ✅ Passed: $($Global:TestResults.Passed)" -ForegroundColor Green
    Write-Host "  ❌ Failed: $($Global:TestResults.Failed)" -ForegroundColor Red
    Write-Host "  ⏭️ Skipped: $($Global:TestResults.Skipped)" -ForegroundColor Yellow
    Write-Host "  ⏱️ Total Duration: $([math]::Round($totalDuration, 2)) seconds" -ForegroundColor White
    
    # Success rate calculation
    if ($Global:TestResults.Total -gt 0) {
        $successRate = ($Global:TestResults.Passed / ($Global:TestResults.Total - $Global:TestResults.Skipped)) * 100
        Write-Host "  📈 Success Rate: $([math]::Round($successRate, 1))%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })
    }
    
    # Detailed results
    Write-Host "`n📋 Detailed Test Results:" -ForegroundColor Cyan
    foreach ($result in $Global:TestResults.Details) {
        $statusColor = switch ($result.Status) {
            "PASS" { "Green" }
            "FAIL" { "Red" }
            "SKIP" { "Yellow" }
            default { "White" }
        }
        
        $statusIcon = switch ($result.Status) {
            "PASS" { "✅" }
            "FAIL" { "❌" }
            "SKIP" { "⏭️" }
            default { "❓" }
        }
        
        Write-Host "  $statusIcon $($result.Name)" -ForegroundColor $statusColor
        if ($result.Duration -gt 0) {
            Write-Host "    ⏱️ Duration: $($result.Duration) ms" -ForegroundColor Gray
        }
        if ($result.Message) {
            Write-Host "    💬 Details: $($result.Message)" -ForegroundColor Gray
        }
    }
    
    # Overall assessment
    Write-Host "`n🎯 Overall Assessment:" -ForegroundColor Magenta
    if ($Global:TestResults.Failed -eq 0) {
        Write-Success "All tests passed! Multi-Modal Coordinator Service is fully operational."
    } elseif ($Global:TestResults.Failed -le 2) {
        Write-Warning "Some tests failed, but core functionality appears operational."
    } else {
        Write-Error "Multiple test failures detected. Service may require attention."
    }
    
    # Recommendations
    Write-Host "`n💡 Recommendations:" -ForegroundColor Cyan
    if ($Global:TestResults.Failed -eq 0) {
        Write-Host "  • Service is ready for production deployment" -ForegroundColor Green
        Write-Host "  • Consider running performance tests regularly" -ForegroundColor White
    } else {
        Write-Host "  • Review failed tests and error messages" -ForegroundColor Yellow
        Write-Host "  • Check service logs for detailed error information" -ForegroundColor Yellow
        Write-Host "  • Verify all dependent services are running" -ForegroundColor Yellow
    }
}

# Main execution function
function Main {
    """Ana test execution fonksiyonu"""
    
    # Script header
    Clear-Host
    Write-Host "🧪 AURA AI Multi-Modal Coordinator Service Test Suite" -ForegroundColor Magenta -BackgroundColor Black
    Write-Host "=" * 70 -ForegroundColor Magenta
    Write-Host "Test Mode: $TestMode" -ForegroundColor Cyan
    Write-Host "Service URL: $SERVICE_URL" -ForegroundColor Cyan
    Write-Host "Start Time: $(Get-Date)" -ForegroundColor Cyan
    Write-Host ""
    
    # Service availability check
    Write-Info "Checking if Multi-Modal Coordinator service is available..."
    try {
        $null = Invoke-RestMethod -Uri $SERVICE_URL -Method GET -TimeoutSec 5
        Write-Success "Service is reachable at $SERVICE_URL"
    }
    catch {
        Write-Error "Service is not reachable at $SERVICE_URL"
        Write-Error "Please ensure the Multi-Modal Coordinator service is running"
        Write-Host "`nTo start the service, run:" -ForegroundColor Yellow
        Write-Host "  cd aura_ai_system\services\multi_modal_coordinator" -ForegroundColor White
        Write-Host "  python main.py" -ForegroundColor White
        exit 1
    }
    
    # Execute test suites based on test mode
    switch ($TestMode) {
        "quick" {
            Write-Info "Running quick test suite..."
            Test-ServiceHealth
            Test-ServiceCapabilities
            Test-MultiModalQuery
            Test-QueryStatistics
        }
        "full" {
            Write-Info "Running full test suite..."
            Test-ServiceHealth
            Test-ServiceCapabilities
            Test-MultiModalQuery
            Test-BuiltInScenarios
            Test-QueryStatistics
            Test-ErrorHandling
            Test-Performance
        }
        "performance" {
            Write-Info "Running performance-focused test suite..."
            Test-ServiceHealth
            Test-MultiModalQuery
            Test-Performance
        }
    }
    
    # Show final results
    Show-TestSummary
    
    # Exit code based on test results
    if ($Global:TestResults.Failed -eq 0) {
        exit 0
    } else {
        exit 1
    }
}

# Script execution
try {
    Main
}
catch {
    Write-Error "Unexpected error during test execution: $($_.Exception.Message)"
    exit 1
}
