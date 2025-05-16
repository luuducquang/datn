from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import CategoryProducts, Searchs
from config.database import database

categoryproduct_collection: Collection = database['CategoryProducts']

def ser_get_category():
    datas = []
    for data in categoryproduct_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_categoryproduct(category_id:str):
    if not ObjectId.is_valid(category_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    category = categoryproduct_collection.find_one({"_id": ObjectId(category_id)})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    category["_id"] = str(category["_id"])
    return category

def ser_search_categoryproduct(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"category_name": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = categoryproduct_collection.count_documents(query)

    categoryRentalitems = categoryproduct_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for category in categoryRentalitems:
        category["_id"] = str(category["_id"])
        data.append(category)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_categoryproduct(_data: CategoryProducts) -> str:
    result = categoryproduct_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_categoryproduct(_data: CategoryProducts, categoryproduct_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_category = categoryproduct_collection.find_one({"_id": object_id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="category not found")
    
    updated_category = categoryproduct_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_category.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_categoryproduct(category_id: str, categoryproduct_collection: Collection):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    result = categoryproduct_collection.delete_one({"_id": ObjectId(category_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="category not found")
    
    return {"message": "category deleted successfully"}
