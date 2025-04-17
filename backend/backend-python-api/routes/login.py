import jwt
import random
import string

from fastapi import APIRouter, Depends,Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import LoginRegisterRequest, ResetPassword
from typing import Union, Any
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema
from config.config import conf
from schemas.schemas import EmailRequest, Users,VerifyOTP


router = APIRouter()

user_collection: Collection = database['Users']

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

@router.post("/login")
def login(request_data: LoginRegisterRequest):
    user = user_collection.find_one({"email": request_data.email})

    if not user or user["password"] != request_data.password:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    
    elif not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Tài khoản chưa được xác thực")
         
    else:
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
    

def generate_token(email: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3 
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@router.post("/register")
async def register_user(request_data: Users):
    existing_user = user_collection.find_one({"email": request_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    otp = generate_otp()
    otp_expires_at = datetime.utcnow() + timedelta(minutes=5)

    new_user = request_data.dict(exclude={"id"})
    new_user["otp"] = otp
    new_user["otp_expires_at"] = otp_expires_at
    new_user["is_verified"] = False
    new_user["created_at"] = datetime.utcnow()

    user_collection.insert_one(new_user)

    body = (
    f"Xin chào {request_data.email},\n\n"
    f"Bạn vừa yêu cầu một mã OTP để xác thực tài khoản.\n"
    f"Mã OTP của bạn là: {otp}\n"
    f"Mã sẽ hết hạn sau 5 phút kể từ bây giờ.\n\n"
    "Trân trọng,\n"
    "Q-Billiard Team"
    )

    message = MessageSchema(
    subject="Xác thực tài khoản",
    recipients=[request_data.email],
    body=body,
    subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "Đăng ký thành công. Vui lòng kiểm tra email để xác thực tài khoản."}


@router.post("/verify-otp")
async def verify_otp(request_data: VerifyOTP):
    user = user_collection.find_one({"email": request_data.email})
    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    if user["otp"] != request_data.otp:
        raise HTTPException(status_code=400, detail="Mã OTP không hợp lệ")

    if datetime.utcnow() > user["otp_expires_at"]:
        raise HTTPException(status_code=400, detail="Mã OTP đã hết hạn")

    user_collection.update_one(
        {"email": request_data.email},
        {"$set": {"is_verified": True, "otp": None, "otp_expires_at": None}}
    )

    return {"message": "Xác thực tài khoản thành công!"}


@router.post("/resend-otp")
async def resend_otp(email_request: EmailRequest):
    user = user_collection.find_one({"email": email_request.email})

    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    if user["is_verified"]:
        raise HTTPException(status_code=400, detail="Tài khoản đã được xác thực")

    otp = generate_otp()
    otp_expires_at = datetime.utcnow() + timedelta(minutes=5)

    user_collection.update_one(
        {"email": email_request.email},
        {"$set": {"otp": otp, "otp_expires_at": otp_expires_at}}
    )

    message = MessageSchema(
        subject="Mã OTP mới",
        recipients=[email_request.email],
        body=f"Mã OTP mới của bạn là: {otp}. Hết hạn sau 5 phút.",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "OTP mới đã được gửi đến email của bạn."}


@router.post("/forgot-password")
async def forgot_password(email_request: EmailRequest):
    user = user_collection.find_one({"email": email_request.email})

    if not user:
        raise HTTPException(status_code=404, detail="Email không tồn tại")

    otp = generate_otp()
    otp_expires_at = datetime.utcnow() + timedelta(minutes=5)

    user_collection.update_one(
        {"email": email_request.email},
        {"$set": {"otp": otp, "otp_expires_at": otp_expires_at}}
    )

    body = (
        f"Xin chào {email_request.email},\n\n"
        f"Bạn đã yêu cầu đặt lại mật khẩu.\n"
        f"Mã xác thực của bạn là: {otp}\n"
        f"Mã sẽ hết hạn sau 5 phút.\n\n"
        "Trân trọng,\n"
        "Q-Billiard Team"
    )

    message = MessageSchema(
        subject="Yêu cầu đặt lại mật khẩu",
        recipients=[email_request.email],
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "Mã xác thực đã được gửi đến email của bạn."}


@router.post("/reset-password")
async def reset_password(data: ResetPassword):
    user = user_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

    if user["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Mã OTP không đúng")

    if datetime.utcnow() > user["otp_expires_at"]:
        raise HTTPException(status_code=400, detail="Mã OTP đã hết hạn")

    user_collection.update_one(
        {"email": data.email},
        {"$set": {
            "password": data.new_password,  
            "otp": None,
            "otp_expires_at": None
        }}
    )

    return {"message": "Mật khẩu đã được đặt lại thành công."}
