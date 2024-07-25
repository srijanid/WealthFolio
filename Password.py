import hashlib
import hmac
import os

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt
    else:
        salt = bytes.fromhex(salt)
    password = password.encode('utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return salt.hex() + '$' + hashed_password.hex()

def verify_password(stored_password, provided_password):
    salt, hashed_password = stored_password.split('$')
    return hmac.compare_digest(
        hash_password(provided_password, salt).split('$')[1],
        hashed_password
    )
