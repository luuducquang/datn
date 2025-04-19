from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException

PAYPAL_CLIENT_ID = "AevnZPJJW8_kjKZW3V2nrryVCEreZzQJXFodD54xoNJaXLLEF8hh3863ld1FWjY3w1QJDUbx9UrobbHr"
PAYPAL_SECRET = "ELEGM5gSAY2KWEfiaGFLGy8egXE6LxA4YuXANWeoiO8wMri_C97-MvcsO3q1CCH3lcy5bvbvL0XTpMsn"
PAYPAL_API_BASE = "https://sandbox.paypal.com"  

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

def get_vcb_usd_rate():
    url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    usd = soup.find("Exrate", attrs={"CurrencyCode": "USD"})
    if usd:
        sell_rate = usd["Sell"].replace(",", "") 
        return float(sell_rate)
    raise HTTPException(status_code=500, detail="Failed to get VCB exchange rate")

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
        json=data,
        timeout=10
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
