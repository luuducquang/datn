from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Shifts
from service.shifts import ser_get_shift,ser_delete_shift, ser_insert_shift, ser_update_shift


router = APIRouter()

shift_collection: Collection = database['Shifts']

@router.get("/shifts/get")
async def get_shift():
    return ser_get_shift()

@router.post("/shifts/add")
async def create_shift(_data: Shifts):
    _id = ser_insert_shift(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/shifts/update")
def edit_shift(_data: Shifts):
    result = ser_update_shift(_data, shift_collection)
    return result

@router.delete("/shifts/delete/{shift_id}")
def remove_shift(shift_id: str):
    response = ser_delete_shift(shift_id, shift_collection)
    return response