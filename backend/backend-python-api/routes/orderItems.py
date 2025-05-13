from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import OrderItems
from service.orderItems import ser_get_foodorder,ser_delete_foodorder, ser_insert_foodorder, ser_update_foodorder


router = APIRouter()

foodorder_collection: Collection = database['OrderItems']

@router.get("/foodorders/get")
async def get_foodorder():
    return ser_get_foodorder()

@router.post("/foodorders/add")
async def create_foodorder(_data: OrderItems):
    _id = ser_insert_foodorder(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/foodorders/update")
def edit_foodorder(_data: OrderItems):
    result = ser_update_foodorder(_data, foodorder_collection)
    return result

@router.delete("/foodorders/delete/{foodorder_id}")
def remove_foodorder(foodorder_id: str):
    response = ser_delete_foodorder(foodorder_id, foodorder_collection)
    return response