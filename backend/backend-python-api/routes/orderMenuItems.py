from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, OrderMenuItems
from service.orderMenuItems import ser_getbyid_ordermenuitem,ser_search_ordermenuitem,ser_get_ordermenuitem,ser_delete_ordermenuitem, ser_insert_ordermenuitem, ser_update_ordermenuitem


router = APIRouter()

ordermenuitem_collection: Collection = database['OrderMenuItems']

@router.get("/ordermenuitems/get")
async def get_ordermenuitem():
    return ser_get_ordermenuitem()

@router.get("/ordermenuitems/get/{orderitem_id}")
async def get_ordermenuitem_by_id(orderitem_id: str):
    return ser_getbyid_ordermenuitem(orderitem_id)

@router.post("/ordermenuitems/search")
async def search_ordermenuitem(_data:Searchs):
    return ser_search_ordermenuitem(_data)

@router.post("/ordermenuitems/add")
async def create_ordermenuitem(_data: OrderMenuItems):
    _id = ser_insert_ordermenuitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/ordermenuitems/update")
def edit_ordermenuitem(_data: OrderMenuItems):
    result = ser_update_ordermenuitem(_data, ordermenuitem_collection)
    return result

@router.delete("/ordermenuitems/delete/{ordermenuitem_id}")
def remove_ordermenuitem(ordermenuitem_id: str):
    response = ser_delete_ordermenuitem(ordermenuitem_id, ordermenuitem_collection)
    return response