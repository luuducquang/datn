from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Banners, Searchs
from bson import ObjectId
from config.database import database

banner_collection: Collection = database['Banners']

def ser_get_banners():
    datas = []
    for data in banner_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_banner(_data: Banners, banner_collection: Collection):
    
    result = banner_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)


def ser_search_banner(_data: Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    total_items = banner_collection.count_documents({})  # Bỏ query, trả về tổng số tài liệu

    banners = banner_collection.find({}).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for banner in banners:
        banner["_id"] = str(banner["_id"])
        data.append(banner)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_update_banner(_data: Banners, banner_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    updated_banner = banner_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_banner.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_banner(banner_id: str, banner_collection: Collection):
    if not ObjectId.is_valid(banner_id):
        raise HTTPException(status_code=400, detail="Invalid banner ID")

    result = banner_collection.delete_one({"_id": ObjectId(banner_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="not found")
    
    return {"message": "deleted successfully"}
