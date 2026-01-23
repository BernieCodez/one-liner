from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
from io import StringIO
import traceback
import signal
import contextlib
import json
import os
import secrets
from database import (
    create_user, verify_user, 
    create_forum_post, get_forum_posts, get_forum_post, create_forum_reply,
    create_wiki_page, update_wiki_page, get_wiki_page, get_all_wiki_pages, delete_wiki_page,
    init_db, save_user_solution, get_user_progress, get_user_solution
)

app = Flask(__name__)

# Use persistent secret key
SECRET_KEY_FILE = 'secret.key'
if os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, 'r') as f:
        app.secret_key = f.read()
else:
    app.secret_key = secrets.token_hex(32)
    with open(SECRET_KEY_FILE, 'w') as f:
        f.write(app.secret_key)

# Initialize database
init_db()

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
        "solution": "print(\"Hello World!\")"
    },
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
        "solution": "print(input()[::-1])"
    },
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
        "solution": "print(list(range(1, int(input())+1, 2)))"
    },
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
        "solution": "print([int(x) for x in input().split()][int(input())-1])"
    },
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
        "solution": "print(sum([int(x) for x in input().split(',')]))"
    },
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
        "solution": "print((s:=input().replace(' ','').lower())==s[::-1])"
    },
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
        "solution": "print(__import__(\"math\").factorial(int(input())))"
    },
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
        "solution": "print(['FizzBuzz'if i%15==0 else'Fizz'if i%3==0 else'Buzz'if i%5==0 else i for i in range(1,int(input())+1)])"
    },
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
        "solution": "print(list(dict.fromkeys(map(int,input().split(',')))))"
    },
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
        "solution": "print(sum(c.lower() in 'aeiou' for c in input()))"
    },
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
        "solution": "print(sum([int(x) for x in __import__('re').findall(r\"\\((\\w+), 'sum'\\)\",input())]))"
    },
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
        "solution": "print([x for x in range(2,int(input())+1)if all(x%i!=0 for i in range(2,int(x**0.5)+1))])"
    },
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
        "solution": "print(list({k:[w for w in(l:=input().split(','))if sorted(w)==list(k)]for k in{tuple(sorted(w))for w in l}}.values()))"
    },
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
        "solution": "print(''.join(chr((ord(c)-65+3)%26+65)if c.isupper()else chr((ord(c)-97+3)%26+97)if c.islower()else c for c in input()))"
    },
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
        "solution": "print(sorted(set(map(int,input().split(','))))[-2])"
    }
]
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")

@app.route('/')
def index():
    return render_template('home.html', user=session.get('user'))

@app.route('/challenges')
def challenges():
    user = session.get('user')
    return render_template('index.html', user=user, username=user.get('username') if user else 'Guest')

@app.route('/test')
def test_page():
    user = session.get('user')
    return render_template('freeplay.html', user=user, username=user.get('username') if user else 'Guest')

@app.route('/login')
def login_page():
    return render_template('login.html')

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    success, result = create_user(username, password)
    if success:
        return jsonify({"success": True, "message": "User created successfully"}), 201
    else:
        return jsonify({"error": result}), 400

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    success, result = create_user(username, password)
    if success:
        user_data = {'id': result, 'username': username}
        session['user'] = user_data
        return jsonify({"success": True, "user": user_data}), 201
    else:
        return jsonify({"error": result}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    success, result = verify_user(username, password)
    if success:
        session['user'] = result
        return jsonify({"success": True, "user": result})
    else:
        return jsonify({"error": result}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True})

@app.route('/api/auth/me')
def get_current_user():
    user = session.get('user')
    if user:
        return jsonify({"user": user})
    return jsonify({"user": None})

@app.route('/api/user/progress')
def get_user_progress_api():
    """Get user's progress on all challenges"""
    user = session.get('user')
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = user.get('id')
    if not user_id:
        return jsonify({"error": "Invalid user session"}), 400
    
    progress = get_user_progress(user_id)
    return jsonify({"progress": progress})

# Wiki routes
@app.route('/wiki')
def wiki():
    return render_template('wiki.html', user=session.get('user'))

@app.route('/api/wiki/pages')
def get_wiki_pages():
    pages = get_all_wiki_pages()
    return jsonify(pages)

