from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import EmployeeTypes
from config.database import database

employeetype_collection: Collection = database['EmployeeTypes']

def ser_get_employeetype():
    datas = []
    for data in employeetype_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_employeetype(employeetype_id:str):
    if not ObjectId.is_valid(employeetype_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    employeetype = employeetype_collection.find_one({"_id": ObjectId(employeetype_id)})

    if employeetype is None:
        raise HTTPException(status_code=404, detail="employeetype not found")

    employeetype["_id"] = str(employeetype["_id"])
    return employeetype

def ser_insert_employeetype(_data: EmployeeTypes) -> str:
    result = employeetype_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_employeetype(_data: EmployeeTypes, employeetype_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_employeetype = employeetype_collection.find_one({"_id": object_id})
    if not existing_employeetype:
        raise HTTPException(status_code=404, detail="employeeType not found")
    
    updated_employeetype = employeetype_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_employeetype.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_employeetype(employeetype_id: str, employeetype_collection: Collection):
    if not ObjectId.is_valid(employeetype_id):
        raise HTTPException(status_code=400, detail="Invalid employeeType ID")

    result = employeetype_collection.delete_one({"_id": ObjectId(employeetype_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="employeeType not found")
    
    return {"message": "employeeType deleted successfully"}
