import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

DB_PATH = "chatmate.db"

# ===== Create Tables =====
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Logins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# ===== Validate Email =====
def validate_email(email):
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    return bool(pattern.match(email))

# ===== Validate Password =====
def validate_password(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(pattern.match(password))

# ===== Signup User =====
def signup_user(username, email, password):
    if not validate_email(email):
        return False, "Invalid email format", None
    if not validate_password(password):
        return False, "Password must be 8+ chars with upper, lower, digit, special char", None
    
    hashed_pw = generate_password_hash(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_pw)
        )
        conn.commit()
        user_id = cursor.lastrowid  # <-- get new user ID
        conn.close()
        user_data = {"id": user_id, "username": username, "email": email}
        return True, "Signup successful", user_data
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists", None

# ===== Login User =====
def login_user(username_or_email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, password FROM users WHERE username=? OR email=?", 
        (username_or_email, username_or_email)
    )
    result = cursor.fetchone()

    if result:
        user_id, username, email, stored_password = result
        if check_password_hash(stored_password, password):
            # Record successful login
            cursor.execute(
                "INSERT INTO logins (username, success) VALUES (?, ?)",
                (username, 1)
            )
            conn.commit()
            conn.close()
            user_data = {"id": user_id, "username": username, "email": email}
            return True, "Login successful", user_data
        else:
            # Record failed login
            cursor.execute(
                "INSERT INTO logins (username, success) VALUES (?, ?)",
                (username, 0)
            )
            conn.commit()
            conn.close()
            return False, "Incorrect password", None
    else:
        conn.close()
        return False, "User not found", None  

# ===== Fetch Login History =====
def get_login_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, timestamp, success
        FROM logins
        ORDER BY timestamp DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    return records

# ===== Initialize Tables =====
if __name__ == "__main__":
    create_tables()
    print("Users and Logins tables ready.")
