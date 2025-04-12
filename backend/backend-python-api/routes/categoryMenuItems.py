from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import CategoryMenuItems, Searchs
from service.categoryMenuItems import ser_getbyid_categorymenuitem,ser_get_category,ser_search_categorymenuitem,ser_delete_categorymenuitem, ser_insert_categorymenuitem, ser_update_categorymenuitem


router = APIRouter()

categorymenuitem_collection: Collection = database['CategoryMenuItems']

@router.get("/categorymenuitems/get")
async def get_category():
    return ser_get_category()

@router.get("/categorymenuitems/get/{category_id}")
async def get_category_by_id(category_id: str):
    return ser_getbyid_categorymenuitem(category_id)

@router.post("/categorymenuitems/search")
async def search_category(_data:Searchs):
    return ser_search_categorymenuitem(_data)

@router.post("/categorymenuitems/add")
async def create_category(_data: CategoryMenuItems):
    _id = ser_insert_categorymenuitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/categorymenuitems/update")
def edit_category(_data: CategoryMenuItems):
    result = ser_update_categorymenuitem(_data, categorymenuitem_collection)
    return result

@router.delete("/categorymenuitems/delete/{category_id}")
def remove_category(category_id: str):
    response = ser_delete_categorymenuitem(category_id, categorymenuitem_collection)
    return response