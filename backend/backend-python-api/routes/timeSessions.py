from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import TimeSessions
from service.timeSessions import ser_get_timesession,ser_delete_timesession, ser_insert_timesession, ser_update_timesession


router = APIRouter()

timesession_collection: Collection = database['TimeSessions']

@router.get("/timesessions/get")
async def get_timesession():
    return ser_get_timesession()

@router.post("/timesessions/add")
async def create_timesession(_data: TimeSessions):
    _id = ser_insert_timesession(_data)
    return  _id

@router.put("/timesessions/update")
def edit_timesession(_data: TimeSessions):
    result = ser_update_timesession(_data, timesession_collection)
    return result

@router.delete("/timesessions/delete/{timesession_id}")
def remove_timesession(timesession_id: str):
    response = ser_delete_timesession(timesession_id, timesession_collection)
    return response