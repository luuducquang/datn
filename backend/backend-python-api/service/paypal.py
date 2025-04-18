import requests
from fastapi import HTTPException

PAYPAL_CLIENT_ID = "AevnZPJJW8_kjKZW3V2nrryVCEreZzQJXFodD54xoNJaXLLEF8hh3863ld1FWjY3w1QJDUbx9UrobbHr"
PAYPAL_SECRET = "AevnZPJJW8_kjKZW3V2nrryVCEreZzQJXFodD54xoNJaXLLEF8hh3863ld1FWjY3w1QJDUbx9UrobbHr"
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"  

def get_access_token():
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        headers={"Accept": "application/json"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get PayPal token")
    return response.json()["access_token"]

def create_order(total_amount: str, currency="USD"):
    access_token = get_access_token()
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": total_amount
                }
            }
        ]
    }
    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=data
    )
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")
    return response.json()

def capture_order(order_id: str):
    access_token = get_access_token()
    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to capture PayPal order")
    return response.json()
