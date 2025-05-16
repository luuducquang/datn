from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, RateBookings
from config.database import database

ratebooking_collection: Collection = database['RateBookings']
booking_collection: Collection = database['Bookings']
user_collection: Collection = database['Users']
table_collection: Collection = database['Tables']

def ser_get_ratebooking():
    datas = []
    for data in ratebooking_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_ratebooking(ratebooking_id:str):
    if not ObjectId.is_valid(ratebooking_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    ratebooking = ratebooking_collection.find_one({"_id": ObjectId(ratebooking_id)})

    if ratebooking is None:
        raise HTTPException(status_code=404, detail="ratebooking not found")

    ratebooking["_id"] = str(ratebooking["_id"])
    return ratebooking

def ser_getby_booking_id(booking_id: str):
    ratebooking = ratebooking_collection.find_one({"booking_id": booking_id})

    if ratebooking is not None:
        ratebooking["_id"] = str(ratebooking["_id"])

    return ratebooking  

# def ser_getby_booking_id(booking_id: str):
#     ratebookings = list(ratebooking_collection.find({"booking_id": booking_id}))

#     if not ratebookings:
#         raise HTTPException(status_code=404, detail="No RateBookings found with given booking_id")

#     for rb in ratebookings:
#         rb["_id"] = str(rb["_id"])

#     return ratebookings


def ser_search_ratebooking(_data: Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"text": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = ratebooking_collection.count_documents(query)
    ratebookings = ratebooking_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for ratebooking in ratebookings:
        ratebooking["_id"] = str(ratebooking["_id"])

        booking = booking_collection.find_one({"_id": ObjectId(ratebooking["booking_id"])})
        if booking:
            booking["_id"] = str(booking["_id"])

            table = table_collection.find_one({"_id": ObjectId(booking["table_id"])})
            if table:
                table["_id"] = str(table["_id"])
                booking["table"] = table
            else:
                booking["table"] = None

            ratebooking["booking"] = booking
        else:
            ratebooking["booking"] = None

        user = user_collection.find_one({"_id": ObjectId(ratebooking["user_id"])}, {"fullname": 1, "phone": 1})
        if user:
            user["_id"] = str(user["_id"])
            ratebooking["user"] = user
        else:
            ratebooking["user"] = None

        data.append(ratebooking)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }


def ser_insert_ratebooking(_data: RateBookings) -> str:
    result = ratebooking_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_ratebooking(_data: RateBookings, ratebooking_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_ratebooking = ratebooking_collection.find_one({"_id": object_id})
    if not existing_ratebooking:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    updated_ratebooking = ratebooking_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_ratebooking.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_ratebooking(ratebooking_id: str, ratebooking_collection: Collection):
    if not ObjectId.is_valid(ratebooking_id):
        raise HTTPException(status_code=400, detail="Invalid tableType ID")

    result = ratebooking_collection.delete_one({"_id": ObjectId(ratebooking_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    return {"message": "tableType deleted successfully"}
