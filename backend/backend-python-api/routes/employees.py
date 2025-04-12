from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Employees, Searchs
from service.employees import ser_get_employee,ser_search_employee,ser_getbyid_employee,ser_delete_employee, ser_insert_employee, ser_update_employee


router = APIRouter()

employee_collection: Collection = database['Employees']
user_collection: Collection = database['Users']

@router.get("/employees/get")
async def get_employee():
    return ser_get_employee()


@router.get("/employees/get/{employee_id}")
async def get_employee_by_id(employee_id: str):
    return ser_getbyid_employee(employee_id)

@router.post("/employees/search")
async def search_employee(_data:Searchs):
    return ser_search_employee(_data)


@router.post("/employees/add")
async def create_employee(_data: Employees):
    _id = ser_insert_employee(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/employees/update")
def edit_employee(_data: Employees):
    result = ser_update_employee(_data, employee_collection)
    return result

@router.delete("/employees/delete/{employee_id}")
def remove_employee(employee_id: str):
    response = ser_delete_employee(employee_id, employee_collection)
    return response