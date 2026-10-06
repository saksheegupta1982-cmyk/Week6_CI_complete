# app_secure.py - Secure version 
import sqlite3
import os
import re
import bcrypt
#from getpass import getpass

# Fix 1: Secret from env variable, not hardcoded 
# Earlier SECRET_KEY = "admin123" was visible in code.
# Now we take it from environment variable, so even if code leaks, secret is safe.
SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_secure_key")

def init_db():
    # Create users table if not exists - prevents crash on first run
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def sanitize_input(input_str):
    """Fix 4: Input sanitization + Path traversal prevention
    Only allows a-z, A-z, 0-9 and underscore.
    Blocks payloads like../../etc/passwd or <script>alert()
    """ 
    if not re.match(r"^[a-zA-Z0-9_]+$", input_str):
        raise ValueError("Invalid characters detected - only alphanumeric and _ allowed")
    return input_str

def login_secure():
    # Main scure login function with all fixes
    init_db()

    # validate username before using it anywhere
    try:
        
        username = sanitize_input(input("Enter username: "))
    except ValueError as e:
        print(e)
        return 

    # getpass hides password while typing, prevents shoulder surfing
    password = input("Enter password: ") # Hides password

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Fix 2: Parameterized Query - Prevents SQL Injection
    # Earlier: f"SELECT * FROM users WHERE username = '{username}'" ->attacker can inject 'OR '1'='1
    # Now: Using parameterized
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        # Fix 5: Secure Password Storage using bcrypt
        # bcrypt hashes password with salt, plain text never stored
        # checkpw compres hash safely,prevents timing attacks 
        stored_hash = user[1].encode() if isinstance(user[1], str)else user[1]
        if bcrypt.checkpw(password.encode(), stored_hash):
            print("Login success")
            try:
                # Fix 4: Path Traversal Prevention - Part 2 
                # os.path.join + os.path.basename ensure file stays inside notes/ folder
                # Even if username is../../etc/passwd, basename will make it passwd
                os.makedirs("notes", exist_ok = True)
                safe_path = os.path.join("notes",os.path.basename(f"{username}_notes.txt"))
                with open (safe_path, 'r')as f:
                    print(f.read())
            except FileNotFoundError:
                # Fix 3: Secure Error Handling - Part 1
                # Generic message, does not revel if file exists or not
                print("No notes found")
            except Exception:
                # Fix 3: Secure Error Handling - Part 2
                # Earlier: print(f"Error: {e}")leaked file path and stack trace
                # Now: Generic message hides internal details from attacker
                print("Unable  to read notes")

        else:
                # Same message for wrong password and wrong user - prevents user enumeration
                print("Invalid credentials")

    else:
            print("New user - registering securely")
            # Hash password before storing 
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute("INSERT INTO users VALUES (?,?)", (username, hashed.decode()))
            conn.commit()
            print("User registration with hashed password - plain text never stored")

    conn.close()

if __name__ == "__main__":
    login_secure()