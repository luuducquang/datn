from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import ImportItems
from service.importItems import ser_get_importitem,ser_delete_importitem, ser_insert_importitem, ser_update_importitem


router = APIRouter()

importitem_collection: Collection = database['ImportItems']
rentalitem_collection: Collection = database['RentalItems']
menuitem_collection: Collection = database['MenuItems']

@router.get("/importitems/get")
async def get_importitem():
    return ser_get_importitem()

@router.post("/importitems/add")
async def create_importitem(_data: ImportItems):
    _id = ser_insert_importitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/importitems/update")
def edit_importitem(_data: ImportItems):
    result = ser_update_importitem(_data, importitem_collection)
    return result

@router.delete("/importitems/delete/{importitem_id}")
def remove_importitem(importitem_id: str):
    response = ser_delete_importitem(
        importitem_id, 
        importitem_collection, 
        rentalitem_collection, 
        menuitem_collection
    )
    return response