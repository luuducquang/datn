from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import TableRentalItems
from config.database import database

table_rentalitem_collection: Collection = database['TableRentalItems']
rentalitem_collection: Collection = database['RentalItems']

def ser_get_tablerentalitem():
    datas = []
    for data in table_rentalitem_collection.find():
        data["_id"] = str(data["_id"])

        rentalitem_data = rentalitem_collection.find_one({"_id": ObjectId(data["item_id"])})
        if rentalitem_data:
            rentalitem_data["_id"] = str(rentalitem_data["_id"])  
            data["rentalitem"] = rentalitem_data  
        else:
            data["rentalitem"] = None  

        datas.append(data)
    return datas

def ser_getbyid_table_tablerentalitem(table_id:str):
    if not ObjectId.is_valid(table_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    table_rentalitem_data = table_rentalitem_collection.find({"table_id": table_id})
    
    if table_rentalitem_data is None:
        raise HTTPException(status_code=404, detail="table rentalitem not found")

    result = []
    for item in table_rentalitem_data:
        item["_id"] = str(item["_id"])

        rentalitem_data = rentalitem_collection.find_one({"_id": ObjectId(item["item_id"])})
        if rentalitem_data:
            rentalitem_data["_id"] = str(rentalitem_data["_id"])
            item["rentalitem"] = rentalitem_data
        else:
            item["rentalitem"] = None 

        result.append(item)

    return result


def ser_insert_table_rentalitem(_data: TableRentalItems) -> str:
    result = table_rentalitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)


def ser_update_table_rentalitem(_data: TableRentalItems, table_rentalitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_rentalitem = table_rentalitem_collection.find_one({"_id": object_id})
    if not existing_rentalitem:
        raise HTTPException(status_code=404, detail="table rentalitem not found")
    
    updated_table_rentalitem = table_rentalitem_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_table_rentalitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_table_rentalitem(table_id: str, table_rentalitem_collection: Collection):
    if not ObjectId.is_valid(table_id):
        raise HTTPException(status_code=400, detail="Invalid rentalitem ID")

    result = table_rentalitem_collection.delete_many({"table_id": table_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="table rentalitem not found")
    
    return {"message": "table rentalitem deleted successfully"}

def ser_delete_rentalitem(id: str, table_rentalitem_collection: Collection):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid rentalitem ID")

    result = table_rentalitem_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="table rentalitem not found")
    
    return {"message": "rentalitem deleted successfully"}