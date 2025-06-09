"""
Test script to verify all components work correctly
Tests AI agent, AIA generator, and GUI components
"""

import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
        import google.generativeai as genai
        print("✓ Google AI imported successfully")
        
        from PIL import Image
        print("✓ PIL imported successfully")
        
        import tkinter as tk
        print("✓ Tkinter imported successfully")
        
        from ai_agent import AIAgent
        from aia_generator import AIAGenerator
        from config import Config
        from gui import AIAGeneratorGUI
        print("✓ All custom modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration management"""
    print("\nTesting configuration...")
    try:
        from config import Config
        config = Config()
        
        # Test API key storage
        test_key = "test_api_key_12345"
        config.save_api_key(test_key)
        retrieved_key = config.get_api_key()
        
        if retrieved_key == test_key:
            print("✓ API key storage working")
        else:
            print("✗ API key storage failed")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Config test error: {e}")
        return False

def test_aia_generator():
    """Test AIA file generation"""
    print("\nTesting AIA generator...")
    try:
        from aia_generator import AIAGenerator
        generator = AIAGenerator()
        
        # Test data
        test_app_data = {
            "app_name": "TestApp",
            "description": "Test application",
            "screens": [
                {
                    "name": "Screen1",
                    "title": "Test Screen",
                    "components": [
                        {
                            "type": "Button",
                            "name": "Button1",
                            "text": "Click Me",
                            "properties": {
                                "BackgroundColor": "#FF0000",
                                "TextColor": "#FFFFFF"
                            }
                        }
                    ]
                }
            ],
            "blocks": [
                {
                    "event": "Button1.Click",
                    "action": "set Label1.Text to 'Button clicked!'"
                }
            ]
        }
        
        # Generate AIA file
        output_path = generator.create_aia_file(test_app_data)
        
        if os.path.exists(output_path):
            print(f"✓ AIA file generated: {os.path.basename(output_path)}")
            # Clean up
            os.remove(output_path)
            return True
        else:
            print("✗ AIA file generation failed")
            return False
            
    except Exception as e:
        print(f"✗ AIA generator test error: {e}")
        return False

def test_ai_agent_structure():
    """Test AI agent structure without API call"""
    print("\nTesting AI agent structure...")
    try:
        from ai_agent import AIAgent
        
        # Test initialization (will fail without valid API key, but structure should work)
        try:
            agent = AIAgent("dummy_key")
            print("✓ AI agent initialization structure working")
        except Exception as e:
            if "api" in str(e).lower():
                print("✓ AI agent structure working (API key validation expected)")
            else:
                print(f"✗ Unexpected AI agent error: {e}")
                return False
                
        # Test prompt creation
        agent = AIAgent("dummy_key")
        prompt = agent._create_detailed_prompt("Create a simple calculator app")
        
        if "JSON" in prompt and "app_name" in prompt:
            print("✓ Prompt generation working")
        else:
            print("✗ Prompt generation failed")
            return False
            
        return True
    except Exception as e:
        print(f"✗ AI agent test error: {e}")
        return False

def test_gui_structure():
    """Test GUI structure without display"""
    print("\nTesting GUI structure...")
    try:
        import tkinter as tk
        from gui import AIAGeneratorGUI
        
        # Create root window (won't display in headless mode)
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test GUI initialization
        app = AIAGeneratorGUI(root)
        
        # Check if key components exist
        if hasattr(app, 'api_key_var') and hasattr(app, 'prompt_text'):
            print("✓ GUI components initialized correctly")
        else:
            print("✗ GUI components missing")
            return False
            
        root.destroy()
        return True
    except Exception as e:
        print(f"✗ GUI test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("MIT App Inventor AIA Generator - Component Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_aia_generator,
        test_ai_agent_structure,
        test_gui_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All tests passed! Application is ready for deployment.")
        return True
    else:
        print("✗ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)