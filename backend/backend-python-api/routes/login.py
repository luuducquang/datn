

from fastapi import APIRouter, Depends,Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import LoginRegisterRequest, ResetPassword
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema
from config.config import conf
from schemas.schemas import EmailRequest, Users,VerifyOTP
from service.login import check_password, generate_otp, generate_token, hash_password


router = APIRouter()

user_collection: Collection = database['Users']


@router.post("/login")
def login(request_data: LoginRegisterRequest):
    user = user_collection.find_one({"email": request_data.email})
    print (datetime.now())
    print (datetime.now())

    if not user:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    stored_password = user.get("password", "")
    entered_password = request_data.password

    if not check_password(stored_password, entered_password):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")

    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Tài khoản chưa được xác thực")

    token = generate_token(request_data.email,user.get("role_name", ""))

    return {
        "_id": str(user.get("_id")),
        "email": user["email"],
        "password": entered_password,
        "fullname": user.get("fullname", ""),
        "phone": user.get("phone", ""),
        "address": user.get("address", ""),
        "avatar": user.get("avatar", ""),
        "loyalty_points": user.get("loyalty_points", 0),
        "wallet": user.get("wallet", 0),
        "role_name": user.get("role_name", ""),
        "token": token
    }
    

@router.post("/register")
async def register_user(request_data: Users):
    existing_user = user_collection.find_one({"email": request_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    otp = generate_otp()
    otp_expires_at = datetime.now() + timedelta(minutes=5)

    hashed_password = hash_password(request_data.password)

    new_user = request_data.dict(exclude={"id"})
    new_user["password"] = hashed_password
    new_user["otp"] = otp
    new_user["otp_expires_at"] = otp_expires_at
    new_user["is_verified"] = False
    new_user["created_at"] = datetime.now()

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

    if datetime.now() > user["otp_expires_at"]:
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
    otp_expires_at = datetime.now() + timedelta(minutes=5)

    user_collection.update_one(
        {"email": email_request.email},
        {"$set": {"otp": otp, "otp_expires_at": otp_expires_at}}
    )

    body = (
    f"Xin chào {email_request.email},\n\n"
    f"Bạn vừa yêu cầu một mã OTP để xác thực tài khoản.\n"
    f"Mã OTP của bạn là: {otp}\n"
    f"Mã sẽ hết hạn sau 5 phút kể từ bây giờ.\n\n"
    "Trân trọng,\n"
    "Q-Billiard Team"
    )

    message = MessageSchema(
    subject="Xác thực tài khoản",
    recipients=[email_request.email],
    body=body,
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
    otp_expires_at = datetime.now() + timedelta(minutes=5)

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

    if datetime.now() > user["otp_expires_at"]:
        raise HTTPException(status_code=400, detail="Mã OTP đã hết hạn")
    
    hashed_password = hash_password(data.new_password)

    user_collection.update_one(
        {"email": data.email},
        {"$set": {
            "password": hashed_password,
            "otp": None,
            "otp_expires_at": None
        }}
    )

    return {"message": "Mật khẩu đã được đặt lại thành công."}
