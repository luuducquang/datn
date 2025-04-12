from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Users
from config.database import database

user_collection: Collection = database['Users']

def ser_get_users():
    datas = []
    for data in user_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_user(_data: Users) -> str:
    existing_email = user_collection.find_one({"email": _data.email})
    if existing_email:
        raise HTTPException(status_code=400, detail=f"email '{_data.email}' already exists.")
    result = user_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_user(_data: Users, user_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_user = user_collection.find_one({"_id": object_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="user not found")
    
    updated_user = user_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_user.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_user(user_id: str, user_collection: Collection):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    
    return {"message": "user deleted successfully"}
