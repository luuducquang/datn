import jwt
import random
import string
import bcrypt
from typing import Union, Any
from datetime import datetime, timedelta

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

def generate_token(email: Union[str, Any]) -> str:
    expire = datetime.now() + timedelta(
        seconds=60 * 60 * 24 * 3 
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_password: str, entered_password: str) -> bool:
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))