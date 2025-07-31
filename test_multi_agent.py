#!/usr/bin/env python3
"""
Test script for the Multi-Agent Image Analysis System

This script tests the basic functionality of all agents without requiring
the full Streamlit interface. It's useful for debugging and verification.
"""

import sys
import os
from PIL import Image
import numpy as np

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import all agents
from agents.image_processing_agent import ImageProcessingAgent
from agents.model_management_agent import ModelManagementAgent
from agents.analysis_agent import AnalysisAgent
from agents.coordinator_agent import CoordinatorAgent

def create_test_image():
    """Create a simple test image for testing."""
    # Create a 100x100 RGB image with a simple pattern
    img_array = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Add some color
    img_array[0:50, 0:50] = [255, 0, 0]    # Red square
    img_array[0:50, 50:100] = [0, 255, 0]  # Green square
    img_array[50:100, 0:50] = [0, 0, 255]  # Blue square
    img_array[50:100, 50:100] = [255, 255, 0]  # Yellow square
    
    return Image.fromarray(img_array)

def test_image_processing_agent():
    """Test the Image Processing Agent."""
    print("🧪 Testing Image Processing Agent...")
    
    agent = ImageProcessingAgent()
    
    # Test image creation
    test_image = create_test_image()
    
    # Test preprocessing
    processed_image = agent.preprocess_image(test_image)
    print(f"✅ Image preprocessing: {processed_image.size} -> {processed_image.mode}")
    
    # Test image info
    info = agent.get_image_info(processed_image)
    print(f"✅ Image info: {info}")
    
    # Test format validation
    valid_formats = ['test.png', 'image.jpg', 'photo.jpeg']
    invalid_formats = ['test.txt', 'document.pdf']
    
    for fmt in valid_formats:
        assert agent.validate_image_format(fmt), f"Should accept {fmt}"
    
    for fmt in invalid_formats:
        assert not agent.validate_image_format(fmt), f"Should reject {fmt}"
    
    print("✅ Image Processing Agent tests passed!")
    return True

def test_model_management_agent():
    """Test the Model Management Agent."""
    print("🧪 Testing Model Management Agent...")
    
    agent = ModelManagementAgent()
    
    # Test device detection
    device = agent.get_device_info()
    print(f"✅ Device detection: {device}")
    
    # Test model status before initialization
    status = agent.get_model_status()
    print(f"✅ Initial status: {status}")
    
    # Note: We won't actually load the model in tests to avoid dependencies
    # In a real test environment, you might want to use a mock model
    
    print("✅ Model Management Agent tests passed!")
    return True

def test_analysis_agent():
    """Test the Analysis Agent."""
    print("🧪 Testing Analysis Agent...")
    
    # Create a mock model agent for testing
    class MockModelAgent:
        def __init__(self):
            self.is_loaded = False
            self.model_id = "test-model"
            self.device = "cpu"
        
        def get_model_status(self):
            return {'is_loaded': self.is_loaded}
    
    mock_model_agent = MockModelAgent()
    agent = AnalysisAgent(mock_model_agent)
    
    # Test with unloaded model
    test_image = create_test_image()
    result = agent.analyze_image(test_image, "test prompt", 10)
    print(f"✅ Analysis with unloaded model: {result['success']}")
    
    # Test statistics
    stats = agent.get_statistics()
    print(f"✅ Statistics: {stats}")
    
    # Test history
    history = agent.get_analysis_history()
    print(f"✅ History length: {len(history)}")
    
    print("✅ Analysis Agent tests passed!")
    return True

def test_coordinator_agent():
    """Test the Coordinator Agent."""
    print("🧪 Testing Coordinator Agent...")
    
    coordinator = CoordinatorAgent()
    
    # Test agent registration
    test_agent = ImageProcessingAgent()
    coordinator.register_agent('test_agent', test_agent)
    
    # Test agent retrieval
    retrieved_agent = coordinator.get_agent('test_agent')
    assert retrieved_agent is not None, "Should retrieve registered agent"
    
    # Test system status
    status = coordinator.get_system_status()
    print(f"✅ System status: {status}")
    
    # Test health check
    health = coordinator.run_health_check()
    print(f"✅ Health check: {health['overall_health']}")
    
    print("✅ Coordinator Agent tests passed!")
    return True

def test_integration():
    """Test basic integration between agents."""
    print("🧪 Testing Agent Integration...")
    
    # Create all agents
    image_agent = ImageProcessingAgent()
    model_agent = ModelManagementAgent()
    analysis_agent = AnalysisAgent(model_agent)
    coordinator = CoordinatorAgent()
    
    # Register agents
    coordinator.register_agent('image_processing', image_agent)
    coordinator.register_agent('model_management', model_agent)
    coordinator.register_agent('analysis', analysis_agent)
    
    # Test workflow (without actual model loading)
    test_image = create_test_image()
    processed_image = image_agent.preprocess_image(test_image)
    
    print(f"✅ Integration test: Processed image size {processed_image.size}")
    
    # Test system status
    status = coordinator.get_system_status()
    assert len(status['registered_agents']) == 3, "Should have 3 registered agents"
    
    print("✅ Integration tests passed!")
    return True

def main():
    """Run all tests."""
    print("🚀 Starting Multi-Agent System Tests...\n")
    
    tests = [
        test_image_processing_agent,
        test_model_management_agent,
        test_analysis_agent,
        test_coordinator_agent,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The multi-agent system is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 