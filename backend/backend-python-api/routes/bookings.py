from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException, Query
from pymongo.collection import Collection
from config.database import database
from datetime import datetime
from schemas.schemas import Bookings, Searchs
from service.bookings import find_available_table,get_active_bookings_service,ser_get_booking_by_id,ser_get_booking_by_user_id,ser_update_booking_status_service,ser_get_booking_by_table,ser_get_booking,ser_search_booking,ser_delete_booking, ser_insert_booking, ser_update_booking,ser_check_availability_booking,ser_update_booking_status


router = APIRouter()

booking_collection: Collection = database['Bookings']
tables_collection: Collection = database['Tables']

@router.get("/bookings/get")
async def get_booking():
    return ser_get_booking()

@router.get("/bookings/get-by-id/{booking_id}")
async def get_booking_by_id(booking_id: str):
    return ser_get_booking_by_id(booking_id)

@router.get("/bookings/get-by-table/{table_id}")
async def get_booking_by_table(table_id: str):
    return ser_get_booking_by_table(table_id)

@router.get("/bookings/get-booking-by-userid/{user_id}")
async def get_booking_by_user_id(user_id: str):
    return ser_get_booking_by_user_id(user_id)

@router.get("/bookings/get-booking-active")
async def get_active_bookings():
    return get_active_bookings_service()

@router.put("/bookings/update-status/{booking_id}")
async def update_booking_status(booking_id: str):
    return ser_update_booking_status_service(booking_id)

@router.post("/bookings/check-availability-booking")
async def check_availability_booking(
    table_id: str = Body(...),
    start_time: datetime = Body(...),
    end_time: datetime = Body(...),
):
    return await ser_check_availability_booking(table_id, start_time, end_time, booking_collection)

@router.post("/bookings/search")
async def search_booking(_data:Searchs):
    return ser_search_booking(_data)

@router.post("/bookings/add")
async def create_booking(_data: Bookings):
    _id = ser_insert_booking(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/bookings/update")
def edit_booking(_data: Bookings):
    result = ser_update_booking(_data, booking_collection)
    return result

@router.delete("/bookings/delete/{booking_id}")
def remove_booking(booking_id: str):
    response = ser_delete_booking(booking_id, booking_collection)
    return response

@router.put("/bookings/false-status/{booking_id}")
def update_booking_status(booking_id: str):
    response = ser_update_booking_status(booking_id, booking_collection)
    return response

@router.post("/bookings/available")
def get_available_table(
    start_time: datetime = Body(...),
    end_time: datetime = Body(...)
):
    table_id = find_available_table(
        start_time.isoformat(),
        end_time.isoformat(),
        tables_collection,
        booking_collection
    )
    return  table_id