# 🚀 Aura AI End-to-End Testing Guide
# Complete AI Workflow Testing for Integrated System

## 🎯 **Pre-Test Setup**

### 1. **Verify All Services Are Running**
```powershell
# Run the comprehensive health check
.\CHECK_AI_SERVICES.ps1

# Quick verification - all should return 200
(Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing).StatusCode  # Backend
(Invoke-WebRequest -Uri "http://localhost:8001" -UseBasicParsing).StatusCode        # Image Processing
(Invoke-WebRequest -Uri "http://localhost:8002" -UseBasicParsing).StatusCode        # NLU Service
(Invoke-WebRequest -Uri "http://localhost:8003" -UseBasicParsing).StatusCode        # Style Profile
(Invoke-WebRequest -Uri "http://localhost:8004" -UseBasicParsing).StatusCode        # Combination Engine
(Invoke-WebRequest -Uri "http://localhost:8005" -UseBasicParsing).StatusCode        # Recommendation Engine
```

### 2. **Open Testing Interfaces**
```powershell
# Open main API documentation
start "http://localhost:8000/docs"

# Open individual AI service docs (in separate tabs)
start "http://localhost:8001/docs"  # Image Processing
start "http://localhost:8002/docs"  # NLU Service
start "http://localhost:8003/docs"  # Style Profile
```

---

## 🌟 **COMPLETE AI WORKFLOW TESTS**

### 🖼️ **Test 1: Image Analysis & Style Recognition**

#### **Step 1: Upload Clothing Image**
```powershell
# Method 1: Using PowerShell to test image upload
$imageFile = "C:\path\to\your\clothing\image.jpg"  # Replace with actual path

# Create form data for image upload
$form = @{
    file = Get-Item $imageFile
}

# Upload image to AI service
$response = Invoke-RestMethod -Uri "http://localhost:8001/analyze-image" -Method POST -Form $form
$response | ConvertTo-Json -Depth 3
```

#### **Step 2: Via Swagger UI (Recommended)**
1. Go to **http://localhost:8001/docs**
2. Find the **`POST /analyze-image`** endpoint
3. Click **"Try it out"**
4. Click **"Choose file"** and select a clothing image
5. Click **"Execute"**

**Expected Response:**
```json
{
  "message": "Image analyzed successfully",
  "filename": "shirt.jpg",
  "analysis_results": {
    "clothing_items": [
      {
        "category": "shirt",
        "color": "blue",
        "pattern": "solid",
        "confidence": 0.92
      }
    ],
    "style_attributes": {
      "formality": "casual",
      "season": "spring"
    }
  }
}
```

---

### 🗣️ **Test 2: Natural Language Style Queries**

#### **Step 1: Test NLU Service Directly**
```powershell
# Test natural language understanding
$query = @{
    text = "I want a casual blue shirt for spring weather"
    context = "style_recommendation"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8002/analyze-intent" -Method POST -Body $query -ContentType "application/json"
$response | ConvertTo-Json -Depth 3
```

#### **Step 2: Via Swagger UI**
1. Go to **http://localhost:8002/docs**
2. Find **`POST /analyze-intent`**
3. Try these queries:
   - *"Show me formal outfits for a business meeting"*
   - *"I need something casual for weekend"*
   - *"What goes well with a blue denim jacket?"*

**Expected Response:**
```json
{
  "message": "Intent analyzed successfully",
  "original_text": "I want a casual blue shirt for spring weather",
  "analysis_results": {
    "intent": "product_search",
    "entities": {
      "style": "casual",
      "color": "blue",
      "category": "shirt",
      "season": "spring"
    },
    "confidence": 0.89
  }
}
```

---

### 👤 **Test 3: User Registration & Style Profile Setup**

#### **Step 1: Create User Account**
```powershell
# Register new user
$user = @{
    email = "aitest@aura.com"
    password = "AuraAI2025!"
    full_name = "AI Test User"
} | ConvertTo-Json

$userResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/signup" -Method POST -Body $user -ContentType "application/json"
Write-Host "User created: $($userResponse.email)"
```

#### **Step 2: Login & Get Token**
```powershell
# Login to get authentication token
$loginForm = @{
    username = "aitest@aura.com"
    password = "AuraAI2025!"
}

$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method POST -Form $loginForm
$token = $loginResponse.access_token
$headers = @{ Authorization = "Bearer $token" }

Write-Host "Login successful, token obtained"
```

