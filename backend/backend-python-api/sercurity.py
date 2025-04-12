import jwt
from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        
        expiration = payload.get('exp')
        if expiration:
            expiration = datetime.fromtimestamp(expiration)
            if expiration < datetime.now():
                raise HTTPException(status_code=403, detail="Token expired")
        
        username = payload.get('username')
        if not username:
            raise HTTPException(status_code=403, detail="Username not found in token")
        
        return username
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
