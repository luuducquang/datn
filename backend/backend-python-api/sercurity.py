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

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> dict:
    """
    Decode JWT token => return payload dict with email and role_name
    """
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials,
            SECRET_KEY,
            algorithms=[SECURITY_ALGORITHM]
        )

        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")

        if not payload.get("email"):
            raise HTTPException(status_code=403, detail="Email not found in token")

        if not payload.get("role_name"):
            raise HTTPException(status_code=403, detail="Role not found in token")

        return payload

    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def require_role(allowed_roles: list):
    def checker(payload: dict = Depends(validate_token)):
        role = payload.get("role_name")
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return payload
    return checker