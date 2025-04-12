from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, Tables
from service.tables import ser_getbyid_table,ser_search_table,ser_get_table,ser_delete_table, ser_insert_table, ser_update_table,ser_update_tablestatus

from socketio_server import sio

router = APIRouter()


table_collection: Collection = database['Tables']

@router.get("/tables/get")
async def get_table():
    return ser_get_table()

@router.get("/tables/get/{table_id}")
async def get_table_by_id(table_id: str):
    result =  ser_getbyid_table(table_id)
    return result

@router.post("/tables/search")
async def search_table(_data:Searchs):
    return ser_search_table(_data)

@router.post("/tables/add")
async def create_table(_data: Tables):
    _id = ser_insert_table(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/tables/update")
async def edit_table(_data: Tables):
    result = ser_update_table(_data, table_collection)
    updated_table = ser_getbyid_table(_data.id)

    if "start_date" in updated_table:
        updated_table["start_date"] = updated_table["start_date"].isoformat()
    if "end_date" in updated_table:
        updated_table["end_date"] = updated_table["end_date"].isoformat()
        
    await sio.emit("table_status_updated", updated_table)
    return result

@router.put("/tables/updatestatus/{table_id}")
async def edit_tablestatus(table_id: str):
    result = await ser_update_tablestatus(table_id)
    updated_table = await ser_getbyid_table(table_id)
    await sio.emit("table_status_updated", updated_table)

    return result

@router.delete("/tables/delete/{table_id}")
def remove_table(table_id: str):
    response = ser_delete_table(table_id, table_collection)
    return response