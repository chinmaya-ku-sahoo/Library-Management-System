from fastapi import HTTPException

import os
import hashlib

def hash_password(psswrd: str)->str:
    """
    Function to hash the password and generate salt.
    """
    try:
        salt = os.urandom(32)
        encoded_psswrd = psswrd.encode()
        digest = hashlib.pbkdf2_hmac('sha512', encoded_psswrd, salt, 100000)
        hashedpsswrd = digest.hex()
        
        return hashedpsswrd, salt
    
    except Exception as e: 
        HTTPException(status_code=500, detail={"message": f"Unable to hash the password due to {e}"})
