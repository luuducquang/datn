from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import TableRentalItems
from service.tablerentalitems import ser_delete_rentalitem,ser_get_tablerentalitem,ser_getbyid_table_tablerentalitem,ser_delete_table_rentalitem, ser_insert_table_rentalitem, ser_update_table_rentalitem


router = APIRouter()

rentalitem_collection: Collection = database['TableRentalItems']

@router.get("/tablerentalitems/get")
async def get_tablerentalitem():
    return ser_get_tablerentalitem()

@router.get("/tablerentalitems/get/{table_id}")
async def get_tablerentalitem_by_id_table(table_id: str):
    return ser_getbyid_table_tablerentalitem(table_id)

@router.post("/tablerentalitems/add")
async def create_tablerentalitem(_data: TableRentalItems):
    _id = ser_insert_table_rentalitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/tablerentalitems/update")
def edit_tablerentalitem(_data: TableRentalItems):
    result = ser_update_table_rentalitem(_data, rentalitem_collection)
    return result

@router.delete("/tablerentalitems/delete/{table_id}")
def remove_tablerentalitem(table_id: str):
    response = ser_delete_table_rentalitem(table_id, rentalitem_collection)
    return response

@router.delete("/tablerentalitems/deleteitem/{id}")
def remove_rentalitem(id: str):
    response = ser_delete_rentalitem(id, rentalitem_collection)
    return response