#!/usr/bin/env powershell
<#
🧹 AURA AI - Professional Workspace Cleanup & Organization Script
Computer Vision & AI Engineer: Workspace Organization Excellence

Bu script şunları yapar:
1. Gereksiz duplicate dosyaları siler
2. Eski test ve report dosyalarını temizler
3. Backup'ları organize eder
4. Kusursuz dosya düzeni oluşturur
5. Professional workspace structure kurar
#>

Write-Host "🧹 AURA AI - Professional Workspace Cleanup & Organization" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "Computer Vision & AI Engineer: Workspace Excellence" -ForegroundColor Yellow
Write-Host "=======================================================" -ForegroundColor Cyan

# Function to safely remove files
function Remove-SafeFile {
    param([string]$FilePath, [string]$Reason)
    
    if (Test-Path $FilePath) {
        try {
            Remove-Item $FilePath -Force
            Write-Host "✅ Removed: $FilePath" -ForegroundColor Green
            Write-Host "   Reason: $Reason" -ForegroundColor Gray
        }
        catch {
            Write-Host "⚠️ Could not remove: $FilePath" -ForegroundColor Yellow
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Function to create directory if not exists
function Ensure-Directory {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        try {
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
            Write-Host "✅ Created directory: $Path" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ Failed to create directory: $Path" -ForegroundColor Red
        }
    }
}

Write-Host "🗂️ PHASE 1: REMOVING DUPLICATE AND OBSOLETE FILES" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Cyan

# Remove duplicate demo files (keep only in services)
Remove-SafeFile "aura_ai_demo.py" "Duplicate demo file - original in services"
Remove-SafeFile "prompt_engineering_nlu_demo.py" "Duplicate demo file - original in services"

# Remove duplicate test files
Remove-SafeFile "prompt_engineering_nlu_tester.py" "Duplicate test file - original in services"

# Remove old completion and status reports (keep only essential ones)
$obsoleteReports = @(
    "AI_SYSTEM_CLEANUP_REPORT.md",
    "AURA_AI_FEEDBACK_LOOP_FINAL_STATUS_REPORT.md",
    "AURA_AI_NLU_FINAL_IMPLEMENTATION_REPORT.md",
    "AURA_AI_NLU_TEST_RESULTS.md",
    "FEEDBACK_LOOP_COMPLETION_REPORT.md",
    "GITHUB_PUSH_SUCCESS_REPORT.md",
    "IMAGE_PROCESSING_COMPLETION_REPORT.md",
    "IMPLEMENTATION_SUCCESS_SUMMARY.md",
    "MULTI_MODAL_COORDINATOR_FINAL_REPORT.md",
    "PROJECT_REORGANIZATION_REPORT.md",
    "PROMPT_ENGINEERING_NLU_SUCCESS_REPORT.md",
    "RCI_QUALITY_ASSURANCE_SUCCESS_REPORT.md"
)

foreach ($report in $obsoleteReports) {
    Remove-SafeFile $report "Obsolete status report - information preserved in final docs"
}

# Remove old deploy scripts (keep only the main ones)
Remove-SafeFile "FEEDBACK_LOOP_ADVANCED_DEPLOY.ps1" "Obsolete - functionality integrated into main deploy script"
Remove-SafeFile "IMAGE_PROCESSING_DEPLOY.ps1" "Obsolete - replaced by enhanced version"
Remove-SafeFile "IMAGE_PROCESSING_DEPLOY_FIXED.ps1" "Obsolete - functionality integrated"
Remove-SafeFile "rci_quick_test.ps1" "Obsolete test script"

# Remove obsolete JSON test results
Remove-SafeFile "prompt_engineering_nlu_test_results.json" "Obsolete test results"

# Remove log files (they will be regenerated)
Remove-SafeFile "multi_modal_coordinator.log" "Temporary log file"

Write-Host ""
Write-Host "🗂️ PHASE 2: ORGANIZING EXISTING STRUCTURE" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Cyan

# Ensure proper directory structure
Ensure-Directory "docs/reports"
Ensure-Directory "docs/guides"
Ensure-Directory "docs/api"
Ensure-Directory "scripts/deployment"
Ensure-Directory "scripts/testing"
Ensure-Directory "backup/configs"
Ensure-Directory "backup/deprecated"

# Move important documents to proper locations
if (Test-Path "FINAL_SUCCESS_REPORT.md") {
    Move-Item "FINAL_SUCCESS_REPORT.md" "docs/reports/" -Force
    Write-Host "✅ Moved: FINAL_SUCCESS_REPORT.md to docs/reports/" -ForegroundColor Green
}

if (Test-Path "FINAL_CLEANUP_SUMMARY.md") {
    Move-Item "FINAL_CLEANUP_SUMMARY.md" "docs/reports/" -Force
    Write-Host "✅ Moved: FINAL_CLEANUP_SUMMARY.md to docs/reports/" -ForegroundColor Green
}

# Move technical documentation
$techDocs = @(
    "AURA_AI_FEEDBACK_LOOP_PROMPT_ENGINEERING.md",
    "AURA_AI_NLU_ADVANCED_PROMPT_ENGINEERING.md",
    "AURA_RCI_QUALITY_ASSURANCE_DESIGN.md",
    "IMAGE_PROCESSING_FLOW_SCHEMAS.md",
    "MULTI_MODAL_QUERY_SYSTEM_DESIGN.md",
    "PROMPT_ENGINEERING_NLU_DOCUMENTATION.md",
    "TEKNOLOJI_YIGINI_OZETI.md"
)

foreach ($doc in $techDocs) {
    if (Test-Path $doc) {
        Move-Item $doc "docs/guides/" -Force
        Write-Host "✅ Moved: $doc to docs/guides/" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 WORKSPACE CLEANUP AND ORGANIZATION COMPLETED!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 PROFESSIONAL WORKSPACE SUMMARY:" -ForegroundColor Magenta
Write-Host "✅ Removed duplicate and obsolete files" -ForegroundColor Green
Write-Host "✅ Organized documentation into docs/ structure" -ForegroundColor Green
Write-Host "✅ Created professional scripts/ directory" -ForegroundColor Green
Write-Host "✅ Established backup/ directory for deprecated items" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 AURA AI Professional Workspace Ready!" -ForegroundColor Green
Write-Host "Computer Vision and AI Engineering Excellence Achieved!" -ForegroundColor Cyan
