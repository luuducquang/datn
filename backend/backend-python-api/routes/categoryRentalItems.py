from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import CategoryRentalItems, Searchs
from service.categoryRentalItems import ser_get_category,ser_getbyid_categoryrentalitem,ser_search_categoryrentalitem,ser_delete_categoryrentalitem, ser_insert_categoryrentalitem, ser_update_categoryrentalitem


router = APIRouter()

categoryrentalitem_collection: Collection = database['CategoryRentalItems']

@router.get("/categoryrentalitems/get")
async def get_category():
    return ser_get_category()

@router.get("/categoryrentalitems/get/{category_id}")
async def get_category_by_id(category_id: str):
    return ser_getbyid_categoryrentalitem(category_id)

@router.post("/categoryrentalitems/search")
async def search_category(_data:Searchs):
    return ser_search_categoryrentalitem(_data)

@router.post("/categoryrentalitems/add")
async def create_category(_data: CategoryRentalItems):
    _id = ser_insert_categoryrentalitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/categoryrentalitems/update")
def edit_category(_data: CategoryRentalItems):
    result = ser_update_categoryrentalitem(_data, categoryrentalitem_collection)
    return result

@router.delete("/categoryrentalitems/delete/{category_id}")
def remove_category(category_id: str):
    response = ser_delete_categoryrentalitem(category_id, categoryrentalitem_collection)
    return response