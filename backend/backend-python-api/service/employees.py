from bson import ObjectId
from fastapi import HTTPException
from bson import ObjectId,errors
from pymongo.collection import Collection
from schemas.schemas import Employees, Searchs
from config.database import database

employee_collection: Collection = database['Employees']
user_collection: Collection = database['Users']

def ser_get_employee():
    datas = []
    for employee in employee_collection.find():
        try:
            user_id = ObjectId(employee["user_id"])
        except (errors.InvalidId, KeyError):
            user_data = None
        else:
            user_data = user_collection.find_one({"_id": user_id})
        employee["_id"] = str(employee["_id"])
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            employee["user_info"] = user_data
        else:
            employee["user_info"] = {}
        datas.append(employee)
    return datas

def ser_getbyid_employee(employee_id:str):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    employee = employee_collection.find_one({"_id": ObjectId(employee_id)})

    if employee is None:
        raise HTTPException(status_code=404, detail="employee not found")
    user_id = ObjectId(employee["user_id"])
    user_data = user_collection.find_one({"_id": user_id})
    employee["_id"] = str(employee["_id"])
    if user_data:
            user_data["_id"] = str(user_data["_id"])
            employee["user_info"] = user_data
    else:
        employee["user_info"] = {}
    return employee

def ser_search_employee(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    user_query = {}
    if _data.search_term:
        user_query["$or"] = [
            {"username": {"$regex": _data.search_term, "$options": "i"}},
            {"fullname": {"$regex": _data.search_term, "$options": "i"}},
            {"email": {"$regex": _data.search_term, "$options": "i"}},
            {"phone": {"$regex": _data.search_term, "$options": "i"}}
        ]

    users = user_collection.find(user_query)
    user_ids = [str(user["_id"]) for user in users]

    if not user_ids:
        return {
            "page": _data.page,
            "pageSize": _data.pageSize,
            "totalItems": 0,
            "data": []
        }

    employee_query = {"user_id": {"$in": user_ids}}

    total_items = employee_collection.count_documents(employee_query)

    employees = employee_collection.find(employee_query).skip(skip).limit(_data.pageSize)

    data = []
    for employee in employees:
        employee["_id"] = str(employee["_id"])
        user = user_collection.find_one({"_id": ObjectId(employee["user_id"])})
        user["_id"] = str(user["_id"])
        if user:
            employee["user_info"] = user
        data.append(employee)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_employee(_data: Employees) -> str:
    result = employee_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_employee(_data: Employees, employee_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_employee = employee_collection.find_one({"_id": object_id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="employee not found")
    
    updated_employee = employee_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_employee.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_employee(employee_id: str, employee_collection: Collection):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")

    result = employee_collection.delete_one({"_id": ObjectId(employee_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="employee not found")
    
    return {"message": "employee deleted successfully"}
