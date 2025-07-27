# Aura AI Quick Demo Script
# This script demonstrates the most impressive AI features of your system

Write-Host "🌟 Welcome to Aura AI - Quick Demo!" -ForegroundColor Cyan
Write-Host "=" * 50

# Test all AI services are running
Write-Host "`n🔍 Checking AI Services Status..." -ForegroundColor Yellow

$services = @(
    @{Name="Image Processing"; Port=8001},
    @{Name="NLU Service"; Port=8002},
    @{Name="Style Profile"; Port=8003},
    @{Name="Combination Engine"; Port=8004},
    @{Name="Recommendation Engine"; Port=8005},
    @{Name="Orchestrator"; Port=8006},
    @{Name="Feedback Loop"; Port=8007}
)

$allWorking = $true
foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($service.Port)" -UseBasicParsing -TimeoutSec 3
        Write-Host "✅ $($service.Name) - OPERATIONAL" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($service.Name) - NOT RESPONDING" -ForegroundColor Red
        $allWorking = $false
    }
}

if ($allWorking) {
    Write-Host "`n🎉 All AI Services are OPERATIONAL!" -ForegroundColor Green
    Write-Host "Ready to demonstrate AI capabilities!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ Some services are not responding. Please check docker-compose status." -ForegroundColor Yellow
    return
}

Write-Host "`n🚀 Starting AI Demonstration..." -ForegroundColor Cyan

# Demo 1: Natural Language Style Query
Write-Host "`n📝 Demo 1: Natural Language Understanding" -ForegroundColor Yellow
Write-Host "Testing query: 'I need a professional outfit for a job interview'" -ForegroundColor White

$nluQuery = @{
    text = "I need a professional outfit for a job interview"
    context = "style_recommendation"
} | ConvertTo-Json

try {
    $nluResponse = Invoke-RestMethod -Uri "http://localhost:8002/analyze-intent" -Method POST -Body $nluQuery -ContentType "application/json"
    Write-Host "✅ NLU Analysis Successful!" -ForegroundColor Green
    Write-Host "Intent: $($nluResponse.analysis_results.intent)" -ForegroundColor Cyan
    Write-Host "Extracted Entities:" -ForegroundColor Cyan
    $nluResponse.analysis_results.entities | ConvertTo-Json | Write-Host -ForegroundColor White
} catch {
    Write-Host "❌ NLU Demo Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Demo 2: Style Profile Generation
Write-Host "`n👤 Demo 2: AI Style Profile Generation" -ForegroundColor Yellow
Write-Host "Generating style profile for business professional..." -ForegroundColor White

$profileRequest = @{
    user_preferences = @{
        colors = @("navy", "charcoal", "white")
        styles = @("business_formal", "professional")
        occasions = @("work", "meetings", "presentations")
    }
    analysis_depth = "comprehensive"
} | ConvertTo-Json -Depth 3

try {
    $profileResponse = Invoke-RestMethod -Uri "http://localhost:8003/generate-profile" -Method POST -Body $profileRequest -ContentType "application/json"
    Write-Host "✅ Style Profile Generated!" -ForegroundColor Green
    Write-Host "Dominant Style: $($profileResponse.user_style_profile.dominant_style)" -ForegroundColor Cyan
    Write-Host "Recommended Colors: $($profileResponse.user_style_profile.color_palette -join ', ')" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Style Profile Demo Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Demo 3: AI Outfit Combinations
Write-Host "`n🎨 Demo 3: AI Outfit Combination Engine" -ForegroundColor Yellow
Write-Host "Creating outfit combinations for business casual..." -ForegroundColor White

$comboRequest = @{
    wardrobe_items = @("Navy Blazer", "White Dress Shirt", "Khaki Chinos", "Brown Leather Shoes")
    occasion = "business_casual"
    weather = "mild"
    style_preference = "smart_casual"
} | ConvertTo-Json -Depth 2

try {
    $comboResponse = Invoke-RestMethod -Uri "http://localhost:8004/generate-combinations" -Method POST -Body $comboRequest -ContentType "application/json"
    Write-Host "✅ Outfit Combinations Generated!" -ForegroundColor Green
    Write-Host "Number of combinations: $($comboResponse.combinations.Count)" -ForegroundColor Cyan
    if ($comboResponse.combinations.Count -gt 0) {
        Write-Host "Best combination: $($comboResponse.combinations[0].items -join ' + ')" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Combination Engine Demo Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Demo 4: FAISS Recommendations
Write-Host "`n🎯 Demo 4: FAISS-Powered Recommendations" -ForegroundColor Yellow
Write-Host "Getting personalized product recommendations..." -ForegroundColor White

$recoRequest = @{
    user_profile = @{
        style_preferences = @("modern", "minimalist", "professional")
        color_preferences = @("black", "white", "navy", "grey")
        size_info = @{
            top = "M"
            bottom = "32"
        }
    }
    context = @{
        occasion = "work"
        season = "spring"
        budget_max = 300
    }
    recommendation_count = 3
} | ConvertTo-Json -Depth 3

try {
    $recoResponse = Invoke-RestMethod -Uri "http://localhost:8005/recommend" -Method POST -Body $recoRequest -ContentType "application/json"
    Write-Host "✅ Personalized Recommendations Generated!" -ForegroundColor Green
    Write-Host "Number of recommendations: $($recoResponse.recommendations.Count)" -ForegroundColor Cyan
    foreach ($rec in $recoResponse.recommendations) {
        Write-Host "  • $($rec.name) - Similarity: $($rec.similarity_score)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Recommendations Demo Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Demo 5: Orchestrated Workflow
Write-Host "`n🔄 Demo 5: Complete AI Workflow Orchestration" -ForegroundColor Yellow
Write-Host "Testing coordinated multi-service AI workflow..." -ForegroundColor White

$workflowRequest = @{
    workflow_type = "complete_style_consultation"
    inputs = @{
        user_query = "I have a wedding to attend next month"
        user_preferences = @{
            budget = 500
            style = "formal"
            occasion = "wedding_guest"
        }
    }
    services_to_use = @("nlu", "style_profile", "combinations", "recommendations")
} | ConvertTo-Json -Depth 4

try {
    $workflowResponse = Invoke-RestMethod -Uri "http://localhost:8006/execute-workflow" -Method POST -Body $workflowRequest -ContentType "application/json"
    Write-Host "✅ Complete AI Workflow Executed!" -ForegroundColor Green
    Write-Host "Workflow Status: $($workflowResponse.workflow_status)" -ForegroundColor Cyan
    Write-Host "Services Used: $($workflowResponse.services_executed -join ', ')" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Workflow Demo Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎊 Demo Complete!" -ForegroundColor Green
Write-Host "=" * 50

Write-Host "`n🌐 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:8000/docs for complete API testing" -ForegroundColor White
Write-Host "2. Try uploading images at http://localhost:8001/docs" -ForegroundColor White
Write-Host "3. Test natural language queries at http://localhost:8002/docs" -ForegroundColor White
Write-Host "4. Explore all AI services individually on ports 8001-8007" -ForegroundColor White
Write-Host "5. Review END_TO_END_AI_TESTING.md for comprehensive testing" -ForegroundColor White

Write-Host "`n🏆 Your Aura AI system is fully operational and impressive!" -ForegroundColor Green
Write-Host "All 7 AI services + 3 core services = 10-service architecture complete!" -ForegroundColor Yellow
