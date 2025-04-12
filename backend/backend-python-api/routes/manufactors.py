from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Manufactors
from service.manufactor import ser_get_manufactor,ser_delete_manufactor, ser_insert_manufactor, ser_update_manufactor


router = APIRouter()

manufactor_collection: Collection = database['Manufactors']

@router.get("/manufactors/get")
async def get_manufactor():
    return ser_get_manufactor()

@router.get("/manufactors/get/{manufactor_id}")
async def get_manufactor_by_id(manufactor_id: str):
    if not ObjectId.is_valid(manufactor_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    manufactor = manufactor_collection.find_one({"_id": ObjectId(manufactor_id)})

    if manufactor is None:
        raise HTTPException(status_code=404, detail="manufactor not found")

    manufactor["_id"] = str(manufactor["_id"])
    return manufactor

@router.post("/manufactors/search")
async def search_manufactor(
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
            {"name": {"$regex": search_term, "$options": "i"}},
            {"phone": {"$regex": search_term, "$options": "i"}},
            {"address": {"$regex": search_term, "$options": "i"}},
        ]

    total_items = manufactor_collection.count_documents(query)

    manufactors = manufactor_collection.find(query).skip(skip).limit(pageSize)

    data = []
    for manufactor in manufactors:
        manufactor["_id"] = str(manufactor["_id"])
        data.append(manufactor)

    return {
        "page":page,
        "pageSize":pageSize,
        "totalItems": total_items,
        "data": data,
    }


@router.post("/manufactors/add")
async def create_manufactor(_data: Manufactors):
    _id = ser_insert_manufactor(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/manufactors/update")
def edit_manufactor(_data: Manufactors):
    result = ser_update_manufactor(_data, manufactor_collection)
    return result

@router.delete("/manufactors/delete/{manufactor_id}")
def remove_manufactor(manufactor_id: str):
    response = ser_delete_manufactor(manufactor_id, manufactor_collection)
    return response