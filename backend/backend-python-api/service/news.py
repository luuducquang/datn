from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import News
from config.database import database

new_collection: Collection = database['News']

def ser_get_new():
    datas = []
    for data in new_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_new(_data: News) -> str:
    result = new_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_new(_data: News, new_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_new = new_collection.find_one({"_id": object_id})
    if not existing_new:
        raise HTTPException(status_code=404, detail="new not found")
    
    updated_new = new_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_new.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_new(new_id: str, new_collection: Collection):
    if not ObjectId.is_valid(new_id):
        raise HTTPException(status_code=400, detail="Invalid new ID")

    result = new_collection.delete_one({"_id": ObjectId(new_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="new not found")
    
    return {"message": "new deleted successfully"}
