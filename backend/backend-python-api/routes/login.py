import jwt

from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import LoginRegisterRequest
from typing import Union, Any
from datetime import datetime, timedelta


router = APIRouter()

user_collection: Collection = database['Users']

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

@router.post("/login")
def login(request_data: LoginRegisterRequest):
    user = user_collection.find_one({"email": request_data.email, "password": request_data.password})
    
    if user:
        token = generate_token(request_data.email)
    
        return {
                "_id": str(user.get("_id")),   
                "email": user["email"],
                "password": user.get("password", ""),
                "fullname": user.get("fullname", ""),
                "phone": user.get("phone", ""),
                "address": user.get("address", ""),
                "avatar": user.get("avatar", ""),
                "loyalty_points": user.get("loyalty_points", ""),
                "role_name": user.get("role_name", ""),
                "token": token
            }
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    

def generate_token(email: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3 
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt