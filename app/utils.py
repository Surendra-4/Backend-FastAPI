from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    
    return hasher.hash(password)