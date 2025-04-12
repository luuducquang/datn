from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import News
from service.news import ser_get_new,ser_delete_new, ser_insert_new, ser_update_new


router = APIRouter()

new_collection: Collection = database['News']
user_collection: Collection = database['Users']

@router.get("/news/get")
async def get_new():
    return ser_get_new()

@router.get("/news/get/{new_id}")
async def get_new_by_id(new_id: str):
    if not ObjectId.is_valid(new_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    new = new_collection.find_one({"_id": ObjectId(new_id)})

    if new is None:
        raise HTTPException(status_code=404, detail="News not found")

    new_collection.update_one({"_id": ObjectId(new_id)}, {"$inc": {"view": 1}})

    user = user_collection.find_one({"_id": ObjectId(new["user_id"])})
    if user:
        new["fullname"] = user.get("fullname", "Unknown")
    else:
        new["fullname"] = "Unknown"

    new["_id"] = str(new["_id"])
    return new

@router.post("/news/search")
async def search_new(
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
            {"title": {"$regex": search_term, "$options": "i"}},
            {"content": {"$regex": search_term, "$options": "i"}},
            {"view": {"$regex": search_term, "$options": "i"}},
        ]

    user_ids = []
    if search_term:
        user_query = {"fullname": {"$regex": search_term, "$options": "i"}}
        users = user_collection.find(user_query)
        user_ids = [str(user["_id"]) for user in users]

    if user_ids:
        query["$or"].append({"user_id": {"$in": user_ids}})

    total_items = new_collection.count_documents(query)

    news = new_collection.find(query).skip(skip).limit(pageSize)

    data = []
    for new in news:
        new["_id"] = str(new["_id"])

        user = user_collection.find_one({"_id": ObjectId(new["user_id"])})
        if user:
            new["fullname"] = user.get("fullname", "")
        else:
            new["fullname"] = ""
        data.append(new)

    return {
        "page": page,
        "pageSize": pageSize,
        "totalItems": total_items,
        "data": data,
    }



@router.post("/news/add")
async def create_new(_data: News):
    _id = ser_insert_new(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/news/update")
def edit_new(_data: News):
    result = ser_update_new(_data, new_collection)
    return result

@router.delete("/news/delete/{new_id}")
def remove_new(new_id: str):
    response = ser_delete_new(new_id, new_collection)
    return response