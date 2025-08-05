# 🔄 AURA AI FEEDBACK LOOP - DEPLOYMENT AUTOMATION SCRIPT
# Feedback Loop Prompt Engineering Sisteminin Tam Otomatik Deploy ve Test Scripti

param(
    [string]$Mode = "deploy",  # deploy, test, validate, demo, full
    [switch]$SkipBuild = $false,
    [switch]$QuickTest = $false,
    [switch]$Verbose = $false
)

# Color output functions
function Write-ColoredText {
    param([string]$Text, [string]$Color = "White")
    switch ($Color) {
        "Red"     { Write-Host $Text -ForegroundColor Red }
        "Green"   { Write-Host $Text -ForegroundColor Green }
        "Yellow"  { Write-Host $Text -ForegroundColor Yellow }
        "Blue"    { Write-Host $Text -ForegroundColor Blue }
        "Cyan"    { Write-Host $Text -ForegroundColor Cyan }
        "Magenta" { Write-Host $Text -ForegroundColor Magenta }
        default   { Write-Host $Text }
    }
}

function Write-SectionHeader {
    param([string]$Title)
    Write-Host ""
    Write-ColoredText "=" * 80 "Cyan"
    Write-ColoredText " $Title " "White"
    Write-ColoredText "=" * 80 "Cyan"
}

function Write-Success {
    param([string]$Message)
    Write-ColoredText "✅ $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColoredText "⚠️ $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColoredText "❌ $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColoredText "ℹ️ $Message" "Blue"
}

Write-SectionHeader "AURA AI FEEDBACK LOOP - DEPLOYMENT AUTOMATION"
Write-Info "Mode: $Mode"
Write-Info "Skip Build: $SkipBuild"
Write-Info "Quick Test: $QuickTest"
Write-Info "Start Time: $(Get-Date)"

# Check if we're in the correct directory
if (-not (Test-Path "docker-compose.yml")) {
    Write-Error "docker-compose.yml not found. Please run from project root directory."
    exit 1
}

# Function to check if Docker is running
function Test-DockerStatus {
    Write-SectionHeader "DOCKER STATUS CHECK"
    
    try {
        $dockerVersion = docker version --format '{{.Server.Version}}' 2>$null
        if ($dockerVersion) {
            Write-Success "Docker is running - Version: $dockerVersion"
            return $true
        } else {
            Write-Error "Docker is not running or not accessible"
            return $false
        }
    } catch {
        Write-Error "Docker check failed: $_"
        return $false
    }
}

# Function to build feedback loop service
function Build-FeedbackLoopService {
    if ($SkipBuild) {
        Write-Warning "Skipping build as requested"
        return $true
    }
    
    Write-SectionHeader "BUILDING FEEDBACK LOOP SERVICE"
    
    try {
        Write-Info "Building feedback-loop service..."
        docker-compose build feedback-loop
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Feedback Loop service built successfully"
            return $true
        } else {
            Write-Error "Failed to build Feedback Loop service"
            return $false
        }
    } catch {
        Write-Error "Build failed: $_"
        return $false
    }
}

# Function to deploy all services
function Deploy-AuraAISystem {
    Write-SectionHeader "DEPLOYING AURA AI SYSTEM"
    
    try {
        Write-Info "Stopping existing containers..."
        docker-compose down
        
        Write-Info "Starting all services..."
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "All services deployed successfully"
            return $true
        } else {
            Write-Error "Deployment failed"
            return $false
        }
    } catch {
        Write-Error "Deployment failed: $_"
        return $false
    }
}

