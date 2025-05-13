from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import CategoryProducts, Searchs
from service.categoryProducts import ser_get_category,ser_getbyid_categoryproduct,ser_search_categoryproduct,ser_delete_categoryproduct, ser_insert_categoryproduct, ser_update_categoryproduct


router = APIRouter()

categoryproduct_collection: Collection = database['CategoryProducts']

@router.get("/categoryproducts/get")
async def get_category():
    return ser_get_category()

@router.get("/categoryproducts/get/{category_id}")
async def get_category_by_id(category_id: str):
    return ser_getbyid_categoryproduct(category_id)

@router.post("/categoryproducts/search")
async def search_category(_data:Searchs):
    return ser_search_categoryproduct(_data)

@router.post("/categoryproducts/add")
async def create_category(_data: CategoryProducts):
    _id = ser_insert_categoryproduct(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/categoryproducts/update")
def edit_category(_data: CategoryProducts):
    result = ser_update_categoryproduct(_data, categoryproduct_collection)
    return result

@router.delete("/categoryproducts/delete/{category_id}")
def remove_category(category_id: str):
    response = ser_delete_categoryproduct(category_id, categoryproduct_collection)
    return response