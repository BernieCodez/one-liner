from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO
import traceback
import signal
import contextlib

app = Flask(__name__)

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
                "expected": [1, 4, 9, 16, 25],
                "description": "Should return squares of 1-5"
            }
        ],
        "solution": "[x**2 for x in range(1, 6)]"
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
        "solution": "\"Python\"[::-1]"
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
                "expected": [2, 4, 6, 8, 10],
                "description": "Should return even numbers from 1-10"
            }
        ],
        "solution": "[x for x in range(1, 11) if x % 2 == 0]"
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
                "expected": {1: 1, 2: 8, 3: 27, 4: 64, 5: 125},
                "description": "Should map numbers to their cubes"
            }
        ],
        "solution": "{x: x**3 for x in range(1, 6)}"
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
                "expected": [2, 4, 6, 8, 10],
                "description": "Should double all numbers"
            }
        ],
        "solution": "list(map(lambda x: x * 2, [1, 2, 3, 4, 5]))"
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
                "expected": [1, 2, 3, 4, 5, 6],
                "description": "Should flatten nested list"
            }
        ],
        "solution": "[item for sublist in [[1, 2], [3, 4], [5, 6]] for item in sublist]"
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
                "expected": 385,
                "description": "Should return sum of squares 1-10"
            }
        ],
        "solution": "sum(x**2 for x in range(1, 11))"
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
                "expected": [4, 9, 25, 49, 121, 169, 289, 361],
                "description": "Should return squares of primes 2-19"
            }
        ],
        "solution": "[x**2 for x in range(2, 21) if all(x % i != 0 for i in range(2, int(x**0.5) + 1))]"
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
        "solution": "\"\".join(c.upper() if c in 'aeiou' else c for c in \"hello world\")"
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
                "expected": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
                "description": "Should return first 10 Fibonacci numbers"
            }
        ],
        "solution": "(lambda n: [0, 1] + [sum((fib := [0, 1] + [0]*(n-2))[i-2:i]) or fib.__setitem__(i, sum(fib[i-2:i])) or fib[i] for i in range(2, n)])[-1][:n] if n > 2 else [0, 1][:n])(10) if False else [0, 1] + [(lambda f: f(f, 10, 2, [0, 1]))(lambda f, n, i, acc: acc if i >= n else f(f, n, i+1, acc + [acc[-1] + acc[-2]]))]"
    }
]

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/challenges')
def get_challenges():
    """Return list of challenges without solutions"""
    challenges_list = [
        {
            "id": c["id"],
            "title": c["title"],
            "difficulty": c["difficulty"]
        }
        for c in CHALLENGES
    ]
    return jsonify(challenges_list)

@app.route('/api/challenge/<int:challenge_id>')
def get_challenge(challenge_id):
    """Return specific challenge details without solution"""
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
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
    
    # Check if code is a single line
    if '\n' in code.strip():
        return jsonify({
            "error": "Code must be a single line!",
            "passed": False,
            "results": []
        })
    
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    
    results = []
    all_passed = True
    
    for test_case in challenge["test_cases"]:
        try:
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Execute code in a restricted namespace
            namespace = {
                '__builtins__': __builtins__,
            }
            
            # Set timeout (not available on all systems, will skip if not)
            try:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(2)  # 2 second timeout
            except (AttributeError, ValueError):
                pass  # Windows doesn't support SIGALRM
            
            result = eval(code, namespace)
            
            # Cancel timeout
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
            
            # Restore stdout
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check result
            expected = test_case["expected"]
            passed = result == expected
            
            if not passed:
                all_passed = False
            
            results.append({
                "description": test_case["description"],
                "expected": expected,
                "actual": result,
                "passed": passed
            })
            
        except TimeoutError:
            sys.stdout = old_stdout
            all_passed = False
            results.append({
                "description": test_case["description"],
                "error": "Execution timed out (max 2 seconds)",
                "passed": False
            })
        except Exception as e:
            sys.stdout = old_stdout
            all_passed = False
            results.append({
                "description": test_case["description"],
                "error": str(e),
                "traceback": traceback.format_exc(),
                "passed": False
            })
    
    return jsonify({
        "passed": all_passed,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
