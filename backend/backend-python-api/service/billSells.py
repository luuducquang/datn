from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import BillSells, Searchs
from config.database import database

billsell_collection: Collection = database['BillSells']
sellitem_collection: Collection = database['SellItems']
product_collection: Collection = database['Products']
user_collection: Collection = database['Users']

def ser_get_billsell():
    datas = []
    for data in billsell_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_billsell_by_user(user_id: str):
    datas = []
    for data in billsell_collection.find({"user_id": user_id}):
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_billsell_by_sell_id(sell_id: str):
    datas = []
    for data in sellitem_collection.find({"sell_id": sell_id}):
        data["_id"] = str(data["_id"])
        rental_item_data = product_collection.find_one({"_id": ObjectId(data["item_id"])})
        if rental_item_data:
            rental_item_data["_id"] = str(rental_item_data["_id"])  
            data["product"] = rental_item_data  
        else:
            data["product"] = None  
        datas.append(data)
    return datas

def ser_get_billsell_by_billsell_id(billsell_id: str):
    datas = []
    for data in billsell_collection.find({"_id": ObjectId(billsell_id)}):
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_search_billsell(_data: Searchs) -> dict:
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"name": {"$regex": _data.search_term, "$options": "i"}},
            {"email": {"$regex": _data.search_term, "$options": "i"}},
            {"phone": {"$regex": _data.search_term, "$options": "i"}},
            {"address": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = billsell_collection.count_documents(query)

    billsells = billsell_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for billsell in billsells:
        billsell["_id"] = str(billsell["_id"])

        user_info = None
        if "user_id" in billsell:
            user = user_collection.find_one({"_id": ObjectId(billsell["user_id"])})
            if user:
                user["_id"] = str(user["_id"])
                user_info = {
                    "user_id": user["_id"],
                    "username": user.get("username", ""),
                    "email": user.get("email", ""),
                    "phone": user.get("phone", ""),
                    "fullname": user.get("fullname", "")
                }
        billsell["user_info"] = user_info

        related_items = sellitem_collection.find({"sell_id": billsell["_id"]})
        billsell["sell_items"] = [
            {
                **item,
                "_id": str(item["_id"]),
                "sell_id": str(item["sell_id"]),
            } for item in related_items
        ]

        data.append(billsell)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }


def ser_insert_billsell(_data: BillSells) -> str:
    if _data.sell_items:
        for item in _data.sell_items:
            rental_item = product_collection.find_one({"_id": ObjectId(item.item_id)})
            if not rental_item:
                raise HTTPException(status_code=404, detail=f"Không tìm thấy món hàng với ID {item.item_id}")

            available_quantity = rental_item.get("quantity_available", 0)
            if available_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Số lượng sản phẩm không đủ, còn: {available_quantity} sản phẩm"
                )

    bill_data = {
        "user_id": _data.user_id,
        "sell_date": _data.sell_date,
        "name": _data.name,
        "email": _data.email,
        "phone": _data.phone,
        "address": _data.address,
        "address_detail": _data.address_detail,
        "total_price": _data.total_price,
        "status": _data.status,
        "is_paid": _data.is_paid,
        "created_at": datetime.now() 
    }

    result = billsell_collection.insert_one(bill_data)
    bill_id = str(result.inserted_id)

    if _data.sell_items:
        for item in _data.sell_items:
            item.sell_id = bill_id  
            rental_item = product_collection.find_one({"_id": ObjectId(item.item_id)})
            available_quantity = rental_item.get("quantity_available", 0)

            update_result = product_collection.update_one(
                {"_id": ObjectId(item.item_id)},
                {"$set": {"quantity_available": available_quantity - item.quantity}}
            )
            if update_result.modified_count == 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"Không thể cập nhật số lượng tồn kho cho món hàng {item.item_id}"
                )

        sellitem_collection.insert_many([item.dict(exclude={"id"}) for item in _data.sell_items])

    return bill_id


def ser_update_billsell(_data: BillSells, billsell_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_billsell = billsell_collection.find_one({"_id": object_id})
    if not existing_billsell:
        raise HTTPException(status_code=404, detail="billsell not found")
    
    updated_billsell = billsell_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_billsell.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_billsell(billsell_id: str, billsell_collection: Collection):
    if not ObjectId.is_valid(billsell_id):
        raise HTTPException(status_code=400, detail="Invalid billsell ID")

    result = billsell_collection.delete_one({"_id": ObjectId(billsell_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="billsell not found")
    
    return {"message": "billsell deleted successfully"}
