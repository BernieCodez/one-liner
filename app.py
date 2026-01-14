from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO
import traceback
import signal
import contextlib
import json
import os

app = Flask(__name__)

# Directory for storing user code
SAVED_CODE_DIR = 'saved_code'
if not os.path.exists(SAVED_CODE_DIR):
    os.makedirs(SAVED_CODE_DIR)

# File for storing custom challenges
CUSTOM_CHALLENGES_FILE = os.path.join(SAVED_CODE_DIR, 'custom_challenges.json')

def load_custom_challenges():
    """Load custom challenges from file"""
    if os.path.exists(CUSTOM_CHALLENGES_FILE):
        try:
            with open(CUSTOM_CHALLENGES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_custom_challenges(challenges):
    """Save custom challenges to file"""
    with open(CUSTOM_CHALLENGES_FILE, 'w') as f:
        json.dump(challenges, f, indent=2)

# Define challenges with increasing difficulty
CHALLENGES = [
    {
        "id": 1,
        "title": "List Comprehension Basics",
        "difficulty": "Easy",
        "description": """
## Challenge 1: Square Numbers

Create a one-liner that returns a list of squares for numbers 1 through 5.

**Expected Output:** `[1, 4, 9, 16, 25]`

**Hint:** Use list comprehension with `range(1, 6)`

**Example:**
```python
# Your one-liner should create: [1, 4, 9, 16, 25]
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[1, 4, 9, 16, 25]",
                "description": "Should return squares of 1-5"
            }
        ],
        "solution": "print([x**2 for x in range(1, 6)])"
    },
    {
        "id": 2,
        "title": "String Manipulation",
        "difficulty": "Easy",
        "description": """
## Challenge 2: Reverse a String

Create a one-liner that reverses the string "Python".

**Expected Output:** `"nohtyP"`

**Hint:** Use string slicing with `[::-1]`

**Example:**
```python
# Your one-liner should reverse "Python" to "nohtyP"
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "nohtyP",
                "description": "Should reverse 'Python'"
            }
        ],
        "solution": "print(\"Python\"[::-1])"
    },
    {
        "id": 3,
        "title": "Filter Even Numbers",
        "difficulty": "Easy",
        "description": """
## Challenge 3: Filter Even Numbers

Create a one-liner that returns only even numbers from the list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].

**Expected Output:** `[2, 4, 6, 8, 10]`

**Hint:** Use list comprehension with an `if` condition

**Example:**
```python
# Your one-liner should filter: [2, 4, 6, 8, 10]
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[2, 4, 6, 8, 10]",
                "description": "Should return even numbers from 1-10"
            }
        ],
        "solution": "print([x for x in range(1, 11) if x % 2 == 0])"
    },
    {
        "id": 4,
        "title": "Dictionary Comprehension",
        "difficulty": "Medium",
        "description": """
## Challenge 4: Create a Dictionary

Create a one-liner that creates a dictionary mapping numbers 1-5 to their cubes.

**Expected Output:** `{1: 1, 2: 8, 3: 27, 4: 64, 5: 125}`

**Hint:** Use dictionary comprehension `{key: value for ...}`

**Example:**
```python
# Your one-liner should create: {1: 1, 2: 8, 3: 27, 4: 64, 5: 125}
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "{1: 1, 2: 8, 3: 27, 4: 64, 5: 125}",
                "description": "Should map numbers to their cubes"
            }
        ],
        "solution": "print({x: x**3 for x in range(1, 6)})"
    },
    {
        "id": 5,
        "title": "Lambda and Map",
        "difficulty": "Medium",
        "description": """
## Challenge 5: Double the Numbers

Create a one-liner using `map` and `lambda` to double all numbers in [1, 2, 3, 4, 5].

**Expected Output:** `[2, 4, 6, 8, 10]`

**Hint:** Combine `list()`, `map()`, and a `lambda` function

**Example:**
```python
# Your one-liner should use map and lambda to get: [2, 4, 6, 8, 10]
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[2, 4, 6, 8, 10]",
                "description": "Should double all numbers"
            }
        ],
        "solution": "print(list(map(lambda x: x * 2, [1, 2, 3, 4, 5])))"
    },
    {
        "id": 6,
        "title": "Flatten a List",
        "difficulty": "Medium",
        "description": """
## Challenge 6: Flatten Nested List

Create a one-liner that flattens the nested list [[1, 2], [3, 4], [5, 6]].

**Expected Output:** `[1, 2, 3, 4, 5, 6]`

**Hint:** Use list comprehension with nested loops

**Example:**
```python
# Your one-liner should flatten: [1, 2, 3, 4, 5, 6]
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[1, 2, 3, 4, 5, 6]",
                "description": "Should flatten nested list"
            }
        ],
        "solution": "print([item for sublist in [[1, 2], [3, 4], [5, 6]] for item in sublist])"
    },
    {
        "id": 7,
        "title": "Sum of Squares",
        "difficulty": "Medium",
        "description": """
## Challenge 7: Sum of Squares

Create a one-liner that calculates the sum of squares for numbers 1-10.

**Expected Output:** `385`

**Hint:** Use `sum()` with a generator expression or list comprehension

**Example:**
```python
# Your one-liner should calculate: 1² + 2² + ... + 10² = 385
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "385",
                "description": "Should return sum of squares 1-10"
            }
        ],
        "solution": "print(sum(x**2 for x in range(1, 11)))"
    },
    {
        "id": 8,
        "title": "Filter and Transform",
        "difficulty": "Hard",
        "description": """
## Challenge 8: Prime Numbers Squared

Create a one-liner that returns squares of prime numbers from 1 to 20.

**Expected Output:** `[4, 9, 25, 49, 121, 169, 289, 361]`

**Hint:** Combine list comprehension with a condition that checks for primes (a number is prime if it has no divisors except 1 and itself)

**Example:**
```python
# Your one-liner should find primes in 1-20 and square them
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[4, 9, 25, 49, 121, 169, 289, 361]",
                "description": "Should return squares of primes 2-19"
            }
        ],
        "solution": "print([x**2 for x in range(2, 21) if all(x % i != 0 for i in range(2, int(x**0.5) + 1))])"
    },
    {
        "id": 9,
        "title": "String Transformation",
        "difficulty": "Hard",
        "description": """
## Challenge 9: Vowel Capitalization

Create a one-liner that capitalizes only vowels in "hello world".

**Expected Output:** `"hEllO wOrld"`

**Hint:** Use join with a conditional expression in a generator

**Example:**
```python
# Your one-liner should transform: "hello world" -> "hEllO wOrld"
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "hEllO wOrld",
                "description": "Should capitalize only vowels"
            }
        ],
        "solution": "print(\"\".join(c.upper() if c in 'aeiou' else c for c in \"hello world\"))"
    },
    {
        "id": 10,
        "title": "Fibonacci Sequence",
        "difficulty": "Hard",
        "description": """
## Challenge 10: Fibonacci One-Liner

Create a one-liner that generates the first 10 Fibonacci numbers.

**Expected Output:** `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`

**Hint:** Use a lambda with reduce or a creative list comprehension approach

**Example:**
```python
# Your one-liner should generate: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
""",
        "test_cases": [
            {
                "input": None,
                "expected": "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]",
                "description": "Should return first 10 Fibonacci numbers"
            }
        ],
        "solution": "print([0, 1] + [(lambda f: f(f, 10, 2, [0, 1]))(lambda f, n, i, acc: acc if i >= n else f(f, n, i+1, acc + [acc[-1] + acc[-2]]))])"
    },
    {
        "id": 11,
        "title": "Sum Two Numbers",
        "difficulty": "Easy",
        "description": """
## Challenge 11: Sum Two Numbers from Input

Write a program that reads two space-separated integers from input and prints their sum.

**Input Format:** Two integers separated by a space (e.g., "5 3")

**Output Format:** The sum of the two numbers (e.g., "8")

**Example:**
```
Input: 5 3
Output: 8
```

**Hint:** Use `input()` to read the line, `split()` to separate values, and `int()` to convert strings to integers.

**Note:** Your output should match exactly - just print the number with no extra text.
""",
        "test_cases": [
            {
                "input": "5 3",
                "expected": "8",
                "description": "Sum of 5 and 3"
            },
            {
                "input": "10 20",
                "expected": "30",
                "description": "Sum of 10 and 20"
            },
            {
                "input": "-5 15",
                "expected": "10",
                "description": "Sum with negative number"
            }
        ],
        "solution": "a, b = map(int, input().split())\nprint(a + b)"
    },
    {
        "id": 12,
        "title": "Greeting with Name",
        "difficulty": "Easy",
        "description": """
## Challenge 12: Personalized Greeting

Write a program that reads a name from input and prints a greeting.

**Input Format:** A single line with a name (e.g., "Alice")

**Output Format:** "Hello, [name]!" (e.g., "Hello, Alice!")

**Example:**
```
Input: Alice
Output: Hello, Alice!
```

**Hint:** Use `input()` to read the name and f-strings or string concatenation for formatting.
""",
        "test_cases": [
            {
                "input": "Alice",
                "expected": "Hello, Alice!",
                "description": "Greeting for Alice"
            },
            {
                "input": "Bob",
                "expected": "Hello, Bob!",
                "description": "Greeting for Bob"
            },
            {
                "input": "Charlie",
                "expected": "Hello, Charlie!",
                "description": "Greeting for Charlie"
            }
        ],
        "solution": "name = input()\nprint(f'Hello, {name}!')"
    },
    {
        "id": 13,
        "title": "Count Words",
        "difficulty": "Medium",
        "description": """
## Challenge 13: Count Words in a Sentence

Write a program that reads a sentence and prints the number of words in it.

**Input Format:** A single line with a sentence (e.g., "The quick brown fox")

**Output Format:** The number of words (e.g., "4")

**Example:**
```
Input: The quick brown fox
Output: 4
```

**Hint:** Use `split()` to break the sentence into words and `len()` to count them.
""",
        "test_cases": [
            {
                "input": "The quick brown fox",
                "expected": "4",
                "description": "Four words"
            },
            {
                "input": "Hello",
                "expected": "1",
                "description": "Single word"
            },
            {
                "input": "Python is an amazing programming language",
                "expected": "6",
                "description": "Six words"
            }
        ],
        "solution": "sentence = input()\nprint(len(sentence.split()))"
    },
    {
        "id": 14,
        "title": "Temperature Converter",
        "difficulty": "Medium",
        "description": """
## Challenge 14: Celsius to Fahrenheit

Write a program that reads a temperature in Celsius and converts it to Fahrenheit.

**Formula:** F = (C × 9/5) + 32

**Input Format:** A number representing temperature in Celsius (e.g., "25")

**Output Format:** The temperature in Fahrenheit rounded to 1 decimal place (e.g., "77.0")

**Example:**
```
Input: 25
Output: 77.0
```

**Hint:** Use `float()` to convert input, apply the formula, and `round()` for precision.
""",
        "test_cases": [
            {
                "input": "25",
                "expected": "77.0",
                "description": "25°C to Fahrenheit"
            },
            {
                "input": "0",
                "expected": "32.0",
                "description": "0°C to Fahrenheit"
            },
            {
                "input": "100",
                "expected": "212.0",
                "description": "100°C to Fahrenheit"
            },
            {
                "input": "-40",
                "expected": "-40.0",
                "description": "-40°C to Fahrenheit"
            }
        ],
        "solution": "celsius = float(input())\nfahrenheit = round((celsius * 9/5) + 32, 1)\nprint(fahrenheit)"
    },
    {
        "id": 15,
        "title": "List Statistics",
        "difficulty": "Hard",
        "description": """
## Challenge 15: Calculate List Statistics

Write a program that reads a list of space-separated integers and prints their sum, average (rounded to 2 decimals), and maximum value on separate lines.

**Input Format:** Space-separated integers (e.g., "10 20 30 40 50")

**Output Format:** Three lines:
- Sum
- Average (2 decimal places)
- Maximum

**Example:**
```
Input: 10 20 30 40 50
Output:
150
30.00
50
```

**Hint:** Use `map(int, input().split())` to parse numbers, then use `sum()`, `len()`, and `max()`.
""",
        "test_cases": [
            {
                "input": "10 20 30 40 50",
                "expected": "150\n30.00\n50",
                "description": "Statistics for [10, 20, 30, 40, 50]"
            },
            {
                "input": "5 5 5 5",
                "expected": "20\n5.00\n5",
                "description": "All same numbers"
            },
            {
                "input": "100 1 50",
                "expected": "151\n50.33\n100",
                "description": "Three numbers with varying values"
            }
        ],
        "solution": "numbers = list(map(int, input().split()))\nprint(sum(numbers))\nprint(f'{sum(numbers)/len(numbers):.2f}')\nprint(max(numbers))"
    }
]

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creator')
def creator():
    return render_template('creator.html')

