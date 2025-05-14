from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import OrderItems
from service.orderItems import ser_get_orderitem,ser_delete_orderitem, ser_insert_orderitem, ser_update_orderitem


router = APIRouter()

orderitem_collection: Collection = database['OrderItems']

@router.get("/orderitems/get")
async def get_orderitem():
    return ser_get_orderitem()

@router.post("/orderitems/add")
async def create_orderitem(_data: OrderItems):
    _id = ser_insert_orderitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/orderitems/update")
def edit_orderitem(_data: OrderItems):
    result = ser_update_orderitem(_data, orderitem_collection)
    return result

@router.delete("/orderitems/delete/{orderitem_id}")
def remove_orderitem(orderitem_id: str):
    response = ser_delete_orderitem(orderitem_id, orderitem_collection)
    return response