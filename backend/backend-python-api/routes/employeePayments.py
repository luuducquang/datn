from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import EmployeePayments
from service.employeePayments import ser_get_employeepayment,ser_delete_employeepayment, ser_insert_employeepayment, ser_update_employeepayment


router = APIRouter()

employeepayment_collection: Collection = database['EmployeePayments']

@router.get("/employeepayments/get")
async def get_employeepayment():
    return ser_get_employeepayment()

@router.post("/employeepayments/add")
async def create_employeepayment(_data: EmployeePayments):
    _id = ser_insert_employeepayment(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/employeepayments/update")
def edit_employee(_data: EmployeePayments):
    result = ser_update_employeepayment(_data, employeepayment_collection)
    return result

@router.delete("/employeepayments/delete/{employeepayment_id}")
def remove_employee(employeepayment_id: str):
    response = ser_delete_employeepayment(employeepayment_id, employeepayment_collection)
    return response