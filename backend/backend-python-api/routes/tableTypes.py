from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Searchs, TableTypes
from service.tableTypes import ser_getbyid_tabletype,ser_search_tabletype,ser_get_tabletype,ser_delete_tabletype, ser_insert_tabletype, ser_update_tabletype


router = APIRouter()

tabletype_collection: Collection = database['TableTypes']

@router.get("/tabletypes/get")
async def get_tabletype():
    return ser_get_tabletype()

@router.get("/tabletypes/get/{tabletype_id}")
async def get_tabletype_by_id(tabletype_id: str):
    return ser_getbyid_tabletype(tabletype_id)

@router.post("/tabletypes/search")
async def search_tabletype(_data:Searchs):
    return ser_search_tabletype(_data)

@router.post("/tabletypes/add")
async def create_tabletype(_data: TableTypes):
    _id = ser_insert_tabletype(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/tabletypes/update")
def edit_tabletype(_data: TableTypes):
    result = ser_update_tabletype(_data, tabletype_collection)
    return result

@router.delete("/tabletypes/delete/{tabletype_id}")
def remove_tabletype(tabletype_id: str):
    response = ser_delete_tabletype(tabletype_id, tabletype_collection)
    return response