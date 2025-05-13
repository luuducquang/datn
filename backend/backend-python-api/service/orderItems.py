from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import OrderItems
from config.database import database

foodorder_collection: Collection = database['OrderItems']

def ser_get_foodorder():
    datas = []
    for data in foodorder_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_foodorder(_data: OrderItems) -> str:
    result = foodorder_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_foodorder(_data: OrderItems, foodorder_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_foodorder = foodorder_collection.find_one({"_id": object_id})
    if not existing_foodorder:
        raise HTTPException(status_code=404, detail="foodorder not found")
    
    updated_foodorder = foodorder_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_foodorder.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_foodorder(foodorder_id: str, foodorder_collection: Collection):
    if not ObjectId.is_valid(foodorder_id):
        raise HTTPException(status_code=400, detail="Invalid foodorder ID")

    result = foodorder_collection.delete_one({"_id": ObjectId(foodorder_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="foodorder not found")
    
    return {"message": "foodorder deleted successfully"}
