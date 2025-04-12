from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import SellItems
from service.sellItems import ser_get_sellitem,ser_delete_sellitem, ser_insert_sellitem, ser_update_sellitem


router = APIRouter()

sellitem_collection: Collection = database['SellItems']
rentalitem_collection: Collection = database['RentalItems']

@router.get("/sellitems/get")
async def get_sellitem():
    return ser_get_sellitem()

@router.post("/sellitems/add")
async def create_sellitem(_data: SellItems):
    _id = ser_insert_sellitem(_data, sellitem_collection, rentalitem_collection)
    return {"message": "Created successfully", "_id": _id}

@router.put("/sellitems/update")
def edit_sellitem(_data: SellItems):
    result = ser_update_sellitem(_data, sellitem_collection, rentalitem_collection)
    return result

@router.delete("/sellitems/delete/{sellitem_id}")
def remove_sellitem(sellitem_id: str):
    response = ser_delete_sellitem(sellitem_id, sellitem_collection, rentalitem_collection)
    return response