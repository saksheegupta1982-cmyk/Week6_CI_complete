# app_vulnerable.py - Vulnerable Version 
import sqlite3
import os

# Vulnerability 1: Hardcoded secret 
SECRET_KEY = "admin123"

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def login():
    init_db()
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnerability 2: SQL Injection 
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    # Vulnerability 3: Improper Error Handling - Leaks info
    if user:
        print("Login success")
        try:
            note = open(f"{username}_notes.txt").read() # Vulnerability 4: Path Traversal
            print(note)
        except Exception as e:
            print(f"Error: {e}") # Show full stack trace

    else:
        print("Invalid login")

    # Vulnerability 5: Weak hashing / Plain text storage
        cursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}')")
        conn.commit()
        print("User registered")

    conn.close()

if __name__ == "__main__":
 login()