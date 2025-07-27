# Simple test to isolate the issue
import sys
sys.path.append('.')

try:
    from main import PersonalStyleIntelligence, Phase4PersonalizedRequest
    
    # Test the PersonalIntelligence class directly
    intel = PersonalStyleIntelligence()
    
    # Create a simple request
    request = Phase4PersonalizedRequest(user_id="test", context="casual")
    
    # Test analyze_personalization_match with None style_dna
    result = intel.analyze_personalization_match(None, request)
    print(f"✅ None style_dna test passed: {result}")
    
    # Test with empty dict
    result2 = intel.analyze_personalization_match({}, request)
    print(f"✅ Empty dict test passed: {result2}")
    
    print("🎉 All direct tests passed!")
    
except Exception as e:
    print(f"💥 Error in direct test: {str(e)}")
    import traceback
    traceback.print_exc()
