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

def ser_get_booking_by_id(booking_id: str):
    try:
        data = booking_collection.find_one({"_id": ObjectId(booking_id)})
        if not data:
            raise HTTPException(status_code=404, detail="Không tìm thấy booking")
        data["_id"] = str(data["_id"])
        return data
    except Exception:
        raise HTTPException(status_code=400, detail="ID không hợp lệ")

def ser_get_booking_by_table(table_id: str):
    datas = []
    now = datetime.now()
    query = {
        "table_id": table_id,
        "status": True,
        "end_time": {"$gte": now}
    }
    for data in booking_collection.find(query):
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_booking_by_user_id(user_id: str):
    datas = []
    now = datetime.now()
    query = {
        "user_id": user_id,
    }
    for data in booking_collection.find(query):
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas


def get_active_bookings_service():
    now = datetime.now()

    bookings = booking_collection.find({"status": True}).sort("start_time", 1)

    data = []
    for booking in bookings:
        end_time_value = booking.get("end_time")
        start_time_value = booking.get("start_time")

        if isinstance(end_time_value, str):
            booking_end_time = datetime.fromisoformat(end_time_value)
        elif isinstance(end_time_value, datetime):
            booking_end_time = end_time_value
        else:
            continue

        booking_end_time = booking_end_time.replace(tzinfo=None)

        if isinstance(start_time_value, str):
            booking_start_time = datetime.fromisoformat(start_time_value)
        elif isinstance(start_time_value, datetime):
            booking_start_time = start_time_value
        else:
            continue

        booking_start_time = booking_start_time.replace(tzinfo=None)

        if booking_end_time >= now:
            booking["_id"] = str(booking["_id"])

            table_id = ObjectId(booking["table_id"])
            table_data = table_collection.find_one({"_id": table_id})
            if table_data:
                table_data["_id"] = str(table_data["_id"])  
                booking["table"] = table_data  
            else:
                booking["table"] = None  


            data.append(booking)

    return data

def ser_update_booking_status_service(booking_id: str):
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID")

    booking = booking_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    new_status = not booking.get("status", False)

    result = booking_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": new_status}}
    )

    if result.modified_count == 1:
        return {"message": "Status updated", "new_status": new_status}
    else:
        raise HTTPException(status_code=500, detail="Failed to update status")
    

async def ser_check_availability_booking(
    table_id: str,
    start_time: datetime,
    end_time: datetime,
    booking_collection
):
    if not table_id:
        raise HTTPException(status_code=400, detail="Invalid table ID")

    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    start_time = start_time.replace(tzinfo=None)
    end_time = end_time.replace(tzinfo=None)

    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Start time must be earlier than end time")

    try:
        conflict_count = booking_collection.count_documents({
            "table_id": table_id,  
            "status": True,
            "$and": [
                {"start_time": {"$lt": end_time}},
                {"end_time": {"$gt": start_time}}
            ]
        })
        print(f"[DEBUG] conflict_count: {conflict_count}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
    query = {
        "table_id": table_id,
        "status": True,
        "$and": [
            {"start_time": {"$lt": end_time}},
            {"end_time": {"$gt": start_time}}
        ]
    }
    print("[DEBUG QUERY]", query)
    print(booking_collection.find_one({}))
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

    bookings = booking_collection.find(query).sort("_id", -1).sort("_id", -1).skip(skip).limit(_data.pageSize)

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
    
    if isinstance(booking_data.get("start_time"), datetime) and isinstance(booking_data.get("end_time"), datetime):
        start_time = booking_data["start_time"]
        end_time = booking_data["end_time"]
    else:
        raise HTTPException(status_code=400, detail="Start time and End time must be valid datetime objects.")
    
    vietnam_now = datetime.now()
    
    if start_time < vietnam_now + timedelta(minutes=0):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian bắt đầu sau hiện tại.")
    
    if end_time <= start_time + timedelta(minutes=0):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian kết thúc sau thời gian bắt đầu ít nhất 1 phút.")
    
    booking_data["created_at"] = vietnam_now
    
    try:
        result = booking_collection.insert_one(booking_data)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting booking: {e}")


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


def find_available_table(start_time, end_time, tables_collection, booking_collection) -> str:
    try:
        start_dt = datetime.fromisoformat(start_time).replace(tzinfo=None)
        end_dt = datetime.fromisoformat(end_time).replace(tzinfo=None)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    if start_dt >= end_dt:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    all_tables = list(tables_collection.find({}, {"_id": 1}))  
    print("all_tables:", all_tables)
    all_table_ids = [str(t["_id"]) for t in all_tables if "_id" in t]

    if not all_table_ids:
        raise HTTPException(status_code=404, detail="No tables found")

    booked_tables = list(booking_collection.find({
        "status": True,
        "$and": [
            {"start_time": {"$lt": end_dt}},
            {"end_time": {"$gt": start_dt}}
        ]
    }, {"_id": 0, "table_id": 1}))

    booked_table_ids = [b["table_id"] for b in booked_tables]

    available_table_ids = [tid for tid in all_table_ids if tid not in booked_table_ids]

    if not available_table_ids:
        raise HTTPException(status_code=404, detail="No available table found")

    return available_table_ids[0]