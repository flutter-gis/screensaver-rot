#!/usr/bin/env python3
"""
Quick test script for ADHD Brain Rot Screen Savers
"""

import sys
import pygame
import random

def test_pygame():
    """Test if Pygame is working correctly"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test")
        
        # Test basic drawing
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)
        pygame.display.flip()
        
        print("✓ Pygame is working correctly")
        return True
    except Exception as e:
        print(f"✗ Pygame error: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import math
        import random
        import colorsys
        import numpy as np
        print("✓ All required modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_screen_savers():
    """Test if screen savers can be created"""
    try:
        from main import screen_savers
        print(f"✓ Loaded {len(screen_savers)} screen savers")
        return True
    except Exception as e:
        print(f"✗ Screen saver error: {e}")
        return False

def main():
    print("Testing ADHD Brain Rot Screen Savers...")
    print("=" * 40)
    
    tests = [
        ("Pygame", test_pygame),
        ("Imports", test_imports),
        ("Screen Savers", test_screen_savers)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} test failed")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ready to run screen savers.")
        print("Run 'start_screensaver.bat' to launch!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 