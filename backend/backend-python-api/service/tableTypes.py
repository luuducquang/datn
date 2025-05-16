from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, TableTypes
from config.database import database

tabletype_collection: Collection = database['TableTypes']

def ser_get_tabletype():
    datas = []
    for data in tabletype_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_tabletype(tabletype_id:str):
    if not ObjectId.is_valid(tabletype_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    tabletype = tabletype_collection.find_one({"_id": ObjectId(tabletype_id)})

    if tabletype is None:
        raise HTTPException(status_code=404, detail="tabletype not found")

    tabletype["_id"] = str(tabletype["_id"])
    return tabletype

def ser_search_tabletype(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"table_type_name": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = tabletype_collection.count_documents(query)

    tabletypes = tabletype_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for tabletype in tabletypes:
        tabletype["_id"] = str(tabletype["_id"])
        data.append(tabletype)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_tabletype(_data: TableTypes) -> str:
    result = tabletype_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_tabletype(_data: TableTypes, tabletype_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_tabletype = tabletype_collection.find_one({"_id": object_id})
    if not existing_tabletype:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    updated_tabletype = tabletype_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_tabletype.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_tabletype(tabletype_id: str, tabletype_collection: Collection):
    if not ObjectId.is_valid(tabletype_id):
        raise HTTPException(status_code=400, detail="Invalid tableType ID")

    result = tabletype_collection.delete_one({"_id": ObjectId(tabletype_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    return {"message": "tableType deleted successfully"}