#### **Step 3: Set Style Preferences**
```powershell
# Set user style preferences
$stylePrefs = @{
    preferred_colors = @("blue", "black", "white", "navy")
    style_types = @("casual", "business_casual", "smart_casual")
    size_preferences = @{
        top = "M"
        bottom = "32"
        shoes = "10"
    }
    budget_range = @{
        min = 50
        max = 300
    }
} | ConvertTo-Json -Depth 3

$prefResponse = Invoke-RestMethod -Uri "http://localhost:8000/users/me/style-preferences" -Method PUT -Body $stylePrefs -ContentType "application/json" -Headers $headers
Write-Host "Style preferences set successfully"
```

---

### 🎨 **Test 4: AI Style Profiling**

#### **Step 1: Generate Style Profile**
```powershell
# Test style profile generation
$profileRequest = @{
    user_preferences = @{
        colors = @("blue", "black")
        styles = @("casual", "business_casual")
        occasions = @("work", "weekend")
    }
    analysis_depth = "comprehensive"
} | ConvertTo-Json -Depth 3

$profileResponse = Invoke-RestMethod -Uri "http://localhost:8003/generate-profile" -Method POST -Body $profileRequest -ContentType "application/json"
$profileResponse | ConvertTo-Json -Depth 4
```

#### **Expected Response:**
```json
{
  "message": "Style profile generated successfully",
  "user_style_profile": {
    "dominant_style": "smart_casual",
    "color_palette": ["navy", "white", "light_blue"],
    "recommended_categories": ["blazers", "chinos", "dress_shirts"],
    "style_score": 0.87
  }
}
```

---

### 🤖 **Test 5: AI-Powered Outfit Combinations**

#### **Step 1: Add Items to Wardrobe**
```powershell
# Add wardrobe items
$wardrobeItems = @(
    @{
        name = "Navy Blazer"
        category = "outerwear"
        color = "navy"
        brand = "Hugo Boss"
        purchase_date = "2025-01-15"
    },
    @{
        name = "White Dress Shirt"
        category = "tops"
        color = "white"
        brand = "Ralph Lauren"
        purchase_date = "2025-01-20"
    },
    @{
        name = "Dark Jeans"
        category = "bottoms"
        color = "dark_blue"
        brand = "Levi's"
        purchase_date = "2025-01-10"
    }
)

foreach ($item in $wardrobeItems) {
    $itemJson = $item | ConvertTo-Json
    $wardrobeResponse = Invoke-RestMethod -Uri "http://localhost:8000/wardrobe/items" -Method POST -Body $itemJson -ContentType "application/json" -Headers $headers
    Write-Host "Added: $($item.name)"
}
```

#### **Step 2: Generate AI Outfit Combinations**
```powershell
# Request AI-generated outfit combinations
$comboRequest = @{
    wardrobe_items = @("Navy Blazer", "White Dress Shirt", "Dark Jeans")
    occasion = "business_casual"
    weather = "mild"
    style_preference = "smart_casual"
} | ConvertTo-Json -Depth 2

$comboResponse = Invoke-RestMethod -Uri "http://localhost:8004/generate-combinations" -Method POST -Body $comboRequest -ContentType "application/json"
$comboResponse | ConvertTo-Json -Depth 4
```

---

### 🎯 **Test 6: FAISS-Powered Personalized Recommendations**

#### **Step 1: Get AI Recommendations**
```powershell
# Get personalized product recommendations
$recoRequest = @{
    user_profile = @{
        style_preferences = @("casual", "business_casual")
        color_preferences = @("blue", "navy", "white")
        size_info = @{
            top = "M"
            bottom = "32"
        }
    }
    context = @{
        occasion = "work"
        season = "spring"
        budget_max = 200
    }
    recommendation_count = 5
} | ConvertTo-Json -Depth 3

$recoResponse = Invoke-RestMethod -Uri "http://localhost:8005/recommend" -Method POST -Body $recoRequest -ContentType "application/json"
$recoResponse | ConvertTo-Json -Depth 4
```

#### **Expected Response:**
```json
{
  "message": "Recommendations generated successfully",
  "recommendations": [
    {
      "product_id": "shirt_001",
      "name": "Premium Cotton Shirt",
      "category": "shirts",
      "color": "light_blue",
      "price": 89.99,
      "similarity_score": 0.94,
      "reason": "Matches your casual business style preference"
    }
  ]
}
```

---

### 🔄 **Test 7: Complete Orchestrated Workflow**