@app.route('/api/challenges')
def get_challenges():
    """Return list of challenges without solutions"""
    # Combine built-in challenges with custom ones
    custom = load_custom_challenges()
    all_challenges = CHALLENGES + custom
    
    challenges_list = [
        {
            "id": c["id"],
            "title": c["title"],
            "difficulty": c["difficulty"]
        }
        for c in all_challenges
    ]
    return jsonify(challenges_list)

@app.route('/api/challenge/<int:challenge_id>')
def get_challenge(challenge_id):
    """Return specific challenge details without solution"""
    # Check both built-in and custom challenges
    custom = load_custom_challenges()
    all_challenges = CHALLENGES + custom
    
    challenge = next((c for c in all_challenges if c["id"] == challenge_id), None)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    
    # Return challenge without solution
    return jsonify({
        "id": challenge["id"],
        "title": challenge["title"],
        "difficulty": challenge["difficulty"],
        "description": challenge["description"],
        "test_cases": [
            {
                "description": tc["description"],
                "input": tc.get("input"),
                "expected": tc["expected"]
            }
            for tc in challenge["test_cases"]
        ]
    })

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute user's code and check against test cases"""
    data = request.get_json()
    code = data.get('code', '').strip()
    challenge_id = data.get('challenge_id')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # Check both built-in and custom challenges
    custom = load_custom_challenges()
    all_challenges = CHALLENGES + custom
    
    challenge = next((c for c in all_challenges if c["id"] == challenge_id), None)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    
    results = []
    all_passed = True
    
    for test_case in challenge["test_cases"]:
        try:
            # Capture output and setup input
            old_stdout = sys.stdout
            old_stdin = sys.stdin
            sys.stdout = StringIO()
            
            # Setup stdin with test input
            test_input = test_case.get("input", "")
            if test_input is not None:
                sys.stdin = StringIO(str(test_input) if test_input else "")
            
            # Execute code with full built-ins support
            namespace = {'__builtins__': __builtins__, '__name__': '__main__'}
            
            # Set timeout (Note: SIGALRM only works on Unix-like systems)
            try:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(5)  # 5 second timeout
            except (AttributeError, ValueError):
                pass  # Windows doesn't support SIGALRM - timeout not enforced
            
            # Execute the code using exec() instead of eval() to support multi-line scripts
            exec(code, namespace)
            
            # Cancel timeout
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
            
            # Get the output
            output = sys.stdout.getvalue().strip()
            
            # Restore stdout and stdin
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            
            # Check result - compare stdout output with expected
            expected = str(test_case["expected"]).strip()
            passed = output == expected
            
            if not passed:
                all_passed = False
            
            results.append({
                "description": test_case["description"],
                "input": test_input if test_input else "(no input)",
                "expected": expected,
                "actual": output,
                "passed": passed
            })
            
        except TimeoutError:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            all_passed = False
            results.append({
                "description": test_case["description"],
                "input": test_input if test_input else "(no input)",
                "error": "Execution timed out (max 5 seconds)",
                "passed": False
            })
        except Exception as e:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            all_passed = False
            error_msg = str(e)
            if not error_msg:
                error_msg = type(e).__name__
            results.append({
                "description": test_case["description"],
                "input": test_input if test_input else "(no input)",
                "error": error_msg,
                "traceback": traceback.format_exc(),
                "passed": False
            })
    
    return jsonify({
        "passed": all_passed,
        "results": results
    })