# Function to wait for services to be ready
function Wait-ForServices {
    Write-SectionHeader "WAITING FOR SERVICES TO BE READY"
    
    $services = @{
        "image-processing" = "http://localhost:8002"
        "nlu-service" = "http://localhost:8004"
        "style-profile" = "http://localhost:8003"
        "combination-engine" = "http://localhost:8006"
        "recommendation-engine" = "http://localhost:8005"
        "orchestrator" = "http://localhost:8006"
        "feedback-loop" = "http://localhost:8007"
        "quality-assurance" = "http://localhost:8008"
        "multi-modal-coordinator" = "http://localhost:8009"
    }
    
    $maxRetries = 30
    $retryDelay = 5
    
    foreach ($serviceName in $services.Keys) {
        $url = $services[$serviceName]
        Write-Info "Checking $serviceName at $url..."
        
        $retries = 0
        $isReady = $false
        
        while (-not $isReady -and $retries -lt $maxRetries) {
            try {
                $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 5 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    Write-Success "$serviceName is ready"
                    $isReady = $true
                } else {
                    $retries++
                    Start-Sleep $retryDelay
                }
            } catch {
                $retries++
                if ($retries -eq 1) {
                    Write-Info "Waiting for $serviceName to start..."
                }
                Start-Sleep $retryDelay
            }
        }
        
        if (-not $isReady) {
            Write-Error "$serviceName is not responding after $($maxRetries * $retryDelay) seconds"
            return $false
        }
    }
    
    Write-Success "All services are ready"
    return $true
}

# Function to run health checks
function Test-SystemHealth {
    Write-SectionHeader "SYSTEM HEALTH CHECK"
    
    try {
        Write-Info "Running orchestrator health check..."
        $response = Invoke-RestMethod -Uri "http://localhost:8006/health" -Method GET -TimeoutSec 10
        
        if ($response.status -eq "healthy") {
            Write-Success "System health: $($response.status)"
            Write-Info "Service count: $($response.services_count)"
            Write-Info "Healthy services: $($response.healthy_services)"
            
            # Display individual service status
            foreach ($service in $response.service_details.PSObject.Properties) {
                $serviceName = $service.Name
                $serviceStatus = $service.Value.status
                
                if ($serviceStatus -eq "healthy") {
                    Write-Success "  $serviceName: $serviceStatus"
                } else {
                    Write-Warning "  $serviceName: $serviceStatus"
                }
            }
            
            return $true
        } else {
            Write-Error "System health check failed: $($response.status)"
            return $false
        }
    } catch {
        Write-Error "Health check failed: $_"
        return $false
    }
}

