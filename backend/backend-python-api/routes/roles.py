from fastapi import APIRouter, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Roles
from service.roles import ser_get_roles,ser_delete_role, ser_insert_role,ser_update_role
from bson import ObjectId


router = APIRouter()

role_collection: Collection = database['Roles']

@router.get("/roles/get")
async def get_roles():
    return ser_get_roles()

@router.get("/roles/get/{role_id}")
async def get_role_by_id(role_id: str):
    if not ObjectId.is_valid(role_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    role = role_collection.find_one({"_id": ObjectId(role_id)})

    if role is None:
        raise HTTPException(status_code=404, detail="role not found")

    role["_id"] = str(role["_id"])
    return role

@router.post("/roles/add")
def create_role(_data: Roles):
    _id = ser_insert_role(_data, role_collection)
    return {"message": "Role created successfully", "_id": _id}

@router.put("/roles/update")
def edit_role(_data: Roles):
    result = ser_update_role(_data, role_collection)
    return result

@router.delete("/roles/delete/{role_id}")
def remove_role(role_id: str):
    response = ser_delete_role(role_id, role_collection)
    return response


