
from fastapi import APIRouter
from fastapi import HTTPException
from schemas.schemas import  PaymentRequest
from service.paypal import capture_order, create_order, get_vcb_usd_rate


router = APIRouter()

@router.post("/paypal/create-order")
async def create_paypal_order(data: PaymentRequest):  
    try:
        exchange_rate = get_vcb_usd_rate()
        usd_amount = round(data.amount / exchange_rate, 2)
        order = create_order(str(usd_amount))
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/paypal/capture-order/{order_id}")
async def capture_paypal_order(order_id: str):
    result = capture_order(order_id)
    return result