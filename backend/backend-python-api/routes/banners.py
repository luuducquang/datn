from fastapi import APIRouter, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Banners, Searchs
from service.banners import ser_get_banners,ser_delete_banner, ser_insert_banner,ser_update_banner,ser_search_banner
from bson import ObjectId


router = APIRouter()

banner_collection: Collection = database['Banners']

@router.get("/banners/get")
async def get_banners():
    return ser_get_banners()

@router.get("/banners/get/{banner_id}")
async def get_banner_by_id(banner_id: str):
    if not ObjectId.is_valid(banner_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    banner = banner_collection.find_one({"_id": ObjectId(banner_id)})

    if banner is None:
        raise HTTPException(status_code=404, detail="banner not found")

    banner["_id"] = str(banner["_id"])
    return banner

@router.post("/banners/search")
async def search_banner(_data:Searchs):
    return ser_search_banner(_data)

@router.post("/banners/add")
def create_banner(_data: Banners):
    _id = ser_insert_banner(_data, banner_collection)
    return {"message": "banner created successfully", "_id": _id}

@router.put("/banners/update")
def edit_banner(_data: Banners):
    result = ser_update_banner(_data, banner_collection)
    return result

@router.delete("/banners/delete/{banner_id}")
def remove_banner(banner_id: str):
    response = ser_delete_banner(banner_id, banner_collection)
    return response


