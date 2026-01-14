#!/usr/bin/env python3
"""Test script to verify the new input/output features"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_challenge_with_input():
    """Test Challenge 11 - Sum Two Numbers with input"""
    print("Testing Challenge 11: Sum Two Numbers...")
    
    # Test code that reads input and prints output
    code = """a, b = map(int, input().split())
print(a + b)"""
    
    response = requests.post(f"{BASE_URL}/api/execute", 
                            json={"code": code, "challenge_id": 11})
    result = response.json()
    
    print(f"  Passed: {result['passed']}")
    for test in result['results']:
        status = "✓" if test['passed'] else "✗"
        print(f"  {status} {test['description']}")
        if 'input' in test:
            print(f"    Input: {test['input']}")
        if 'expected' in test:
            print(f"    Expected: {test['expected']}")
        if 'actual' in test:
            print(f"    Got: {test['actual']}")
    print()

def test_greeting_challenge():
    """Test Challenge 12 - Greeting with Name"""
    print("Testing Challenge 12: Greeting with Name...")
    
    code = """name = input()
print(f'Hello, {name}!')"""
    
    response = requests.post(f"{BASE_URL}/api/execute",
                            json={"code": code, "challenge_id": 12})
    result = response.json()
    
    print(f"  Passed: {result['passed']}")
    for test in result['results']:
        status = "✓" if test['passed'] else "✗"
        print(f"  {status} {test['description']}")
    print()

def test_imports_and_multiline():
    """Test that imports work"""
    print("Testing imports and multi-line code...")
    
    # For challenge 13 (Count Words)
    code = """import sys
sentence = input()
words = sentence.split()
print(len(words))"""
    
    response = requests.post(f"{BASE_URL}/api/execute",
                            json={"code": code, "challenge_id": 13})
    result = response.json()
    
    print(f"  Passed: {result['passed']}")
    print()

def test_old_challenges_still_work():
    """Test that old one-liner challenges still work"""
    print("Testing Challenge 1: Square Numbers (one-liner)...")
    
    # One-liner should still work
    code = "[x**2 for x in range(1, 6)]"
    
    response = requests.post(f"{BASE_URL}/api/execute",
                            json={"code": code, "challenge_id": 1})
    result = response.json()
    
    print(f"  Passed: {result['passed']}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Testing New Python Editor Features")
    print("=" * 50)
    print()
    
    try:
        test_old_challenges_still_work()
        test_challenge_with_input()
        test_greeting_challenge()
        test_imports_and_multiline()
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
