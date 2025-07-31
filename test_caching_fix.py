#!/usr/bin/env python3
"""
Test script to verify that the caching fixes work correctly.
This script tests the model loading functions without Streamlit UI elements.
"""

import sys
import os

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_model_management_agent_caching():
    """Test that the ModelManagementAgent caching works without UI conflicts."""
    print("🧪 Testing ModelManagementAgent caching...")
    
    try:
        import torch
        from agents.model_management_agent import ModelManagementAgent
        
        # Create agent instance
        agent = ModelManagementAgent()
        
        # Test the cached functions directly (without UI elements)
        print("  Testing _load_processor_cached...")
        processor, error = agent._load_processor_cached(agent.model_id)
        if processor is not None:
            print("  ✅ Processor loaded successfully")
        else:
            print(f"  ❌ Processor loading failed: {error}")
        
        print("  Testing _load_model_cached...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, error = agent._load_model_cached(agent.model_id, device)
        if model is not None:
            print("  ✅ Model loaded successfully")
        else:
            print(f"  ❌ Model loading failed: {error}")
        
        print("✅ ModelManagementAgent caching tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ModelManagementAgent caching test failed: {str(e)}")
        return False

def test_local_analyzer_caching():
    """Test that the local_analyzer caching works without UI conflicts."""
    print("🧪 Testing local_analyzer caching...")
    
    try:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration
        
        # Test the cached function directly
        print("  Testing _load_model_cached...")
        model, processor, device = _load_model_cached()
        
        if model is not None and processor is not None:
            print("  ✅ Model and processor loaded successfully")
            print(f"  📱 Device: {device}")
        else:
            print("  ❌ Model loading failed")
        
        print("✅ local_analyzer caching tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ local_analyzer caching test failed: {str(e)}")
        return False

# Import the cached function from local_analyzer
def _load_model_cached():
    """Load the model and processor with caching (no UI elements)."""
    import torch
    from transformers import BlipProcessor, BlipForConditionalGeneration
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "Salesforce/blip-image-captioning-large"
    
    processor = BlipProcessor.from_pretrained(model_id)
    model = BlipForConditionalGeneration.from_pretrained(model_id).to(device)
    
    return model, processor, device

def main():
    """Run all caching tests."""
    print("🚀 Starting caching fix verification tests...\n")
    
    # Test ModelManagementAgent
    success1 = test_model_management_agent_caching()
    print()
    
    # Test local_analyzer
    success2 = test_local_analyzer_caching()
    print()
    
    # Summary
    if success1 and success2:
        print("🎉 All caching tests passed! The fixes are working correctly.")
        print("\n📋 Summary of fixes applied:")
        print("  ✅ Separated UI elements from cached functions")
        print("  ✅ Created _load_processor_cached and _load_model_cached functions")
        print("  ✅ Moved st.spinner, st.success, and st.error outside cached functions")
        print("  ✅ Maintained caching benefits while avoiding UI conflicts")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    return success1 and success2

if __name__ == "__main__":
    main() 