@app.route('/api/wiki/page/<slug>')
def api_get_wiki_page(slug):
    page = get_wiki_page(slug)
    if page:
        return jsonify(page)
    return jsonify({"error": "Page not found"}), 404

@app.route('/api/wiki/page', methods=['POST'])
def api_create_wiki_page():
    data = request.json
    slug = data.get('slug')
    title = data.get('title')
    content = data.get('content')
    
    if not all([slug, title, content]):
        return jsonify({"error": "Slug, title, and content required"}), 400
    
    success, result = create_wiki_page(slug, title, content)
    if success:
        return jsonify({"success": True, "page_id": result}), 201
    else:
        return jsonify({"error": result}), 400

@app.route('/api/wiki/page/<slug>', methods=['PUT'])
def api_update_wiki_page(slug):
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    if not all([title, content]):
        return jsonify({"error": "Title and content required"}), 400
    
    success = update_wiki_page(slug, title, content)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to update page"}), 500

@app.route('/api/wiki/page/<slug>', methods=['DELETE'])
def api_delete_wiki_page(slug):
    success = delete_wiki_page(slug)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to delete page"}), 500

# Forum routes
@app.route('/forums')
def forums():
    return render_template('forums.html', user=session.get('user'))

@app.route('/forums/post/<int:post_id>')
def forum_post_page(post_id):
    """Render individual forum post page"""
    post = get_forum_post(post_id)
    if not post:
        return "Post not found", 404
    
    # Format dates for display
    from datetime import datetime
    post['created_at'] = datetime.strptime(post['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')
    for reply in post.get('replies', []):
        reply['created_at'] = datetime.strptime(reply['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')
    
    return render_template('forum_post.html', post=post, user=session.get('user'))

@app.route('/api/forums/posts')
def api_get_forum_posts():
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    posts = get_forum_posts(limit, offset)
    return jsonify(posts)

@app.route('/api/forums/post/<int:post_id>')
def api_get_forum_post(post_id):
    post = get_forum_post(post_id)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route('/api/forums/post', methods=['POST'])
def api_create_forum_post():
    user = session.get('user')
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    if not all([title, content]):
        return jsonify({"error": "Title and content required"}), 400
    
    success, result = create_forum_post(user['id'], title, content)
    if success:
        return jsonify({"success": True, "post_id": result}), 201
    else:
        return jsonify({"error": result}), 500

@app.route('/api/forums/post/<int:post_id>/reply', methods=['POST'])
def api_create_forum_reply(post_id):
    user = session.get('user')
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({"error": "Content required"}), 400
    
    success, result = create_forum_reply(post_id, user['id'], content)
    if success:
        return jsonify({"success": True, "reply_id": result}), 201
    else:
        return jsonify({"error": result}), 500

@app.route('/creator')
def creator_list():
    """Show list of user's custom challenges"""
    return render_template('creator_list.html')

@app.route('/creator/new')
def creator_new():
    """Create a new custom challenge"""
    return render_template('creator_edit.html')

@app.route('/creator/edit/<int:challenge_id>')
def creator_edit(challenge_id):
    """Edit an existing custom challenge"""
    return render_template('creator_edit.html', challenge_id=challenge_id)

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
    custom_test_cases = data.get('test_cases')  # For custom challenges being created
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # If custom test cases are provided (during creation/editing), use them
    if custom_test_cases:
        test_cases = custom_test_cases
    else:
        # Check both built-in and custom challenges
        custom = load_custom_challenges()
        all_challenges = CHALLENGES + custom
        
        challenge = next((c for c in all_challenges if c["id"] == challenge_id), None)
        if not challenge:
            return jsonify({"error": "Challenge not found"}), 404
        
        test_cases = challenge["test_cases"]
    
    results = []
    all_passed = True
    
    # Check if solution is a one-liner (no semicolons, newlines except at end)
    code_stripped = code.strip()
    is_one_liner = '\n' not in code_stripped and ';' not in code_stripped
    
    for test_case in test_cases:
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
    
    # Save progress to database if all tests passed and user is logged in
    if all_passed and challenge_id and not custom_test_cases:
        user = session.get('user')
        if user:
            user_id = user.get('id')
            if user_id:
                # Check if this is a custom challenge
                is_custom = challenge_id not in [c['id'] for c in CHALLENGES]
                save_user_solution(user_id, challenge_id, code, is_custom)
    
    return jsonify({
        "passed": all_passed,
        "results": results,
        "is_one_liner": is_one_liner
    })

@app.route('/api/execute-general', methods=['POST'])
def execute_general():
    """Execute user's code in general mode (free play) with custom input"""
    import time
    data = request.get_json()
    code = data.get('code', '').strip()
    user_input = data.get('input', '')
    
    if not code:
        return jsonify({"success": False, "error": "No code provided"}), 400
    
    try:
        # Capture output and setup input
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = StringIO()
        
        # Setup stdin with user's custom input
        sys.stdin = StringIO(user_input)
        
        # Execute code with full built-ins support
        namespace = {'__builtins__': __builtins__, '__name__': '__main__'}
        
        # Set timeout
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)  # 10 second timeout for free play
        except (AttributeError, ValueError):
            pass  # Windows doesn't support SIGALRM
        
        # Execute the code and track time
        start_time = time.time()
        exec(code, namespace)
        execution_time = time.time() - start_time
        
        # Cancel timeout
        try:
            signal.alarm(0)
        except (AttributeError, ValueError):
            pass
        
        # Get the output
        output = sys.stdout.getvalue()
        
        # Restore stdout and stdin
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        
        return jsonify({
            "success": True,
            "output": output,
            "execution_time": execution_time
        })
        
    except TimeoutError:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        return jsonify({
            "success": False,
            "error": "Execution timed out (max 10 seconds)",
            "traceback": ""
        })
    except Exception as e:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        error_msg = str(e) if str(e) else type(e).__name__
        return jsonify({
            "success": False,
            "error": error_msg,
            "traceback": traceback.format_exc()
        })

@app.route('/api/save-code', methods=['POST'])
def save_code():
    """Save code for a specific challenge"""
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    code = data.get('code', '')
    is_custom = data.get('is_custom', False)
    
    if not challenge_id:
        return jsonify({"error": "No challenge ID provided"}), 400
    
    # Save to file (server-side storage)
    try:
        filepath = os.path.join(SAVED_CODE_DIR, f'challenge_{challenge_id}.py')
        with open(filepath, 'w') as f:
            f.write(code)
        
        # Also save to database if user is logged in
        user = session.get('user')
        if user and code.strip():  # Only save non-empty code
            user_id = user.get('id')
            if user_id:
                save_user_solution(user_id, challenge_id, code, is_custom)
        
        return jsonify({"success": True, "message": "Code saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/load-code/<int:challenge_id>')
def load_code(challenge_id):
    """Load saved code for a specific challenge"""
    try:
        # First check database if user is logged in
        user = session.get('user')
        if user:
            user_id = user.get('id')
            if user_id:
                # Check if it's a custom challenge
                custom = load_custom_challenges()
                is_custom = challenge_id not in [c['id'] for c in CHALLENGES]
                
                db_solution = get_user_solution(user_id, challenge_id, is_custom)
                if db_solution:
                    return jsonify({"code": db_solution})
        
        # Fallback to file-based storage
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
        
        # Check if solution is a one-liner
        solution_stripped = data['solution'].strip()
        is_one_liner = '\n' not in solution_stripped and ';' not in solution_stripped
        
        # Create new challenge
        new_challenge = {
            "id": new_id,
            "title": data['title'],
            "difficulty": data['difficulty'],
            "description": data['description'],
            "test_cases": data['test_cases'],
            "solution": data['solution'],
            "custom": True,
            "solvable_in_one_line": is_one_liner
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
        
        # Check if solution is a one-liner
        solution = data.get('solution', '')
        solution_stripped = solution.strip()
        is_one_liner = '\n' not in solution_stripped and ';' not in solution_stripped
        
        # Update challenge
        custom_challenges[challenge_index] = {
            "id": challenge_id,
            "title": data['title'],
            "difficulty": data['difficulty'],
            "description": data['description'],
            "test_cases": data['test_cases'],
            "solution": solution,
            "custom": True,
            "solvable_in_one_line": is_one_liner
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