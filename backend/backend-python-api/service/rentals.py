from typing import List
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Rentals
from config.database import database

rental_collection: Collection = database['Rentals']

def ser_get_rental():
    datas = []
    for data in rental_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_rentals(_data: List[Rentals]) -> List[str]:
    rentals_to_insert = [rental.dict(exclude={"id"}) for rental in _data]
    
    result = rental_collection.insert_many(rentals_to_insert)
    
    return [str(inserted_id) for inserted_id in result.inserted_ids]

def ser_update_rental(_data: Rentals, rental_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_rental = rental_collection.find_one({"_id": object_id})
    if not existing_rental:
        raise HTTPException(status_code=404, detail="rental not found")
    
    updated_rental = rental_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_rental.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_rental(rental_id: str, rental_collection: Collection):
    if not ObjectId.is_valid(rental_id):
        raise HTTPException(status_code=400, detail="Invalid rental ID")

    result = rental_collection.delete_one({"_id": ObjectId(rental_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="rental not found")
    
    return {"message": "rental deleted successfully"}
