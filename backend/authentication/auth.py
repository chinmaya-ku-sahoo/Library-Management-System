
from fastapi import HTTPException
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timedelta

import hashlib
import secrets

class Auth():
    '''
    Class to authorize user.
    '''
    hasher= CryptContext(schemes=['bcrypt'])
    secret = secrets.token_hex(32)
    
    def encode_psswrd(self, psswrd, salt):
        '''
        Method to encode password using sha512 algorithm and salt.
        '''

        encoded_psswrd = psswrd.encode()
        digest = hashlib.pbkdf2_hmac('sha512', encoded_psswrd, salt, 100000)
        hashedpsswrd = digest.hex()
        return hashedpsswrd

    def encode_token(self, userid):
        '''
        Method to encode token.
        '''
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'scope': 'access_token',
            'sub' : str(userid)
        }

        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        '''
        Method to decode the token and return user id.
        '''
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(status_code=401, detail={"message": "Invalid Token Scope"})
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail={"message": f"Token Expired: {e}"})
        except JWTError as e:
            raise HTTPException(status_code=401, detail={"message": f"Invalid Token: {e}"})
