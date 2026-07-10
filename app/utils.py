from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    
    return hasher.hash(password)

def verify_hash(plaintext: str, pwd_hash: str) -> bool:
    return hasher.verify(password=plaintext, hash=pwd_hash)