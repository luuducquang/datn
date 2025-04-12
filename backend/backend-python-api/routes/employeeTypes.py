from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import EmployeeTypes
from service.employeeTypes import ser_get_employeetype,ser_getbyid_employeetype,ser_delete_employeetype, ser_insert_employeetype, ser_update_employeetype


router = APIRouter()

employeetype_collection: Collection = database['EmployeeTypes']

@router.get("/employeetypes/get")
async def get_employeetype():
    return ser_get_employeetype()

@router.get("/employeetypes/get/{employeetype_id}")
async def get_employeetype_by_id(employeetype_id: str):
    return ser_getbyid_employeetype(employeetype_id)

@router.post("/employeetypes/add")
async def create_employeetype(_data: EmployeeTypes):
    _id = ser_insert_employeetype(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/employeetypes/update")
def edit_employeetype(_data: EmployeeTypes):
    result = ser_update_employeetype(_data, employeetype_collection)
    return result

@router.delete("/employeetypes/delete/{employeetype_id}")
def remove_employeetype(employeetype_id: str):
    response = ser_delete_employeetype(employeetype_id, employeetype_collection)
    return response