@app.route('/api/save-code', methods=['POST'])
def save_code():
    """Save code for a specific challenge"""
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    code = data.get('code', '')
    
    if not challenge_id:
        return jsonify({"error": "No challenge ID provided"}), 400
    
    # Save to file (server-side storage)
    try:
        filepath = os.path.join(SAVED_CODE_DIR, f'challenge_{challenge_id}.py')
        with open(filepath, 'w') as f:
            f.write(code)
        return jsonify({"success": True, "message": "Code saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/load-code/<int:challenge_id>')
def load_code(challenge_id):
    """Load saved code for a specific challenge"""
    try:
        filepath = os.path.join(SAVED_CODE_DIR, f'challenge_{challenge_id}.py')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                code = f.read()
            return jsonify({"code": code})
        else:
            return jsonify({"code": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save-settings', methods=['POST'])
def save_settings():
    """Save editor settings"""
    data = request.get_json()
    try:
        filepath = os.path.join(SAVED_CODE_DIR, 'settings.json')
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return jsonify({"success": True, "message": "Settings saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/load-settings')
def load_settings():
    """Load editor settings"""
    try:
        filepath = os.path.join(SAVED_CODE_DIR, 'settings.json')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                settings = json.load(f)
            return jsonify(settings)
        else:
            return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/challenges/create', methods=['POST'])
def create_challenge():
    """Create a new custom challenge"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'difficulty', 'description', 'solution', 'test_cases']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Load existing challenges
        custom_challenges = load_custom_challenges()
        
        # Generate new ID (start from 1000 for custom challenges to avoid conflicts)
        if custom_challenges:
            new_id = max(c['id'] for c in custom_challenges) + 1
        else:
            new_id = 1000
        
        # Create new challenge
        new_challenge = {
            "id": new_id,
            "title": data['title'],
            "difficulty": data['difficulty'],
            "description": data['description'],
            "test_cases": data['test_cases'],
            "solution": data['solution'],
            "custom": True
        }
        
        # Add to list and save
        custom_challenges.append(new_challenge)
        save_custom_challenges(custom_challenges)
        
        return jsonify({"success": True, "challenge": new_challenge, "message": "Challenge created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/challenges/custom')
def get_custom_challenges():
    """Get all custom challenges"""
    try:
        custom_challenges = load_custom_challenges()
        return jsonify(custom_challenges)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/challenges/custom/<int:challenge_id>', methods=['GET'])
def get_single_custom_challenge(challenge_id):
    """Get a single custom challenge"""
    try:
        custom_challenges = load_custom_challenges()
        challenge = next((c for c in custom_challenges if c['id'] == challenge_id), None)
        
        if not challenge:
            return jsonify({"error": "Challenge not found"}), 404
        
        return jsonify(challenge)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/challenges/custom/<int:challenge_id>', methods=['PUT'])
def update_challenge(challenge_id):
    """Update an existing custom challenge"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'difficulty', 'description', 'test_cases']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Load existing challenges
        custom_challenges = load_custom_challenges()
        
        # Find challenge to update
        challenge_index = next((i for i, c in enumerate(custom_challenges) if c['id'] == challenge_id), None)
        
        if challenge_index is None:
            return jsonify({"error": "Challenge not found"}), 404
        
        # Update challenge
        custom_challenges[challenge_index] = {
            "id": challenge_id,
            "title": data['title'],
            "difficulty": data['difficulty'],
            "description": data['description'],
            "test_cases": data['test_cases'],
            "solution": data.get('solution', ''),
            "custom": True
        }
        
        # Save updated list
        save_custom_challenges(custom_challenges)
        
        return jsonify({"success": True, "challenge": custom_challenges[challenge_index], "message": "Challenge updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/challenges/custom/<int:challenge_id>', methods=['DELETE'])
def delete_challenge(challenge_id):
    """Delete a custom challenge"""
    try:
        custom_challenges = load_custom_challenges()
        
        # Filter out the challenge to delete
        updated_challenges = [c for c in custom_challenges if c['id'] != challenge_id]
        
        if len(updated_challenges) == len(custom_challenges):
            return jsonify({"error": "Challenge not found"}), 404
        
        save_custom_challenges(updated_challenges)
        return jsonify({"success": True, "message": "Challenge deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)