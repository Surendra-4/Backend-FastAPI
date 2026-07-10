"""
This file contains the utility functions that are required for the application.
"""

from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

# Takes a password, returns a hash
def hash_password(password: str) -> str:
    
    return hasher.hash(password)

# Takes plaintext and hash to return true if similar else false
def verify_hash(plaintext: str, pwd_hash: str) -> bool:
    return hasher.verify(password=plaintext, hash=pwd_hash)