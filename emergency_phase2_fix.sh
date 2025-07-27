# 🚨 PHASE 2: CRITICAL FINAL FIXES
# Emergency script to fix remaining critical issues and reach 85%+ target

echo "🚨 PHASE 2: EMERGENCY FINAL FIXES"
echo "=================================="

echo "🔧 1. Fixing Image Processing Service..."
# Restart image processing with proper error handling
docker-compose restart image-processing-service

echo "🔧 2. Starting Missing Services..."
# Start all services to fix 4/8 availability issue
docker-compose up -d

echo "🔧 3. Waiting for services to stabilize..."
sleep 10

echo "🔧 4. Testing AI Image Analysis..."
# Test if enhanced analyzer works
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/shirt.jpg", "image_description": "A stylish blue cotton shirt"}' \
  --connect-timeout 5

echo ""
echo "🔧 5. Testing Enhanced Health Checks..."
# Test enhanced monitoring
curl http://localhost:8001/health --connect-timeout 3
curl http://localhost:8001/performance_metrics --connect-timeout 3

echo ""
echo "🔧 6. Service Status Summary..."
# Check all services
for port in 8000 8001 8002 8003 8004 8005 8006 8007; do
  echo -n "Port $port: "
  curl -s http://localhost:$port/health --connect-timeout 2 > /dev/null && echo "✅ UP" || echo "❌ DOWN"
done

echo ""
echo "🎯 Final Validation - Run this after fixes:"
echo "python phase2_final_validator.py"
echo "=================================="
