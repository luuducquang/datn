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
    # Không cần ObjectId nếu table_id trong DB là string
    if not table_id:
        raise HTTPException(status_code=400, detail="Invalid table ID")

    # Parse thời gian nếu là string
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    # Bỏ timezone
    start_time = start_time.replace(tzinfo=None)
    end_time = end_time.replace(tzinfo=None)

    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="Start time must be earlier than end time")

    try:
        conflict_count = booking_collection.count_documents({
            "table_id": table_id,  # giữ nguyên kiểu string
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
    
    # Giữ nguyên start_time và end_time dưới dạng datetime
    if isinstance(booking_data.get("start_time"), datetime) and isinstance(booking_data.get("end_time"), datetime):
        # Không cần phải chuyển đổi thành chuỗi ISO 8601
        start_time = booking_data["start_time"]
        end_time = booking_data["end_time"]
    else:
        raise HTTPException(status_code=400, detail="Start time and End time must be valid datetime objects.")
    
    # Lấy thời gian hiện tại của hệ thống
    vietnam_now = datetime.now()
    
    # Kiểm tra thời gian bắt đầu có cách thời gian hiện tại ít nhất 30 phút không
    if start_time < vietnam_now + timedelta(minutes=30):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian bắt đầu sau hiện tại 30 phút để chúng tôi chuẩn bị.")
    
    # Kiểm tra thời gian kết thúc có ít nhất 30 phút sau thời gian bắt đầu không
    if end_time <= start_time + timedelta(minutes=30):
        raise HTTPException(status_code=400, detail="Vui lòng chọn thời gian kết thúc sau thời gian bắt đầu ít nhất 30 phút.")
    
    # Cập nhật created_at với thời gian hiện tại của hệ thống
    booking_data["created_at"] = vietnam_now
    
    # Lưu booking vào MongoDB
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