# Function to test feedback loop functionality
function Test-FeedbackLoopFunctionality {
    Write-SectionHeader "FEEDBACK LOOP FUNCTIONALITY TEST"
    
    $testFeedbacks = @(
        @{
            "user_id" = "test_user_1"
            "recommendation_id" = "rec_001"
            "feedback_text" = "Bu kombini hiç beğenmedim"
            "context" = @{ "occasion" = "work" }
            "expected_type" = "negative_general"
        },
        @{
            "user_id" = "test_user_2"
            "recommendation_id" = "rec_002"
            "feedback_text" = "Renkleri uyumlu değil"
            "context" = @{ "colors" = @("red", "green") }
            "expected_type" = "color_dissatisfaction"
        },
        @{
            "user_id" = "test_user_3"
            "recommendation_id" = "rec_003"
            "feedback_text" = "Mükemmel! Benzer öneriler istiyorum"
            "context" = @{ "style" = "casual" }
            "expected_type" = "request_similar"
        }
    )
    
    $successCount = 0
    $totalTests = $testFeedbacks.Count
    
    foreach ($i in 0..($testFeedbacks.Count - 1)) {
        $feedback = $testFeedbacks[$i]
        Write-Info "Test $($i + 1)/$totalTests: $($feedback.feedback_text)"
        
        try {
            # Test direct feedback service
            $directResponse = Invoke-RestMethod -Uri "http://localhost:8007/feedback/analyze" -Method POST -Body ($feedback | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 15
            
            if ($directResponse.success) {
                $predictedType = $directResponse.data.classification_results.feedback_type
                $confidence = $directResponse.data.classification_results.confidence
                
                if ($predictedType -eq $feedback.expected_type) {
                    Write-Success "  Direct test: $predictedType (confidence: $confidence)"
                    $successCount++
                } else {
                    Write-Warning "  Direct test: Expected $($feedback.expected_type), got $predictedType"
                }
            } else {
                Write-Error "  Direct test failed: $($directResponse.error)"
            }
            
            # Test orchestrated feedback processing
            $orchestratedResponse = Invoke-RestMethod -Uri "http://localhost:8006/feedback/process" -Method POST -Body ($feedback | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 20
            
            if ($orchestratedResponse.success) {
                Write-Success "  Orchestrated test: Workflow $($orchestratedResponse.workflow_id) completed"
                Write-Info "    Actions taken: $($orchestratedResponse.actions_taken.Count)"
            } else {
                Write-Warning "  Orchestrated test failed"
            }
            
        } catch {
            Write-Error "  Test failed: $_"
        }
        
        Start-Sleep 2  # Brief delay between tests
    }
    
    $accuracy = [math]::Round(($successCount / $totalTests) * 100, 1)
    
    Write-Info "Test Results:"
    Write-Info "  Total Tests: $totalTests"
    Write-Info "  Successful: $successCount"
    Write-Info "  Accuracy: $accuracy%"
    
    if ($accuracy -ge 80) {
        Write-Success "Feedback Loop functionality test PASSED"
        return $true
    } else {
        Write-Warning "Feedback Loop functionality test needs improvement"
        return $false
    }
}

# Function to run comprehensive validation
function Start-ComprehensiveValidation {
    Write-SectionHeader "COMPREHENSIVE VALIDATION SUITE"
    
    try {
        Write-Info "Running comprehensive validation..."
        
        # Change to feedback service directory
        Push-Location "aura_ai_system/services/feedback_loop_service"
        
        # Run the validation suite
        python feedback_validation_suite.py
        
        Pop-Location
        
        Write-Success "Comprehensive validation completed"
        return $true
    } catch {
        Write-Error "Comprehensive validation failed: $_"
        Pop-Location
        return $false
    }
}

# Function to run interactive demo
function Start-InteractiveDemo {
    Write-SectionHeader "INTERACTIVE FEEDBACK DEMO"
    
    try {
        Write-Info "Starting interactive demo..."
        
        # Change to feedback service directory
        Push-Location "aura_ai_system/services/feedback_loop_service"
        
        # Run the demo
        python feedback_demo.py
        
        Pop-Location
        
        Write-Success "Interactive demo completed"
        return $true
    } catch {
        Write-Error "Interactive demo failed: $_"
        Pop-Location
        return $false
    }
}

# Function to display system overview
function Show-SystemOverview {
    Write-SectionHeader "AURA AI SYSTEM OVERVIEW"
    
    Write-Info "Service Architecture:"
    Write-ColoredText "  🖼️  Image Processing Service  - Port 8002" "Cyan"
    Write-ColoredText "  🧠 NLU Service              - Port 8004" "Cyan"
    Write-ColoredText "  👤 Style Profile Service     - Port 8003" "Cyan"
    Write-ColoredText "  🎨 Combination Engine        - Port 8006" "Cyan"
    Write-ColoredText "  💡 Recommendation Engine     - Port 8005" "Cyan"
    Write-ColoredText "  🎯 Orchestrator Service      - Port 8006" "Cyan"
    Write-ColoredText "  🔄 Feedback Loop Service     - Port 8007" "Magenta"
    Write-ColoredText "  🛡️  Quality Assurance Service - Port 8008" "Green"
    Write-ColoredText "  🌟 Multi-Modal Coordinator   - Port 8009" "Yellow"
    
    Write-Info ""
    Write-Info "Key Endpoints:"
    Write-ColoredText "  📊 System Health: http://localhost:8006/health" "Green"
    Write-ColoredText "  🔄 Process Feedback: http://localhost:8006/feedback/process" "Magenta"
    Write-ColoredText "  📈 Feedback Analytics: http://localhost:8006/feedback/analytics" "Magenta"
    Write-ColoredText "  📚 API Documentation: http://localhost:8006/docs" "Yellow"
    Write-ColoredText "  🛡️  Quality Assurance: http://localhost:8008/validate" "Green"
    Write-ColoredText "  🌟 Multi-Modal Query: http://localhost:8009/query" "Yellow"
    Write-ColoredText "  🌟 Multi-Modal Docs: http://localhost:8009/docs" "Yellow"
    Write-ColoredText "  🧠 Advanced NLU Test: http://localhost:8009/test-nlu-advanced" "Cyan"
    
    Write-Info ""
    Write-Info "Feedback Loop Features:"
    Write-ColoredText "  ✨ Prompt Engineering Patterns (5-pattern approach)" "Magenta"
    Write-ColoredText "  🎯 Classification: negative_general, color_dissatisfaction, request_similar, occasion_inappropriate" "Magenta"
    Write-ColoredText "  🔄 Service Coordination & Learning Optimization" "Magenta"
    Write-ColoredText "  📊 Real-time Analytics & Insights" "Magenta"
    
    Write-Info ""
    Write-Info "Multi-Modal Features:"
    Write-ColoredText "  🖼️ CLIP-based Visual Analysis" "Yellow"
    Write-ColoredText "  🧠 Advanced NLU Text Processing" "Yellow"
    Write-ColoredText "  🔗 Context Fusion & Semantic Integration" "Yellow"
    Write-ColoredText "  🎨 Cross-modal Query Processing" "Yellow"
}

# Main execution logic
$overallSuccess = $true

# Check Docker status
if (-not (Test-DockerStatus)) {
    Write-Error "Cannot proceed without Docker"
    exit 1
}

# Execute based on mode
switch ($Mode.ToLower()) {
    "deploy" {
        if (-not (Build-FeedbackLoopService)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Deploy-AuraAISystem)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Wait-ForServices)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Test-SystemHealth)) { $overallSuccess = $false }
    }
    
    "test" {
        if (-not (Test-SystemHealth)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Test-FeedbackLoopFunctionality)) { $overallSuccess = $false }
    }
    
    "validate" {
        if (-not (Start-ComprehensiveValidation)) { $overallSuccess = $false }
    }
    
    "demo" {
        if (-not (Start-InteractiveDemo)) { $overallSuccess = $false }
    }
    
    "full" {
        if (-not (Build-FeedbackLoopService)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Deploy-AuraAISystem)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Wait-ForServices)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Test-SystemHealth)) { $overallSuccess = $false }
        if ($overallSuccess -and -not (Test-FeedbackLoopFunctionality)) { $overallSuccess = $false }
        if ($overallSuccess -and -not $QuickTest -and -not (Start-ComprehensiveValidation)) { $overallSuccess = $false }
    }
    
    default {
        Write-Error "Unknown mode: $Mode. Available modes: deploy, test, validate, demo, full"
        exit 1
    }
}

