from datetime import datetime, timedelta, timezone
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Bookings, Searchs
from config.database import database

booking_collection: Collection = database['Bookings']
table_collection: Collection = database['Tables']

def ser_get_booking():
    datas = []
    for data in booking_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas


async def ser_check_availability_booking(
    table_id: str,
    start_time: datetime,
    end_time: datetime,
    booking_collection
):
    if not ObjectId.is_valid(table_id):
        raise HTTPException(status_code=400, detail="Invalid table ID")
    
    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Start time must be earlier than end time")
    
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    start_time = start_time.replace(tzinfo=None)  
    end_time = end_time.replace(tzinfo=None)    

    try:
        conflict_count = booking_collection.count_documents({
            "table_id": table_id,
            "status": True,
            "$and": [
                {"start_time": {"$lt": end_time}}, 
                {"end_time": {"$gt": start_time}}   
            ]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    
    return conflict_count == 0


def ser_search_booking(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"name": {"$regex": _data.search_term, "$options": "i"}},
            {"phone": {"$regex": _data.search_term, "$options": "i"}},
            {"status": {"$regex": _data.search_term, "$options": "i"}},
        ]
    
    if _data.status is not None: 
        query["status"] = _data.status

    total_items = booking_collection.count_documents(query)

    bookings = booking_collection.find(query).skip(skip).limit(_data.pageSize)

    data = []
    for booking in bookings:
        booking["_id"] = str(booking["_id"])

        table_id = ObjectId(booking["table_id"])

        table_data = table_collection.find_one({"_id": table_id})
        if table_data:
            table_data["_id"] = str(table_data["_id"])  
            booking["table"] = table_data  
        else:
            booking["table"] = None  

        data.append(booking)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_booking(_data: Bookings) -> str:
    booking_data = _data.dict(exclude={"id"})
    
    if isinstance(booking_data.get("start_time"), datetime):
        booking_data["start_time"] = booking_data["start_time"].isoformat()
    elif not isinstance(booking_data.get("start_time"), str):
        raise HTTPException(status_code=400, detail="Start time is required and must be a valid ISO 8601 string.")
    
    if isinstance(booking_data.get("end_time"), datetime):
        booking_data["end_time"] = booking_data["end_time"].isoformat()
    elif not isinstance(booking_data.get("end_time"), str):
        raise HTTPException(status_code=400, detail="End time is required and must be a valid ISO 8601 string.")
    
    try:
        start_time = datetime.fromisoformat(booking_data["start_time"])
    except ValueError:
        raise HTTPException(status_code=400, detail="Start time format is invalid. Must be ISO 8601 format.")
    
    start_time = start_time.replace(tzinfo=timezone.utc)  

    vietnam_now = datetime.now(timezone.utc) + timedelta(hours=7)

    if start_time < vietnam_now + timedelta(minutes=29):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian bắt đầu sau hiện tại 30 phút để chúng tôi chuẩn bị")
    
    try:
        end_time = datetime.fromisoformat(booking_data["end_time"])
    except ValueError:
        raise HTTPException(status_code=400, detail="End time format is invalid. Must be ISO 8601 format.")
    
    end_time = end_time.replace(tzinfo=timezone.utc)

    if end_time <= start_time + timedelta(minutes=30):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian kết thúc sau thời gian bắt đầu ít nhất 30 phút.")
    
    booking_data["created_at"] = vietnam_now

    result = booking_collection.insert_one(booking_data)
    return str(result.inserted_id)


def ser_update_booking(_data: Bookings, booking_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_booking = booking_collection.find_one({"_id": object_id})
    if not existing_booking:
        raise HTTPException(status_code=404, detail="booking not found")
    
    updated_booking = booking_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_booking.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_booking(booking_id: str, booking_collection: Collection):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    result = booking_collection.delete_one({"_id": ObjectId(booking_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="booking not found")
    
    return {"message": "booking deleted successfully"}

def ser_update_booking_status(booking_id: str, booking_collection: Collection):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    result = booking_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": False}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found or status already false")
    
    return {"message": "Booking status updated to false successfully"}