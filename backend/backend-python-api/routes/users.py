from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, Users
from service.users import ser_get_user_by_id, ser_get_users,ser_delete_user, ser_insert_user, ser_search_user, ser_update_user
from sercurity import validate_token


router = APIRouter()
# dependencies=[Depends(validate_token)]

user_collection: Collection = database['Users']

@router.get("/users/get")
async def get_users():
    return ser_get_users()

@router.get("/users/get/{user_id}")
async def get_user_by_id(user_id: str):
    return ser_get_user_by_id(user_id)

@router.post("/users/search")
async def search_user(_data:Searchs):
    return ser_search_user(_data)

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