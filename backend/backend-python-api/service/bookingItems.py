from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, BookingItems
from config.database import database

bookingitem_collection: Collection = database['BookingItems']
menuitem_collection: Collection = database['MenuItems']

def ser_get_bookingitem():
    datas = []
    for data in bookingitem_collection.find():
        data["_id"] = str(data["_id"])
        
        item_data = menuitem_collection.find_one({"_id": ObjectId(data["item_id"])})
        if item_data:
            item_data["_id"] = str(item_data["_id"])  
            data["menuitem"] = item_data  
        else:
            data["menuitem"] = None  

        datas.append(data)
    return datas

def ser_getbyid_bookingitem(booking_id: str):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    results = list(bookingitem_collection.find({"booking_id": booking_id}))

    for item in results:
        item["_id"] = str(item["_id"])

    return results


def ser_insert_bookingitem(_data: BookingItems) -> str:
    result = bookingitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_bookingitem(_data: BookingItems, bookingitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_bookingitem = bookingitem_collection.find_one({"_id": object_id})
    if not existing_bookingitem:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    updated_bookingitem = bookingitem_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_bookingitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_bookingitem(bookingitem_id: str, bookingitem_collection: Collection):
    if not ObjectId.is_valid(bookingitem_id):
        raise HTTPException(status_code=400, detail="Invalid tableType ID")

    result = bookingitem_collection.delete_one({"_id": ObjectId(bookingitem_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    return {"message": "tableType deleted successfully"}
