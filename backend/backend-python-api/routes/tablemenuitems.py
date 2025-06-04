from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import TableMenuItems, TableTransferRequest
from service.tablemenuitems import transfer_table_items_service,ser_delete_menuitem,ser_get_tablemenuitem,ser_getbyid_table_tablemenuitem,ser_delete_table_menuitem, ser_insert_table_menuitem, ser_update_table_menuitem


router = APIRouter()

tablemenuitem_collection: Collection = database['TableMenuItems']
menuitem_collection: Collection = database['MenuItems']

@router.get("/tablemenuitems/get")
async def get_tablemenuitem():
    return ser_get_tablemenuitem()

@router.get("/tablemenuitems/get/{table_id}")
async def get_tablemenuitem_by_id_table(table_id: str):
    return ser_getbyid_table_tablemenuitem(table_id)

@router.post("/tablemenuitems/add")
async def create_tablemenuitem(_data: TableMenuItems):
    _id = ser_insert_table_menuitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/tablemenuitems/update")
def edit_tablemenuitem(_data: TableMenuItems):
    result = ser_update_table_menuitem(_data, tablemenuitem_collection,menuitem_collection)
    return result

@router.delete("/tablemenuitems/deletes/{table_id}")
def remove_tablemenuitem(table_id: str):
    response = ser_delete_table_menuitem(table_id, tablemenuitem_collection)
    return response

@router.delete("/tablemenuitems/deleteitem/{id}")
def remove_menuitem(id: str):
    response = ser_delete_menuitem(id, tablemenuitem_collection, menuitem_collection)
    return response

@router.put("/tablemenuitems/transfer")
def transfer_table_items(data: TableTransferRequest):
    return transfer_table_items_service(
        data.old_table_id,
        data.new_table_id,
        tablemenuitem_collection
    )