from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import EmployeePayments
from config.database import database

employeepayment_collection: Collection = database['EmployeePayments']

def ser_get_employeepayment():
    datas = []
    for data in employeepayment_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_employeepayment(_data: EmployeePayments) -> str:
    result = employeepayment_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_employeepayment(_data: EmployeePayments, employeepayment_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_employeepayment = employeepayment_collection.find_one({"_id": object_id})
    if not existing_employeepayment:
        raise HTTPException(status_code=404, detail="employeepayment not found")
    
    updated_employeepayment = employeepayment_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_employeepayment.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_employeepayment(employeepayment_id: str, employeepayment_collection: Collection):
    if not ObjectId.is_valid(employeepayment_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")

    result = employeepayment_collection.delete_one({"_id": ObjectId(employeepayment_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="employeepayment not found")
    
    return {"message": "employee deleted successfully"}
