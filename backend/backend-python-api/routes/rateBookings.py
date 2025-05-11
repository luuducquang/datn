from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, RateBookings
from service.rateBookings import ser_getby_booking_id,ser_getbyid_ratebooking,ser_search_ratebooking,ser_get_ratebooking,ser_delete_ratebooking, ser_insert_ratebooking, ser_update_ratebooking


router = APIRouter()

ratebooking_collection: Collection = database['RateBookings']

@router.get("/ratebookings/get")
async def get_ratebooking():
    return ser_get_ratebooking()

@router.get("/ratebookings/get/{ratebooking_id}")
async def get_ratebooking_by_id(ratebooking_id: str):
    return ser_getbyid_ratebooking(ratebooking_id)

@router.get("/ratebookings/booking/{booking_id}")
async def get_ratebooking_by_booking_id(booking_id: str):
    return ser_getby_booking_id(booking_id)

@router.post("/ratebookings/search")
async def search_ratebooking(_data:Searchs):
    return ser_search_ratebooking(_data)

@router.post("/ratebookings/add")
async def create_ratebooking(_data: RateBookings):
    _id = ser_insert_ratebooking(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/ratebookings/update")
def edit_ratebooking(_data: RateBookings):
    result = ser_update_ratebooking(_data, ratebooking_collection)
    return result

@router.delete("/ratebookings/delete/{ratebooking_id}")
def remove_ratebooking(ratebooking_id: str):
    response = ser_delete_ratebooking(ratebooking_id, ratebooking_collection)
    return response