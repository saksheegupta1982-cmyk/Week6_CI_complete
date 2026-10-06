# Week6 CLI Integration - Security Enhancement 

This project implements secure coding practices with CI pipeline.

## Features
- Input Sanitization to block SQL Injection & Path Traversal 
- Secure DB Operations using Parameterized Queries
- Password Hashing with bcrypt
- Automated Tests with Pytest

## Project Structure
 - `app_secure.py' - Secure implementation
 - `app_Vulnerable.py` - Vulnerable version (for comparison)
 - `tests/test_secure.py` - 4 Security tests
 - `.github/workflows/ci.yml` - GitHub Action CI Pipeline

## How to Run Locally 
'''bash 
pip install -r requirements.txt
pytest tests/ -v
bandit -r app_secure.py -11