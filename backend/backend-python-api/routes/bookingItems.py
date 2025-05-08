from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, BookingItems
from service.bookingItems import ser_getbyid_bookingitem,ser_get_bookingitem,ser_delete_bookingitem, ser_insert_bookingitem, ser_update_bookingitem


router = APIRouter()

bookingitem_collection: Collection = database['BookingItems']

@router.get("/bookingitems/get")
async def get_bookingitem():
    return ser_get_bookingitem()

@router.get("/bookingitems/get/{booking_id}")
async def get_bookingitem_by_id(booking_id: str):
    return ser_getbyid_bookingitem(booking_id)

@router.post("/bookingitems/add")
async def create_bookingitem(_data: BookingItems):
    _id = ser_insert_bookingitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/bookingitems/update")
def edit_bookingitem(_data: BookingItems):
    result = ser_update_bookingitem(_data, bookingitem_collection)
    return result

@router.delete("/bookingitems/delete/{bookingitem_id}")
def remove_bookingitem(bookingitem_id: str):
    response = ser_delete_bookingitem(bookingitem_id, bookingitem_collection)
    return response