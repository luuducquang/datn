from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import TimeSessions
from config.database import database

timesession_collection: Collection = database['TimeSessions']

def ser_get_timesession():
    datas = []
    for data in timesession_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_timesession(_data: TimeSessions) -> str:
    result = timesession_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_timesession(_data: TimeSessions, timesession_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_timesession = timesession_collection.find_one({"_id": object_id})
    if not existing_timesession:
        raise HTTPException(status_code=404, detail="timesession not found")
    
    updated_timesession = timesession_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_timesession.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_timesession(timesession_id: str, timesession_collection: Collection):
    if not ObjectId.is_valid(timesession_id):
        raise HTTPException(status_code=400, detail="Invalid timesession ID")

    result = timesession_collection.delete_one({"_id": ObjectId(timesession_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="timesession not found")
    
    return {"message": "timesession deleted successfully"}
