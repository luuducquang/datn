from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Suppliers
from config.database import database

supplier_collection: Collection = database['Suppliers']

def ser_get_supplier():
    datas = []
    for data in supplier_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_supplier(_data: Suppliers) -> str:
    result = supplier_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_supplier(_data: Suppliers, supplier_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_supplier = supplier_collection.find_one({"_id": object_id})
    if not existing_supplier:
        raise HTTPException(status_code=404, detail="supplier not found")
    
    updated_supplier = supplier_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_supplier.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_supplier(supplier_id: str, supplier_collection: Collection):
    if not ObjectId.is_valid(supplier_id):
        raise HTTPException(status_code=400, detail="Invalid supplier ID")

    result = supplier_collection.delete_one({"_id": ObjectId(supplier_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="supplier not found")
    
    return {"message": "supplier deleted successfully"}
