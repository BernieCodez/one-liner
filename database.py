import sqlite3
import hashlib
import json
from datetime import datetime

DATABASE = 'users.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User progress table - tracks solved challenges
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            solution TEXT NOT NULL,
            is_custom BOOLEAN DEFAULT 0,
            solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, challenge_id, is_custom)
        )
    ''')
    
    # User created challenges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Forum posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Forum replies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forum_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES forum_posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Wiki pages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wiki_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_pw = hash_password(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      (username, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', 
                  (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, {'id': user['id'], 'username': user['username']}
    return False, "Invalid username or password"

def save_user_solution(user_id, challenge_id, solution, is_custom=False):
    """Save or update user's solution for a challenge"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_progress (user_id, challenge_id, solution, is_custom)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, challenge_id, is_custom) 
            DO UPDATE SET solution = ?, solved_at = CURRENT_TIMESTAMP
        ''', (user_id, challenge_id, solution, is_custom, solution))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_user_progress(user_id):
    """Get all solved challenges for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT challenge_id, solution, is_custom, solved_at 
        FROM user_progress 
        WHERE user_id = ?
        ORDER BY solved_at DESC
    ''', (user_id,))
    progress = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in progress]

def get_user_solution(user_id, challenge_id, is_custom=False):
    """Get user's solution for a specific challenge"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT solution 
        FROM user_progress 
        WHERE user_id = ? AND challenge_id = ? AND is_custom = ?
    ''', (user_id, challenge_id, is_custom))
    result = cursor.fetchone()
    conn.close()
    
    return result['solution'] if result else None

def save_user_challenge(user_id, challenge_data):
    """Save a user-created challenge"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_challenges (user_id, challenge_data)
            VALUES (?, ?)
        ''', (user_id, json.dumps(challenge_data)))
        conn.commit()
        challenge_id = cursor.lastrowid
        conn.close()
        return True, challenge_id
    except Exception as e:
        return False, str(e)

def get_user_challenges(user_id):
    """Get all challenges created by a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, challenge_data, created_at 
        FROM user_challenges 
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    challenges = cursor.fetchall()
    conn.close()
    
    result = []
    for row in challenges:
        data = json.loads(row['challenge_data'])
        data['db_id'] = row['id']
        data['created_at'] = row['created_at']
        result.append(data)
    
    return result

def get_user_stats(user_id):
    """Get statistics for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count solved challenges
    cursor.execute('SELECT COUNT(*) as count FROM user_progress WHERE user_id = ? AND is_custom = 0', (user_id,))
    solved_count = cursor.fetchone()['count']
    
    # Count created challenges
    cursor.execute('SELECT COUNT(*) as count FROM user_challenges WHERE user_id = ?', (user_id,))
    created_count = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        'solved_challenges': solved_count,
        'created_challenges': created_count
    }

# Forum functions
def create_forum_post(user_id, title, content):
    """Create a new forum post"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO forum_posts (user_id, title, content)
            VALUES (?, ?, ?)
        ''', (user_id, title, content))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return True, post_id
    except Exception as e:
        return False, str(e)

def get_forum_posts(limit=50, offset=0):
    """Get all forum posts with user information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            fp.id, fp.title, fp.content, fp.created_at, fp.updated_at,
            u.username,
            (SELECT COUNT(*) FROM forum_replies WHERE post_id = fp.id) as reply_count
        FROM forum_posts fp
        JOIN users u ON fp.user_id = u.id
        ORDER BY fp.updated_at DESC
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    posts = cursor.fetchall()
    conn.close()
    return [dict(row) for row in posts]

def get_forum_post(post_id):
    """Get a single forum post with replies"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get post
    cursor.execute('''
        SELECT 
            fp.id, fp.title, fp.content, fp.created_at, fp.updated_at,
            u.username, fp.user_id
        FROM forum_posts fp
        JOIN users u ON fp.user_id = u.id
        WHERE fp.id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    
    if not post:
        conn.close()
        return None
    
    # Get replies
    cursor.execute('''
        SELECT 
            fr.id, fr.content, fr.created_at,
            u.username, fr.user_id
        FROM forum_replies fr
        JOIN users u ON fr.user_id = u.id
        WHERE fr.post_id = ?
        ORDER BY fr.created_at ASC
    ''', (post_id,))
    replies = cursor.fetchall()
    conn.close()
    
    result = dict(post)
    result['replies'] = [dict(row) for row in replies]
    return result

def create_forum_reply(post_id, user_id, content):
    """Create a reply to a forum post"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO forum_replies (post_id, user_id, content)
            VALUES (?, ?, ?)
        ''', (post_id, user_id, content))
        
        # Update post's updated_at timestamp
        cursor.execute('''
            UPDATE forum_posts SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (post_id,))
        
        conn.commit()
        reply_id = cursor.lastrowid
        conn.close()
        return True, reply_id
    except Exception as e:
        return False, str(e)

# Wiki functions
def create_wiki_page(slug, title, content):
    """Create a new wiki page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO wiki_pages (slug, title, content)
            VALUES (?, ?, ?)
        ''', (slug, title, content))
        conn.commit()
        page_id = cursor.lastrowid
        conn.close()
        return True, page_id
    except sqlite3.IntegrityError:
        return False, "A page with this slug already exists"
    except Exception as e:
        return False, str(e)

def update_wiki_page(slug, title, content):
    """Update an existing wiki page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE wiki_pages 
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE slug = ?
        ''', (title, content, slug))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_wiki_page(slug):
    """Get a wiki page by slug"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, slug, title, content, created_at, updated_at
        FROM wiki_pages
        WHERE slug = ?
    ''', (slug,))
    page = cursor.fetchone()
    conn.close()
    return dict(page) if page else None

def get_all_wiki_pages():
    """Get all wiki pages"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, slug, title, created_at, updated_at
        FROM wiki_pages
        ORDER BY title ASC
    ''')
    pages = cursor.fetchall()
    conn.close()
    return [dict(row) for row in pages]

def delete_wiki_page(slug):
    """Delete a wiki page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM wiki_pages WHERE slug = ?', (slug,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

# Initialize database on import
init_db()
