from typing import List
from fastapi import APIRouter, Body
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Carts
from service.carts import ser_get_cart,ser_delete_cart, ser_insert_cart, ser_update_cart,ser_get_cart_by_user_id,ser_update_cart_false_status,ser_delete_carts


router = APIRouter()

cart_collection: Collection = database['Carts']

@router.get("/carts/get")
async def get_cart():
    return ser_get_cart()

@router.get("/carts/get/{user_id}")
async def get_cart_by_user_id(user_id: str):
    return ser_get_cart_by_user_id(user_id)

@router.post("/carts/add")
async def create_cart(_data: Carts):
    _id = ser_insert_cart(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/carts/update")
def edit_cart(_data: Carts):
    result = ser_update_cart(_data, cart_collection)
    return result

@router.put("/carts/updatefalsestatus/{user_id}")
def edit_cart_false_status(user_id: str):
    result = ser_update_cart_false_status(user_id, cart_collection)
    return result

@router.delete("/carts/delete/{cart_id}")
def remove_cart(cart_id: str):
    response = ser_delete_cart(cart_id, cart_collection)
    return response

@router.delete("/carts/delete")
def remove_carts(cart_ids: List[str] = Body(...)):
    response = ser_delete_carts(cart_ids, cart_collection)
    return response