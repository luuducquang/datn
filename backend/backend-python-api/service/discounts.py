from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, Discounts
from config.database import database

discount_collection: Collection = database['Discounts']

def ser_get_discount():
    datas = []
    for data in discount_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_discount(discount_id:str):
    if not ObjectId.is_valid(discount_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    discount = discount_collection.find_one({"_id": ObjectId(discount_id)})

    if discount is None:
        raise HTTPException(status_code=404, detail="discount not found")

    discount["_id"] = str(discount["_id"])
    return discount

def ser_get_discount_by_code(code: str) -> int:
    discount = discount_collection.find_one({"code": code})

    if (
        discount and
        discount.get("quantity", 0) > 0 
        # and
        # discount.get("status", False) is True
    ):
        return discount.get("discount_value", 0)

    return 0


def ser_use_discount_by_code(code: str):
    discount = discount_collection.find_one({"code": code})

    if not discount:
        raise HTTPException(status_code=404, detail="Discount code not found")

    if not discount.get("status", True):
        raise HTTPException(status_code=400, detail="Discount code is not active")

    if discount.get("quantity", 0) <= 0:
        raise HTTPException(status_code=400, detail="Discount code is no longer available")

    updated_discount = discount_collection.find_one_and_update(
        {"_id": discount["_id"]},
        {
            "$inc": {
                "quantity": -1,
                "used_count": 1
            }
        },
        return_document=True  
    )

    updated_discount["_id"] = str(updated_discount["_id"])
    return updated_discount

def ser_restore_discount_by_code(code: str):
    discount = discount_collection.find_one({"code": code})

    if not discount:
        raise HTTPException(status_code=404, detail="Discount code not found")

    if not discount.get("status", True):
        raise HTTPException(status_code=400, detail="Discount code is not active")

    updated_discount = discount_collection.find_one_and_update(
        {"_id": discount["_id"]},
        {
            "$inc": {
                "quantity": 1,
                "used_count": -1
            }
        },
        return_document=True  
    )

    updated_discount["_id"] = str(updated_discount["_id"])
    return updated_discount


def ser_search_discount(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"code": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = discount_collection.count_documents(query)

    discounts = discount_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for discount in discounts:
        discount["_id"] = str(discount["_id"])
        data.append(discount)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }
def ser_insert_discount(_data: Discounts) -> str:
    existing = discount_collection.find_one({"code": _data.code})
    if existing:
        raise HTTPException(status_code=400, detail="Mã giảm giá đã tồn tại.")

    result = discount_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_discount(_data: Discounts, discount_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_discount = discount_collection.find_one({"_id": object_id})
    if not existing_discount:
        raise HTTPException(status_code=404, detail="discount not found")
    
    updated_discount = discount_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id","code"})} 
)
    
    if updated_discount.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_discount(discount_id: str, discount_collection: Collection):
    if not ObjectId.is_valid(discount_id):
        raise HTTPException(status_code=400, detail="Invalid discount ID")

    result = discount_collection.delete_one({"_id": ObjectId(discount_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="discount not found")
    
    return {"message": "discount deleted successfully"}
