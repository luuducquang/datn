import uuid
import hmac
import hashlib
import requests
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/momo/create-payment")
async def create_payment(request: Request):
    body = await request.json()
    amount = str(body.get("amount", "0")) 

    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"

    orderInfo = "pay with MoMo"
    redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
    ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureWallet"
    extraData = ""

    raw_signature = (
        f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}"
        f"&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}"
        f"&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
    )

    signature = hmac.new(
        secretKey.encode('utf-8'),
        raw_signature.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    data = {
        "partnerCode": partnerCode,
        "accessKey": accessKey,
        "requestId": requestId,
        "amount": amount,
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "extraData": extraData,
        "requestType": requestType,
        "signature": signature,
        "lang": "vi"
    }

    response = requests.post(endpoint, json=data)
    return response.json()


@router.get("/momo/status/{order_id}")
def check_momo_payment_status(order_id: str):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/query"

    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    requestId = order_id 

    raw_signature = (
        f"accessKey={accessKey}&orderId={order_id}&partnerCode={partnerCode}&requestId={requestId}"
    )

    signature = hmac.new(
        secretKey.encode('utf-8'),
        raw_signature.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    data = {
        "partnerCode": partnerCode,
        "accessKey": accessKey,
        "requestId": requestId,
        "orderId": order_id,
        "signature": signature,
        "lang": "vi"
    }

    response = requests.post(endpoint, json=data)
    return response.json()