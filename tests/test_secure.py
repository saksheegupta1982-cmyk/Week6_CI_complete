"""
tests/test_secure.py - Automated Test Suite for CI Pipeline
 This file is executed by GitHub Actions (ci.yml) on every push.
 If any test fails, the CI pipeline will FAIL - acting as quality gate.

 Covers Week 5 security fixes validation.
 """

import os 
import sqlite3
import sys

# Fix for ModuleNotFoundError in CI: Add parent directory
# So that tests/ can import app_secure.py from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_secure import sanitize_input, init_db

def test_sanitize_valid():
    """ Test that valid alphanumeric usernames are accepted."""
    assert sanitize_input("admin123") == "admin123"

def test_sanitize_blocks_sql_injection():
    """
    Test SQL Injection prevention.
    Payload "' OR '1'='1" was able to bypass login in vulnerable version.
    Secure version must raise VulueError.
    """ 
    try:
        sanitize_input(" 'OR'1'='1")
        assert False, "Should have blocked SQLi"
    except ValueError:
        assert True # Excepted - blocked

def test_sanitize_blocks_path_traversal():
    """
    Test Path Traversal prevention.
    Payload"../../etc/passwd" could read system files in vulnerable version.
    """
    try:
        sanitize_input("../../etc/passwd")
        assert False, "Should have blocked Path Traversal"
    except ValueError:
        assert True

def test_init_db_creates_table():
    """Test that init_db() creates users.db and users table - needed for CI fresh env."""
    if os.path.exists("users.db"):
        os.remove("users.db")
    init_db()
    assert os.path.exists("users.db")
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='users'")
    assert cur.fetchone() is not None
    conn.close()

