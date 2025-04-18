from typing import List
from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import BillSells, Searchs
from service.billSells import ser_get_billsell_by_billsell_id,ser_get_billsell,ser_delete_billsell, ser_insert_billsell, ser_search_billsell, ser_update_billsell,ser_get_billsell_by_user,ser_get_billsell_by_sell_id
from service.paypal import capture_order, create_order


router = APIRouter()

billsell_collection: Collection = database['BillSells']

@router.get("/billsells/get")
async def get_billsell():
    return ser_get_billsell()

@router.get("/billsells/get/{user_id}")
async def get_billsell(user_id: str):
    response = ser_get_billsell_by_user(user_id)
    return response

@router.get("/billsells/get-billsell-id/{sell_id}")
async def get_billsell(sell_id: str):
    response = ser_get_billsell_by_sell_id(sell_id)
    return response

@router.get("/billsells/get-detail-billsell/{billsel_id}")
async def get_billsell(billsel_id: str):
    response = ser_get_billsell_by_billsell_id(billsel_id)
    return response

@router.post("/billsells/search")
async def search_billsells(data: Searchs):
    result = ser_search_billsell(data)
    return result

@router.post("/billsells/add")
async def create_billsell(data: BillSells):
    _id = ser_insert_billsell(data)
    return {"message": "Created successfully", "_id": _id}

@router.post("/paypal/create-order")
async def create_paypal_order(amount: float):
    order = create_order(str(amount))
    return order

@router.post("/paypal/capture-order/{order_id}")
async def capture_paypal_order(order_id: str):
    result = capture_order(order_id)
    return result

@router.put("/billsells/update")
def edit_billsell(_data: BillSells):
    result = ser_update_billsell(_data, billsell_collection)
    return result

@router.delete("/billsells/delete/{billsell_id}")
def remove_billsell(billsell_id: str):
    response = ser_delete_billsell(billsell_id, billsell_collection)
    return response