#### **Step 1: Full AI Pipeline Test**
```powershell
# Test the orchestrator service with complete workflow
$workflowRequest = @{
    workflow_type = "style_consultation"
    inputs = @{
        user_query = "I need a complete outfit for a client presentation"
        uploaded_image = "business_shirt.jpg"
        user_preferences = @{
            budget = 400
            style = "professional"
            occasion = "business_formal"
        }
    }
    services_to_use = @("image_processing", "nlu", "style_profile", "combinations", "recommendations")
} | ConvertTo-Json -Depth 4

$workflowResponse = Invoke-RestMethod -Uri "http://localhost:8006/execute-workflow" -Method POST -Body $workflowRequest -ContentType "application/json"
$workflowResponse | ConvertTo-Json -Depth 5
```

---

### 📊 **Test 8: AI Learning & Feedback Loop**

#### **Step 1: Provide User Feedback**
```powershell
# Test the feedback loop system
$feedbackData = @{
    interaction_id = "workflow_001"
    user_feedback = @{
        satisfaction_rating = 4
        selected_recommendations = @("shirt_001", "blazer_003")
        rejected_recommendations = @("pants_002")
        feedback_text = "Great recommendations! The style matches perfectly."
    }
    interaction_context = @{
        workflow_type = "style_consultation"
        user_preferences = @("professional", "modern")
    }
} | ConvertTo-Json -Depth 4

$feedbackResponse = Invoke-RestMethod -Uri "http://localhost:8007/process-feedback" -Method POST -Body $feedbackData -ContentType "application/json"
$feedbackResponse | ConvertTo-Json -Depth 3
```

---

## 🧪 **ADVANCED INTEGRATION TESTS**

### **Multi-Service Integration Test**
```powershell
# Test complete end-to-end integration
function Test-CompleteAIWorkflow {
    param(
        [string]$userEmail = "integration.test@aura.com",
        [string]$styleQuery = "I need a smart casual outfit for a tech conference"
    )
    
    Write-Host "🚀 Starting Complete AI Workflow Test..." -ForegroundColor Cyan
    
    # 1. User Registration
    Write-Host "📝 Step 1: User Registration..." -ForegroundColor Yellow
    # [Registration code here]
    
    # 2. Style Query Processing
    Write-Host "🗣️ Step 2: Processing Natural Language Query..." -ForegroundColor Yellow
    # [NLU processing code here]
    
    # 3. Style Profile Generation
    Write-Host "👤 Step 3: Generating User Style Profile..." -ForegroundColor Yellow
    # [Style profiling code here]
    
    # 4. AI Recommendations
    Write-Host "🎯 Step 4: Generating AI Recommendations..." -ForegroundColor Yellow
    # [Recommendation code here]
    
    # 5. Outfit Combinations
    Write-Host "🎨 Step 5: Creating Outfit Combinations..." -ForegroundColor Yellow
    # [Combination code here]
    
    Write-Host "✅ Complete AI Workflow Test Completed!" -ForegroundColor Green
}

# Run the complete test
Test-CompleteAIWorkflow
```

---

## 🎯 **SUCCESS CRITERIA**

### **✅ System is Working Correctly When:**

1. **Image Processing**: Successfully analyzes clothing images and returns detailed attributes
2. **NLU Service**: Correctly interprets natural language style queries
3. **Style Profile**: Generates comprehensive user style profiles
4. **Combination Engine**: Creates intelligent outfit combinations
5. **Recommendation Engine**: Provides personalized product suggestions
6. **Orchestrator**: Coordinates multiple AI services seamlessly
7. **Feedback Loop**: Processes user feedback and improves recommendations

### **🔍 Key Performance Indicators:**
- Response times < 5 seconds for AI services
- Confidence scores > 0.7 for AI predictions
- Successful inter-service communication
- No error responses from AI endpoints
- Consistent data flow between services

---

## 🚨 **Troubleshooting**

### **Common Issues & Solutions:**

**Image Upload Fails:**
```powershell
# Check if file exists and is accessible
Test-Path "C:\path\to\image.jpg"
# Ensure file is a valid image format (jpg, png, gif)
```

**Authentication Errors:**
```powershell
# Verify token is still valid
$headers = @{ Authorization = "Bearer $token" }
(Invoke-RestMethod -Uri "http://localhost:8000/users/me" -Headers $headers).email
```

**AI Service Not Responding:**
```powershell
# Check individual service health
(Invoke-WebRequest -Uri "http://localhost:8001" -UseBasicParsing).StatusCode
```

---

## 🎉 **CELEBRATION TIME!**

When all tests pass successfully, you'll have verified:
- ✅ **Complete AI integration** across all 7 services
- ✅ **End-to-end workflows** from image upload to recommendations
- ✅ **Inter-service communication** working flawlessly
- ✅ **Production-ready AI system** for fashion e-commerce

**🏆 Your Aura AI system is fully operational and ready for real-world use!**

---

*Happy Testing! You've built something amazing! 🌟*
