from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Manufactors
from config.database import database

manufactor_collection: Collection = database['Manufactors']

def ser_get_manufactor():
    datas = []
    for data in manufactor_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_manufactor(_data: Manufactors) -> str:
    result = manufactor_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_manufactor(_data: Manufactors, manufactor_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_manufactor = manufactor_collection.find_one({"_id": object_id})
    if not existing_manufactor:
        raise HTTPException(status_code=404, detail="manufactor not found")
    
    updated_manufactor = manufactor_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_manufactor.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_manufactor(manufactor_id: str, manufactor_collection: Collection):
    if not ObjectId.is_valid(manufactor_id):
        raise HTTPException(status_code=400, detail="Invalid manufactor ID")

    result = manufactor_collection.delete_one({"_id": ObjectId(manufactor_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="manufactor not found")
    
    return {"message": "manufactor deleted successfully"}