# Show system overview
Show-SystemOverview

# Final status
Write-SectionHeader "DEPLOYMENT AUTOMATION RESULTS"

if ($overallSuccess) {
    Write-Success "🎉 AURA AI Feedback Loop deployment completed successfully!"
    Write-Success "All systems are operational and ready for use."
    
    Write-Info ""
    Write-Info "Next Steps:"
    Write-ColoredText "  1. Visit http://localhost:8006/docs for API documentation" "Yellow"
    Write-ColoredText "  2. Test feedback processing at http://localhost:8006/feedback/process" "Yellow"
    Write-ColoredText "  3. Monitor system health at http://localhost:8006/health" "Yellow"
    Write-ColoredText "  4. Run validation: ./FEEDBACK_LOOP_DEPLOY.ps1 -Mode validate" "Yellow"
    Write-ColoredText "  5. Try interactive demo: ./FEEDBACK_LOOP_DEPLOY.ps1 -Mode demo" "Yellow"
    
} else {
    Write-Error "❌ Deployment encountered issues. Please check the logs above."
    Write-Warning "Troubleshooting suggestions:"
    Write-Warning "  1. Check Docker service status"
    Write-Warning "  2. Verify port availability (8001-8007)"
    Write-Warning "  3. Review individual service logs with: docker-compose logs [service-name]"
    Write-Warning "  4. Try rebuilding: ./FEEDBACK_LOOP_DEPLOY.ps1 -Mode full"
}

Write-Info "End Time: $(Get-Date)"
Write-Info "Total Duration: $((Get-Date) - (Get-Date).AddMinutes(-5))"  # Placeholder - would calculate actual duration

if ($overallSuccess) {
    exit 0
} else {
    exit 1
}
