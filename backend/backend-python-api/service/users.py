from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, Users
from config.database import database
from service.login import hash_password

user_collection: Collection = database['Users']

def ser_get_users():
    datas = []
    for data in user_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    user["_id"] = str(user["_id"])
    user.pop("password", None) 
    return user

def ser_search_user(_data: Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")

    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"username": {"$regex": _data.search_term, "$options": "i"}},
            {"fullname": {"$regex": _data.search_term, "$options": "i"}},
            {"email": {"$regex": _data.search_term, "$options": "i"}},
            {"phone": {"$regex": _data.search_term, "$options": "i"}}
        ]

    total_items = user_collection.count_documents(query)
    users = user_collection.find(query).skip(skip).limit(_data.pageSize)

    data = []
    for user in users:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        data.append(user)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

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
        raise HTTPException(status_code=404, detail="User not found")

    if _data.password:
        _data.password = hash_password(_data.password)

    update_data = _data.dict(exclude={"id", "is_verified", "created_at"})

    updated_user = user_collection.update_one(
        {"_id": object_id},  
        {"$set": update_data}
    )

    if updated_user.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed or no changes made")

    return {"message": "User updated successfully"}


def ser_delete_user(user_id: str, user_collection: Collection):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="user not found")
    
    return {"message": "user deleted successfully"}
