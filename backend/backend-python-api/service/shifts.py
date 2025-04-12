from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Shifts
from config.database import database

shift_collection: Collection = database['Shifts']

def ser_get_shift():
    datas = []
    for data in shift_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_shift(_data: Shifts) -> str:
    result = shift_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_shift(_data: Shifts, shift_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_shift = shift_collection.find_one({"_id": object_id})
    if not existing_shift:
        raise HTTPException(status_code=404, detail="shift not found")
    
    updated_shift = shift_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_shift.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_shift(shift_id: str, shift_collection: Collection):
    if not ObjectId.is_valid(shift_id):
        raise HTTPException(status_code=400, detail="Invalid shift ID")

    result = shift_collection.delete_one({"_id": ObjectId(shift_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="shift not found")
    
    return {"message": "shift deleted successfully"}
