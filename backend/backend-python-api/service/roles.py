from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Roles
from bson import ObjectId
from config.database import database

role_collection: Collection = database['Roles']

def ser_get_roles():
    datas = []
    for data in role_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_role(_data: Roles, role_collection: Collection):
    existing_role = role_collection.find_one({"role_name": {"$regex": f"^{_data.role_name}$", "$options": "i"}})
    
    if existing_role:
        raise HTTPException(status_code=400, detail=f"Role with name '{_data.role_name}' already exists.")
    
    result = role_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)


def ser_update_role(_data: Roles, role_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_role = role_collection.find_one({"_id": object_id})
    if not existing_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if _data.role_name:
        duplicate_role = role_collection.find_one({
            "role_name": _data.role_name,
            "_id": {"$ne": object_id} 
        })
        if duplicate_role:
            raise HTTPException(status_code=400, detail="Role name already exists")
    
    updated_role = role_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_role.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_role(role_id: str, role_collection: Collection):
    if not ObjectId.is_valid(role_id):
        raise HTTPException(status_code=400, detail="Invalid role ID")

    result = role_collection.delete_one({"_id": ObjectId(role_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="not found")
    
    return {"message": "deleted successfully"}
