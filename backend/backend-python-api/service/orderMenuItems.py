from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, OrderMenuItems
from config.database import database

ordermenuitem_collection: Collection = database['OrderMenuItems']
menuitems_collection: Collection = database['MenuItems']

def ser_get_ordermenuitem():
    datas = []
    for data in ordermenuitem_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_ordermenuitem(orderitem_id: str):
    if not ObjectId.is_valid(orderitem_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    cursor = ordermenuitem_collection.find({"order_id": orderitem_id})

    ordermenuitems = []
    for item in cursor:
        item["_id"] = str(item["_id"])

        item_id = item.get("item_id")
        if item_id and ObjectId.is_valid(item_id):
            menu_item = menuitems_collection.find_one({"_id": ObjectId(item_id)})
            if menu_item:
                menu_item["_id"] = str(menu_item["_id"])
                item["menu_items"] = menu_item
            else:
                item["menu_items"] = None
        else:
            item["menu_items"] = None

        ordermenuitems.append(item)

    if len(ordermenuitems) == 0:
        # In ra debug để xem
        print(f"No ordermenuitems found for order_id: {cursor}")
        raise HTTPException(status_code=404, detail="No ordermenuitems found for this order_id")

    return ordermenuitems


def ser_search_ordermenuitem(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"quantity": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = ordermenuitem_collection.count_documents(query)

    ordermenuitems = ordermenuitem_collection.find(query).skip(skip).limit(_data.pageSize)

    data = []
    for ordermenuitem in ordermenuitems:
        ordermenuitem["_id"] = str(ordermenuitem["_id"])
        data.append(ordermenuitem)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_ordermenuitem(_data: OrderMenuItems) -> str:
    result = ordermenuitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_ordermenuitem(_data: OrderMenuItems, ordermenuitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_ordermenuitem = ordermenuitem_collection.find_one({"_id": object_id})
    if not existing_ordermenuitem:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    updated_ordermenuitem = ordermenuitem_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_ordermenuitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_ordermenuitem(ordermenuitem_id: str, ordermenuitem_collection: Collection):
    if not ObjectId.is_valid(ordermenuitem_id):
        raise HTTPException(status_code=400, detail="Invalid tableType ID")

    result = ordermenuitem_collection.delete_one({"_id": ObjectId(ordermenuitem_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tableType not found")
    
    return {"message": "tableType deleted successfully"}
