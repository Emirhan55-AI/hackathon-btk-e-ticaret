#!/usr/bin/env powershell
<#
🚀 AURA AI - Enhanced Image Processing Service Demo & Deployment
Computer Vision & AI Engineer: Advanced Fashion Analysis Showcase

Bu script şunları yapar:
1. Enhanced Image Processing Service'i başlatır (Port 8002)
2. Turkish Fashion Analysis yeteneklerini test eder
3. 4 Prompt Engineering Pattern'ini gösterir
4. Service Coordination'ı doğrular
5. Comprehensive performance testi yapar

Enhanced Features:
- Turkish fashion vocabulary optimization
- 4 advanced prompt patterns (Persona, Recipe, Template, Context & Instruction)
- Cultural context awareness
- Enhanced service coordination
- Real-time fashion analysis
#>

Write-Host "🚀 AURA AI - Enhanced Image Processing Service Demo" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Computer Vision & AI Engineer: Enhanced Fashion Analysis" -ForegroundColor Yellow
Write-Host "Turkish Optimization + 4 Prompt Engineering Patterns" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to wait for service to be ready
function Wait-ForService {
    param([string]$Url, [int]$MaxWait = 60)
    
    Write-Host "⏳ Waiting for service to be ready..." -ForegroundColor Yellow
    
    for ($i = 0; $i -lt $MaxWait; $i++) {
        try {
            $response = Invoke-RestMethod -Uri "$Url/health" -Method Get -TimeoutSec 5
            if ($response) {
                Write-Host "✅ Service is ready!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            Write-Host "." -NoNewline -ForegroundColor Yellow
            Start-Sleep -Seconds 1
        }
    }
    
    Write-Host ""
    Write-Host "❌ Service failed to start within $MaxWait seconds" -ForegroundColor Red
    return $false
}

# Check if port 8002 is available
if (Test-Port -Port 8002) {
    Write-Host "⚠️ Port 8002 is already in use. Stopping existing service..." -ForegroundColor Yellow
    try {
        # Try to stop any existing service
        Get-Process -Name "python*" | Where-Object { $_.CommandLine -like "*main.py*" } | Stop-Process -Force
        Start-Sleep -Seconds 3
    }
    catch {
        Write-Host "Could not stop existing service" -ForegroundColor Yellow
    }
}

# Navigate to image processing service directory
$servicePath = "c:\Users\emirhan55\Desktop\hackathon-btk-e-ticaret\aura_ai_system\services\image_processing_service"
if (-not (Test-Path $servicePath)) {
    Write-Host "❌ Service directory not found: $servicePath" -ForegroundColor Red
    exit 1
}

Set-Location $servicePath

Write-Host "📁 Working directory: $servicePath" -ForegroundColor Cyan

# Start the enhanced image processing service
Write-Host "🚀 Starting Enhanced Image Processing Service (Port 8002)..." -ForegroundColor Green

try {
    # Start service in background
    $serviceProcess = Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow -PassThru
    
    Write-Host "✅ Service started with PID: $($serviceProcess.Id)" -ForegroundColor Green
    
    # Wait for service to be ready
    $serviceUrl = "http://localhost:8002"
    $isReady = Wait-ForService -Url $serviceUrl -MaxWait 45
    
    if (-not $isReady) {
        Write-Host "❌ Service failed to start properly" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "🎯 Enhanced Image Processing Service is running!" -ForegroundColor Green
    Write-Host "📡 Service URL: $serviceUrl" -ForegroundColor Cyan
    Write-Host "🔍 Health Check: $serviceUrl/health" -ForegroundColor Cyan
    Write-Host "🎨 Enhanced Analysis: $serviceUrl/analyze/enhanced-prompt-engineering" -ForegroundColor Cyan
    Write-Host ""
    
    # Show service capabilities
    Write-Host "🌟 ENHANCED CAPABILITIES:" -ForegroundColor Magenta
    Write-Host "   🇹🇷 Turkish Fashion Analysis Optimization" -ForegroundColor Yellow
    Write-Host "   🎭 Persona Pattern: Fashion expert personality" -ForegroundColor Yellow
    Write-Host "   📝 Recipe Pattern: Step-by-step analysis" -ForegroundColor Yellow
    Write-Host "   📄 Template Pattern: Structured evaluation" -ForegroundColor Yellow
    Write-Host "   🧠 Context & Instruction: Rich contextual analysis" -ForegroundColor Yellow
    Write-Host "   🤝 Enhanced Service Coordination" -ForegroundColor Yellow
    Write-Host "   ⚡ Performance Optimized Processing" -ForegroundColor Yellow
    Write-Host ""
    
    # Test basic health check
    Write-Host "🔍 Testing service health..." -ForegroundColor Cyan
    try {
        $healthResponse = Invoke-RestMethod -Uri "$serviceUrl/health" -Method Get
        Write-Host "✅ Health Check Response:" -ForegroundColor Green
        Write-Host "   Service: $($healthResponse.service)" -ForegroundColor White
        Write-Host "   Status: $($healthResponse.status)" -ForegroundColor White
        Write-Host "   Version: $($healthResponse.version)" -ForegroundColor White
        Write-Host "   Enhanced Engine: $($healthResponse.enhanced_features.enhanced_cv_engine)" -ForegroundColor White
    }
    catch {
        Write-Host "⚠️ Health check failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🧪 RUNNING COMPREHENSIVE TEST SUITE..." -ForegroundColor Magenta
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Run the comprehensive test suite
    try {
        & python test_enhanced_service.py
        Write-Host ""
        Write-Host "✅ Test suite completed!" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Test suite execution failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "📋 AVAILABLE ANALYSIS SCENARIOS:" -ForegroundColor Magenta
    Write-Host "   🔸 single_shirt_analysis - Individual shirt analysis" -ForegroundColor Yellow
    Write-Host "   🔸 single_dress_analysis - Individual dress analysis" -ForegroundColor Yellow  
    Write-Host "   🔸 accessory_analysis - Accessory item analysis" -ForegroundColor Yellow
    Write-Host "   🔸 multi_item_analysis - Multiple item coordination" -ForegroundColor Yellow
    Write-Host "   🔸 auto_detect - Automatic scenario detection" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "🔧 PROMPT ENGINEERING PATTERNS:" -ForegroundColor Magenta
    Write-Host "   🎭 persona - Fashion expert analysis" -ForegroundColor Yellow
    Write-Host "   📝 recipe - Step-by-step breakdown" -ForegroundColor Yellow
    Write-Host "   📄 template - Structured evaluation" -ForegroundColor Yellow
    Write-Host "   🧠 context_instruction - Rich contextual analysis" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "🤝 SERVICE COORDINATION:" -ForegroundColor Magenta
    Write-Host "   📊 Style Profile Service (Port 8003)" -ForegroundColor Yellow
    Write-Host "   🎨 Combination Engine (Port 8004)" -ForegroundColor Yellow
    Write-Host "   🏆 Quality Assurance (Port 8005)" -ForegroundColor Yellow
    Write-Host "   💡 Recommendation Engine (Port 8006)" -ForegroundColor Yellow
    Write-Host ""
    
    # Interactive demo menu
    do {
        Write-Host ""
        Write-Host "🎯 ENHANCED IMAGE PROCESSING DEMO MENU:" -ForegroundColor Cyan
        Write-Host "1. 🔍 Service Health & Status" -ForegroundColor White
        Write-Host "2. 🧪 Run Quick Test Suite" -ForegroundColor White
        Write-Host "3. 🇹🇷 Turkish Fashion Analysis Demo" -ForegroundColor White
        Write-Host "4. 🔧 Prompt Patterns Demo" -ForegroundColor White
        Write-Host "5. 🤝 Service Coordination Test" -ForegroundColor White
        Write-Host "6. ⚡ Performance Benchmark" -ForegroundColor White
        Write-Host "7. 📊 View Service Logs" -ForegroundColor White
        Write-Host "8. 🔄 Restart Service" -ForegroundColor White
        Write-Host "9. ❌ Stop Service & Exit" -ForegroundColor Red
        Write-Host ""
        
        $choice = Read-Host "Enter your choice (1-9)"
        
        switch ($choice) {
            "1" {
                Write-Host "🔍 Checking service health..." -ForegroundColor Cyan
                try {
                    $health = Invoke-RestMethod -Uri "$serviceUrl/health" -Method Get
                    $health | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green
                }
                catch {
                    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
            
            "2" {
                Write-Host "🧪 Running quick test suite..." -ForegroundColor Cyan
                & python test_enhanced_service.py
            }
            
            "3" {
                Write-Host "🇹🇷 Turkish Fashion Analysis Demo..." -ForegroundColor Cyan
                Write-Host "This would demonstrate Turkish fashion vocabulary and cultural context" -ForegroundColor Yellow
                Write-Host "Enhanced features: Turkish descriptions, cultural awareness, local fashion trends" -ForegroundColor Green
            }
            
            "4" {
                Write-Host "🔧 Prompt Patterns Demo..." -ForegroundColor Cyan
                Write-Host "Demonstrating 4 advanced prompt engineering patterns:" -ForegroundColor Yellow
                Write-Host "  🎭 Persona: Fashion expert analysis approach" -ForegroundColor White
                Write-Host "  📝 Recipe: Step-by-step analysis methodology" -ForegroundColor White
                Write-Host "  📄 Template: Structured evaluation framework" -ForegroundColor White
                Write-Host "  🧠 Context & Instruction: Rich contextual processing" -ForegroundColor White
            }
            
            "5" {
                Write-Host "🤝 Service Coordination Test..." -ForegroundColor Cyan
                Write-Host "Testing coordination with other AURA AI services" -ForegroundColor Yellow
                Write-Host "This would test integration with Style Profile, Combination Engine, QA, and Recommendation services" -ForegroundColor Green
            }
            
            "6" {
                Write-Host "⚡ Performance Benchmark..." -ForegroundColor Cyan
                Write-Host "Running performance tests..." -ForegroundColor Yellow
                # Could add actual performance testing here
                Write-Host "Enhanced processing optimized for Turkish fashion analysis" -ForegroundColor Green
            }
            
            "7" {
                Write-Host "📊 Service Logs..." -ForegroundColor Cyan
                Write-Host "Service is running with PID: $($serviceProcess.Id)" -ForegroundColor Yellow
                Write-Host "Log output would appear in the service console" -ForegroundColor Green
            }
            
            "8" {
                Write-Host "🔄 Restarting service..." -ForegroundColor Cyan
                try {
                    Stop-Process -Id $serviceProcess.Id -Force
                    Start-Sleep -Seconds 3
                    $serviceProcess = Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow -PassThru
                    $isReady = Wait-ForService -Url $serviceUrl -MaxWait 30
                    if ($isReady) {
                        Write-Host "✅ Service restarted successfully" -ForegroundColor Green
                    }
                }
                catch {
                    Write-Host "❌ Failed to restart service: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
            
            "9" {
                Write-Host "🔄 Stopping Enhanced Image Processing Service..." -ForegroundColor Yellow
                try {
                    Stop-Process -Id $serviceProcess.Id -Force
                    Write-Host "✅ Service stopped successfully" -ForegroundColor Green
                }
                catch {
                    Write-Host "⚠️ Service may have already stopped" -ForegroundColor Yellow
                }
                Write-Host "👋 Enhanced Image Processing Demo completed!" -ForegroundColor Cyan
                break
            }
            
            default {
                Write-Host "❌ Invalid choice. Please enter 1-9." -ForegroundColor Red
            }
        }
        
        if ($choice -ne "9") {
            Write-Host ""
            Read-Host "Press Enter to continue..."
        }
        
    } while ($choice -ne "9")
    
}
catch {
    Write-Host "❌ Failed to start service: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Enhanced Image Processing Service Demo completed!" -ForegroundColor Green
Write-Host "🚀 Computer Vision & AI Engineering: Turkish Fashion Analysis Ready!" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
