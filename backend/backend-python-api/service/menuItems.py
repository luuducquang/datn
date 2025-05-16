from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import MenuItems, Searchs, StockUpdateItem
from config.database import database

menuitem_collection: Collection = database['MenuItems']
categorymenuitem_collection: Collection = database['CategoryMenuItems']

def ser_get_menuitem():
    datas = []
    for data in menuitem_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_menuitem(menuitem_id:str):
    if not ObjectId.is_valid(menuitem_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    menuitem_data = menuitem_collection.find_one({"_id": ObjectId(menuitem_id)})

    if menuitem_data is None:
        raise HTTPException(status_code=404, detail="menuitem not found")

    menuitem_data["_id"] = str(menuitem_data["_id"])
    categorymenuitem_data = categorymenuitem_collection.find_one({"_id": ObjectId(menuitem_data["category_id"])})
    if categorymenuitem_data:
        categorymenuitem_data["_id"] = str(categorymenuitem_data["_id"])  
        menuitem_data["categorymenuitem"] = categorymenuitem_data  
    else:
        menuitem_data["categorymenuitem"] = None  
    return menuitem_data

def ser_search_menuitem(_data:Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        query["$or"] = [
            {"name": {"$regex": _data.search_term, "$options": "i"}},
            {"price": {"$regex": _data.search_term, "$options": "i"}},
            {"stock_quantity": {"$regex": _data.search_term, "$options": "i"}},
        ]

    total_items = menuitem_collection.count_documents(query)

    menuitems = menuitem_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for menuitem in menuitems:
        menuitem["_id"] = str(menuitem["_id"])
        categorymenuitem_data = categorymenuitem_collection.find_one({"_id": ObjectId(menuitem["category_id"])})
        if categorymenuitem_data:
            categorymenuitem_data["_id"] = str(categorymenuitem_data["_id"])  
            menuitem["categorymenuitem"] = categorymenuitem_data  
        else:
            menuitem["categorymenuitem"] = None  
        data.append(menuitem)

    return {
        "page":_data.page,
        "pageSize":_data.pageSize,
        "totalItems": total_items,
        "data": data,
    }


def increase_stock_quantities(items: list[StockUpdateItem]):
    updated_items = []

    for item in items:
        if not ObjectId.is_valid(item.item_id):
            raise HTTPException(status_code=400, detail=f"Invalid ID: {item.item_id}")

        result = menuitem_collection.update_one(
            {"_id": ObjectId(item.item_id)},
            {"$inc": {"stock_quantity": item.quantity}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Menuitem not found: {item.item_id}")

        updated_items.append({
            "item_id": item.item_id,
            "quantity_increased": item.quantity
        })

    return {
        "message": "Stock quantities updated successfully.",
        "updated_items": updated_items
    }

def ser_insert_menuitem(_data: MenuItems) -> str:
    result = menuitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_menuitem(_data: MenuItems, menuitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_menuitem = menuitem_collection.find_one({"_id": object_id})
    if not existing_menuitem:
        raise HTTPException(status_code=404, detail="menuitem not found")
    
    updated_menuitem = menuitem_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_menuitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_menuitem(menuitem_id: str, menuitem_collection: Collection):
    if not ObjectId.is_valid(menuitem_id):
        raise HTTPException(status_code=400, detail="Invalid menuitem ID")

    result = menuitem_collection.delete_one({"_id": ObjectId(menuitem_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="menuitem not found")
    
    return {"message": "menuitem deleted successfully"}
