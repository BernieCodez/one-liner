#!/usr/bin/env python3
"""
Easy Challenge Setup Tool

This script makes it super easy to replace the first 15 challenges with your own problems.
Just edit the CHALLENGES list below with your problems, then run: python setup_challenges.py
"""

# ============================================================================
# EDIT YOUR CHALLENGES BELOW - Replace these with your own 15 problems!
# ============================================================================

CHALLENGES = [
    # Challenge 1: First Contact
    {
        "id": 1,
        "title": "🌍 First Contact",
        "difficulty": "Easy",
        "description": """
## Challenge 1: First Contact

You are sent in a space ship to circle the globe. Your space ship has entered orbit, the planet Earth glows before you. The commander asks you what you see. You respond with a simple phrase, "Hello World!".

**Expected Output:** `Hello World!`

**Explanation:** Print the string "Hello World!"

**Example:**
```python
# Your one-liner should print: Hello World!
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "Hello World!",
                "description": "Should print 'Hello World!'"
            }
        ],
        "solution": "print(\"Hello World!\")",
        "solvable_in_one_line": True
    },
    
    # Challenge 2: The Backwards Transmission
    {
        "id": 2,
        "title": "📡 The Backwards Transmission",
        "difficulty": "Easy",
        "description": """
## Challenge 2: The Backwards Transmission

Your spaceship intercepts an alien transmission. The message appears garbled and incomprehensible. After running it through your ship's universal translator, you realize the aliens communicate by reversing their messages! To understand what they're saying, you need to read the transmission backwards.

**Input:** `!emosewa si nohtyP`

**Expected Output:** `Python is awesome!`

**Explanation:** The reverse of '!emosewa si nohtyP' is 'Python is awesome!'.

**Example:**
```python
# Your one-liner should reverse the input string
```
""",
        "test_cases": [
            {
                "input": "!emosewa si nohtyP",
                "expected": "Python is awesome!",
                "description": "Should reverse the input string"
            },
            {
                "input": "!enod llew yreV",
                "expected": "Very well done!",
                "description": "Hidden test case"
            }
        ],
        "solution": "print(input()[::-1])",
        "solvable_in_one_line": True
    },
    
    # Challenge 3: The Odd Beacon Protocol
    {
        "id": 3,
        "title": "☄️ The Odd Beacon Protocol",
        "difficulty": "Easy",
        "description": """
## Challenge 3: The Odd Beacon Protocol

Your ship's navigation computer has malfunctioned! The asteroid field ahead is marked with numbered beacons from 0 to N. The engineer explains that only the "strange" beacons are safe to pass through—these are beacons whose number, when divided by 2, leaves a remainder of 1. You need to identify all safe beacons to plot your course through the field.

**Input:** `7`

**Expected Output:** `[1, 3, 5, 7]`

**Explanation:** Starting from 0, check each number: 0÷2 has remainder 0 (unsafe). 1÷2 has remainder 1 (safe). 2÷2 has remainder 0 (unsafe). 3÷2 has remainder 1 (safe). This pattern continues through 7.

**Example:**
```python
# Your one-liner should return a list of odd numbers from 1 to N
```
""",
        "test_cases": [
            {
                "input": "7",
                "expected": "[1, 3, 5, 7]",
                "description": "Should return list of odd numbers from 1 to 7"
            },
            {
                "input": "68",
                "expected": "[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67]",
                "description": "Hidden test case with larger input"
            }
        ],
        "solution": "print(list(range(1, int(input())+1, 2)))",
        "solvable_in_one_line": True
    },
    
    # Challenge 4: Power Cell Diagnostic
    {
        "id": 4,
        "title": "🔋 Power Cell Diagnostic",
        "difficulty": "Easy",
        "description": """
## Challenge 4: Power Cell Diagnostic

Your cargo bay contains 99 fuel cells arranged along the wall. Each cell shows a charge level from 0 (empty) to 10 (full). Mission control asks you to check a specific fuel cell by its position to determine if you have enough power for the next jump to hyperspace. You'll receive the charge levels of all 99 cells, then the index of the cell to check.

**Input:** 
```
7 5 2 0 6 7 6 9 5 3 2 2 1 8 2 9 10 0 2 4 8 0 6 10 5 5 1 5 7 9 8 9 2 3 7 2 5 2 9 3 4 9 2 0 10 3 4 0 5 6 4 7 10 2 3 4 9 5 5 5 0 5 10 6 5 0 2 6 4 2 3 5 10 0 7 1 1 4 0 6 1 7 0 6 10 4 1 3 5 4 9 4 2 2 4 9 10 3 0
99
```

**Expected Output:** `0`

**Explanation:** The 99th fuel cell (index 98 in 0-based indexing, or index 99 in 1-based) has a charge level of 0.

**Example:**
```python
# Your one-liner should get the value at the specified index
```
""",
        "test_cases": [
            {
                "input": "7 5 2 0 6 7 6 9 5 3 2 2 1 8 2 9 10 0 2 4 8 0 6 10 5 5 1 5 7 9 8 9 2 3 7 2 5 2 9 3 4 9 2 0 10 3 4 0 5 6 4 7 10 2 3 4 9 5 5 5 0 5 10 6 5 0 2 6 4 2 3 5 10 0 7 1 1 4 0 6 1 7 0 6 10 4 1 3 5 4 9 4 2 2 4 9 10 3 0\n99",
                "expected": "0",
                "description": "Should return the 99th element"
            }
        ],
        "solution": "print([int(x) for x in input().split()][int(input())-1])",
        "solvable_in_one_line": True
    },
    
    # Challenge 5: Treasure Coordinates
    {
        "id": 5,
        "title": "🗺️ Treasure Coordinates",
        "difficulty": "Easy",
        "description": """
## Challenge 5: Treasure Coordinates

You discover a derelict alien spacecraft floating in space. Inside, you find data tablets scattered across the floor. Each tablet displays a number—coordinates to a hidden treasure planet! Your ship's AI determines that you need to sum all the coordinates together to find the exact location.

**Input:** `1,2,3,4,5,6,7,8,9,10`

**Expected Output:** `55`

**Explanation:** 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 = 55

**Example:**
```python
# Your one-liner should sum all comma-separated numbers
```
""",
        "test_cases": [
            {
                "input": "1,2,3,4,5,6,7,8,9,10",
                "expected": "55",
                "description": "Should sum all numbers"
            },
            {
                "input": "46,99,53,50,23,60,57,98,52,45,65,27,100,93,57,56,87,91,47,81,84,44,86,25,62",
                "expected": "1588",
                "description": "Hidden test case with more numbers"
            }
        ],
        "solution": "print(sum([int(x) for x in input().split(',')]))",
        "solvable_in_one_line": True
    },
    
    # Challenge 6: Rally for the Rover
    {
        "id": 6,
        "title": "🏆 Rally for the Rover",
        "difficulty": "Medium",
        "description": """
## Challenge 6: Rally for the Rover

You're competing in the Galactic Rally Race for a brand new space rover (a Toyota, naturally). The final challenge is a pattern recognition test used by ancient star navigators. You watch other racers examining phrases and determining if they're palindromes—words that read the same forwards and backwards. You quickly code a program to help you win the rover!

**Input:** `A Toyota`

**Expected Output:** `True`

**Explanation:** Converting "A Toyota" to lowercase and removing spaces gives "atoyota", which reads the same backwards—a perfect palindrome!

**Example:**
```python
# Your one-liner should check if the input is a palindrome (ignoring case and spaces)
```
""",
        "test_cases": [
            {
                "input": "A Toyota",
                "expected": "True",
                "description": "Should return True for palindrome"
            },
            {
                "input": "Race cars",
                "expected": "False",
                "description": "Should return False for non-palindrome"
            },
            {
                "input": "Pull up if I pull up",
                "expected": "True",
                "description": "Hidden test case"
            },
            {
                "input": "waSsAw",
                "expected": "True",
                "description": "Hidden test case"
            }
        ],
        "solution": "print((s:=input().replace(' ','').lower())==s[::-1])",
        "solvable_in_one_line": True
    },
    
    # Challenge 7: Quantum Factorial Duel
    {
        "id": 7,
        "title": "⚛️ Quantum Factorial Duel",
        "difficulty": "Medium",
        "description": """
## Challenge 7: Quantum Factorial Duel

You're approached by a quantum mathematician from the Andromeda galaxy who challenges you to a speed calculation duel. They rapidly call out numbers, and you must calculate their factorials before the hyperdrive cooldown expires! Each factorial represents the number of possible parallel universes at that quantum level.

**Input:** `5`

**Expected Output:** `120`

**Explanation:** 5! = 5 × 4 × 3 × 2 × 1 = 120

**Example:**
```python
# Your one-liner should calculate the factorial of the input number
```
""",
        "test_cases": [
            {
                "input": "5",
                "expected": "120",
                "description": "Should calculate factorial of 5"
            },
            {
                "input": "38",
                "expected": "523022617466601111760007224100074291200000000",
                "description": "Hidden test case with larger number"
            }
        ],
        "solution": "print(__import__(\"math\").factorial(int(input())))",
        "solvable_in_one_line": True
    },
    
    # Challenge 8: Reactor Rod Status
    {
        "id": 8,
        "title": "⚡ Reactor Rod Status",
        "difficulty": "Medium",
        "description": """
## Challenge 8: Reactor Rod Status

You're calibrating the ship's reactor core, which has numbered control rods from 1 to N. Every 3rd rod emits "Fizz" radiation, every 5th rod emits "Buzz" radiation, and every 15th rod emits both "FizzBuzz". You need to generate a diagnostic report showing each rod's status to ensure safe operation.

**Input:** `15`

**Expected Output:** `[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']`

**Explanation:** Classic FizzBuzz problem with space-themed context.

**Example:**
```python
# Your one-liner should implement FizzBuzz
```
""",
        "test_cases": [
            {
                "input": "15",
                "expected": "[1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']",
                "description": "Should implement FizzBuzz for 1 to 15"
            }
        ],
        "solution": "print(['FizzBuzz'if i%15==0 else'Fizz'if i%3==0 else'Buzz'if i%5==0 else i for i in range(1,int(input())+1)])",
        "solvable_in_one_line": True
    },
    
    # Challenge 9: Duplicate Signal Filter
    {
        "id": 9,
        "title": "🛰️ Duplicate Signal Filter",
        "difficulty": "Medium",
        "description": """
## Challenge 9: Duplicate Signal Filter

Your ship's scanner has detected multiple objects in space, but the sensor array is malfunctioning and reporting some objects multiple times. You need to remove duplicate readings while maintaining the order in which objects were first detected to create an accurate star map.

**Input:** `1,2,3,2,4,1,5`

**Expected Output:** `[1, 2, 3, 4, 5]`

**Explanation:** Remove duplicates while preserving order.

**Example:**
```python
# Your one-liner should remove duplicates while preserving order
```
""",
        "test_cases": [
            {
                "input": "1,2,3,2,4,1,5",
                "expected": "[1, 2, 3, 4, 5]",
                "description": "Should remove duplicates while preserving order"
            }
        ],
        "solution": "print(list(dict.fromkeys(map(int,input().split(',')))))",
        "solvable_in_one_line": True
    },
    
    # Challenge 10: Distress Signal Strength
    {
        "id": 10,
        "title": "🌙 Distress Signal Strength",
        "difficulty": "Medium",
        "description": """
## Challenge 10: Distress Signal Strength

Your ship receives a distress signal from a distant moon. The message is heavily corrupted by solar interference. Your communications officer explains that the signal strength can be determined by counting the vowels (a, e, i, o, u) in the transmission—more vowels mean a stronger, more urgent signal.

**Input:** `Hello World`

**Expected Output:** `3`

**Explanation:** The vowels found are: e, o, o

**Example:**
```python
# Your one-liner should count vowels in the input
```
""",
        "test_cases": [
            {
                "input": "Hello World",
                "expected": "3",
                "description": "Should count vowels (e, o, o)"
            }
        ],
        "solution": "print(sum(c.lower() in 'aeiou' for c in input()))",
        "solvable_in_one_line": True
    },
    
    # Challenge 11: The Glowing Tablets
    {
        "id": 11,
        "title": "💎 The Glowing Tablets",
        "difficulty": "Hard",
        "description": """
## Challenge 11: The Glowing Tablets

You return to the derelict alien spacecraft, but now you notice that only certain data tablets are glowing—these have the word "sum" marked on their backs. The ship's AI corrects you: only the coordinates from the glowing tablets should be added together. The others are decoys meant to throw off treasure hunters!

**Input:** `(1, ' '),(2, ' '),(3, ' '),(4, 'sum'),(5, ' '),(6, 'sum'),(7, ' '),(8, 'sum'),(9, 'sum'),(10, ' ')`

**Expected Output:** `27`

**Explanation:** Only tablets marked with 'sum' (4, 6, 8, and 9) should be added: 4 + 6 + 8 + 9 = 27

**Example:**
```python
# Your one-liner should extract and sum only numbers with 'sum' marker
```
""",
        "test_cases": [
            {
                "input": "(1, ' '),(2, ' '),(3, ' '),(4, 'sum'),(5, ' '),(6, 'sum'),(7, ' '),(8, 'sum'),(9, 'sum'),(10, ' ')",
                "expected": "27",
                "description": "Should sum only numbers marked with 'sum'"
            }
        ],
        "solution": "print(sum([int(x) for x in __import__('re').findall(r\"\\((\\w+), 'sum'\\)\",input())]))",
        "solvable_in_one_line": True
    },
    
    # Challenge 12: Prime Shield Frequencies
    {
        "id": 12,
        "title": "🛡️ Prime Shield Frequencies",
        "difficulty": "Hard",
        "description": """
## Challenge 12: Prime Shield Frequencies

Your ship's shields operate on prime-numbered frequency bands to avoid interference from cosmic radiation. The shield generator needs to identify all available prime frequencies up to a maximum value to establish optimal protection during solar flare season.

**Input:** `20`

**Expected Output:** `[2, 3, 5, 7, 11, 13, 17, 19]`

**Explanation:** Find all prime numbers from 2 to N.

**Example:**
```python
# Your one-liner should generate a list of prime numbers
```
""",
        "test_cases": [
            {
                "input": "20",
                "expected": "[2, 3, 5, 7, 11, 13, 17, 19]",
                "description": "Should return all primes up to 20"
            }
        ],
        "solution": "print([x for x in range(2,int(input())+1)if all(x%i!=0 for i in range(2,int(x**0.5)+1))])",
        "solvable_in_one_line": True
    },
    
    # Challenge 13: Planetary Classification System
    {
        "id": 13,
        "title": "🪐 Planetary Classification System",
        "difficulty": "Hard",
        "description": """
## Challenge 13: Planetary Classification System

You're decoding an encrypted alien message system where anagrams (words with the same letters rearranged) belong to the same conceptual group. The aliens use this to categorize star systems—all systems with rearranged letters share similar properties. Group the words to unlock their classification system.

**Input:** `listen,silent,hello,enlist`

**Expected Output:** `[['listen', 'silent', 'enlist'], ['hello']]`

**Explanation:** Group anagrams together.

**Example:**
```python
# Your one-liner should group anagrams
```
""",
        "test_cases": [
            {
                "input": "listen,silent,hello,enlist",
                "expected": "[['listen', 'silent', 'enlist'], ['hello']]",
                "description": "Should group anagrams together"
            }
        ],
        "solution": "print(list({k:[w for w in(l:=input().split(','))if sorted(w)==list(k)]for k in{tuple(sorted(w))for w in l}}.values()))",
        "solvable_in_one_line": True
    },
    
    # Challenge 14: Pirate-Proof Encryption
    {
        "id": 14,
        "title": "🔐 Pirate-Proof Encryption",
        "difficulty": "Hard",
        "description": """
## Challenge 14: Pirate-Proof Encryption

Your communications are being intercepted by space pirates! To send secure messages back to your home base, you implement a Caesar cipher with a shift of 3—a classic encryption technique where each letter is shifted 3 positions forward in the alphabet. Encrypt your message before transmission!

**Input:** `Hello World!`

**Expected Output:** `Khoor Zruog!`

**Explanation:** Shift each letter by 3 positions. Non-letters remain unchanged.

**Example:**
```python
# Your one-liner should implement Caesar cipher with shift 3
```
""",
        "test_cases": [
            {
                "input": "Hello World!",
                "expected": "Khoor Zruog!",
                "description": "Should encrypt using Caesar cipher with shift 3"
            }
        ],
        "solution": "print(''.join(chr((ord(c)-65+3)%26+65)if c.isupper()else chr((ord(c)-97+3)%26+97)if c.islower()else c for c in input()))",
        "solvable_in_one_line": True
    },
    
    # Challenge 15: Second Star to the Right
    {
        "id": 15,
        "title": "🌟 Second Star to the Right",
        "difficulty": "Hard",
        "description": """
## Challenge 15: Second Star to the Right

Your ship is approaching a cluster of planets for potential colonization. You need to identify the second-largest planet by mass—the largest is a gas giant unsuitable for landing, but the second-largest might be perfect. Find the second-highest value from the planetary mass readings.

**Input:** `10,5,20,15,20,8`

**Expected Output:** `15`

**Explanation:** After removing duplicates and sorting, the second-largest unique value is 15.

**Example:**
```python
# Your one-liner should find the second-largest unique value
```
""",
        "test_cases": [
            {
                "input": "10,5,20,15,20,8",
                "expected": "15",
                "description": "Should return second-largest unique value"
            }
        ],
        "solution": "print(sorted(set(map(int,input().split(','))))[-2])",
        "solvable_in_one_line": True
    },
]

# ============================================================================
# DON'T EDIT BELOW THIS LINE - This code updates app.py automatically
# ============================================================================

def update_app_py():
    """Update the CHALLENGES list in app.py with the new challenges"""
    import re
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the CHALLENGES = [ ... ] section
    # We'll look for the start and end of the CHALLENGES list
    pattern = r'(# Define challenges with increasing difficulty\s*\nCHALLENGES = \[)(.*?)(\n\]\s*\n# END OF CHALLENGES)'
    
    # If END OF CHALLENGES marker doesn't exist, we'll look for the next major section
    if 'END OF CHALLENGES' not in content:
        # Find where CHALLENGES starts and ends (before the next function or major section)
        start_match = re.search(r'# Define challenges.*?\nCHALLENGES = \[', content, re.DOTALL)
        if not start_match:
            print("Error: Could not find CHALLENGES definition in app.py")
            return False
        
        start_pos = start_match.end()
        
        # Find the end - look for the closing ] followed by blank lines and either a function def or @app.route
        end_match = re.search(r'\n\]\s*\n\s*\n(?:def |@app\.)', content[start_pos:])
        if not end_match:
            print("Error: Could not find end of CHALLENGES list in app.py")
            return False
        
        end_pos = start_pos + end_match.start()
        
        # Build the new challenges string
        challenges_str = "[\n"
        for challenge in CHALLENGES:
            challenges_str += f"    {challenge},\n"
        challenges_str += "]\n\n# END OF CHALLENGES\n\n"
        
        # Replace the content
        new_content = content[:start_match.end()] + challenges_str + content[end_pos + 2:]
        
    else:
        # We have the marker, use regex
        challenges_str = "\n"
        for challenge in CHALLENGES:
            challenges_str += f"    {challenge},\n"
        
        new_content = re.sub(pattern, r'\1' + challenges_str + r'\3', content, flags=re.DOTALL)
    
    # Write back to file
    with open('app.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Successfully updated app.py with your 15 challenges!")
    print("\nYour challenges have been installed. Restart the Flask app to see them.")
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("Challenge Setup Tool - Updating app.py with your challenges...")
    print("=" * 70)
    
    # Validate we have exactly 15 challenges
    if len(CHALLENGES) != 15:
        print(f"⚠️  Warning: You have {len(CHALLENGES)} challenges, but should have 15!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            exit(1)
    
    # Validate each challenge has required fields
    required_fields = ['id', 'title', 'difficulty', 'description', 'test_cases', 'solution']
    for i, challenge in enumerate(CHALLENGES, 1):
        for field in required_fields:
            if field not in challenge:
                print(f"❌ Error: Challenge {i} is missing required field: {field}")
                exit(1)
    
    print(f"\n✓ Validated {len(CHALLENGES)} challenges")
    print("\nUpdating app.py...")
    
    if update_app_py():
        print("\n" + "=" * 70)
        print("SUCCESS! Your challenges are now in the app.")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Review the changes in app.py if you want")
        print("2. Restart your Flask application")
        print("3. Your new challenges will be live!")
    else:
        print("\n❌ Failed to update app.py. Please check the file manually.")
        exit(1)
