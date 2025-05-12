from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, Discounts
from service.discounts import ser_restore_discount_by_code,ser_use_discount_by_code,ser_get_discount_by_code,ser_getbyid_discount,ser_search_discount,ser_get_discount,ser_delete_discount, ser_insert_discount, ser_update_discount


router = APIRouter()

discount_collection: Collection = database['Discounts']

@router.get("/discounts/get")
async def get_discount():
    return ser_get_discount()

@router.get("/discounts/get/{discount_id}")
async def get_discount_by_id(discount_id: str):
    return ser_getbyid_discount(discount_id)

@router.get("/discounts/code/{code}", response_model=int)
async def get_discount_by_code(code: str):
    return ser_get_discount_by_code(code)

@router.post("/discounts/use/{code}")
async def use_discount_by_code(code: str):
    return ser_use_discount_by_code(code)

@router.post("/discounts/restore/{code}")
async def use_discount_by_restore_code(code: str):
    return ser_restore_discount_by_code(code)

@router.post("/discounts/search")
async def search_discount(_data:Searchs):
    return ser_search_discount(_data)

@router.post("/discounts/add")
async def create_discount(_data: Discounts):
    _id = ser_insert_discount(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/discounts/update")
def edit_discount(_data: Discounts):
    result = ser_update_discount(_data, discount_collection)
    return result

@router.delete("/discounts/delete/{discount_id}")
def remove_discount(discount_id: str):
    response = ser_delete_discount(discount_id, discount_collection)
    return response