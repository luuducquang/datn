from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import CategoryMenuItems, Searchs
from config.database import database

categorymenuitem_collection: Collection = database['CategoryMenuItems']

def ser_get_category():
    datas = []
    for data in categorymenuitem_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_categorymenuitem(category_id: str):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    category = categorymenuitem_collection.find_one({"_id": ObjectId(category_id)})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    category["_id"] = str(category["_id"])
    return category

def ser_search_categorymenuitem(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"category_name": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = categorymenuitem_collection.count_documents(query)

    categorymenuitems = categorymenuitem_collection.find(query).skip(skip).limit(_data.pageSize)

    data = []
    for category in categorymenuitems:
        category["_id"] = str(category["_id"])
        data.append(category)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_categorymenuitem(_data: CategoryMenuItems) -> str:
    result = categorymenuitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_categorymenuitem(_data: CategoryMenuItems, categorymenuitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_category = categorymenuitem_collection.find_one({"_id": object_id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="category not found")
    
    updated_category = categorymenuitem_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_category.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_categorymenuitem(category_id: str, categorymenuitem_collection: Collection):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    result = categorymenuitem_collection.delete_one({"_id": ObjectId(category_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="category not found")
    
    return {"message": "category deleted successfully"}
