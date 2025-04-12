from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Users
from service.users import ser_get_users,ser_delete_user, ser_insert_user, ser_update_user
from sercurity import validate_token


router = APIRouter()
# dependencies=[Depends(validate_token)]

user_collection: Collection = database['Users']

@router.get("/users/get")
async def get_users():
    return ser_get_users()

@router.get("/users/get/{user_id}")
async def get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    user = user_collection.find_one({"_id": ObjectId(user_id)})

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    user["_id"] = str(user["_id"])
    return user

@router.post("/users/search")
async def search_user(
    page: int = Body(...),
    pageSize: int = Body(...),
    search_term: Optional[str] = Body(None)
):
    if page <= 0 or pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (page - 1) * pageSize

    query = {}
    if search_term:
        query["$or"] = [
            {"username": {"$regex": search_term, "$options": "i"}},
            {"fullname": {"$regex": search_term, "$options": "i"}},
            {"email": {"$regex": search_term, "$options": "i"}},
            {"phone": {"$regex": search_term, "$options": "i"}}
        ]

    total_items = user_collection.count_documents(query)

    users = user_collection.find(query).skip(skip).limit(pageSize)

    data = []
    for user in users:
        user["_id"] = str(user["_id"])
        data.append(user)

    return {
        "page":page,
        "pageSize":pageSize,
        "totalItems": total_items,
        "data": data,
    }

@router.post("/users/add")
async def create_user(_data: Users):
    _id = ser_insert_user(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/users/update")
def edit_user(_data: Users):
    result = ser_update_user(_data, user_collection)
    return result

@router.delete("/users/delete/{user_id}")
def remove_user(user_id: str):
    response = ser_delete_user(user_id, user_collection)
    return response