from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import TableMenuItems
from config.database import database

table_menuitem_collection: Collection = database['TableMenuItems']
menuitem_collection: Collection = database['MenuItems']

def ser_get_tablemenuitem():
    datas = []
    for data in table_menuitem_collection.find():
        data["_id"] = str(data["_id"])

        menuitem_data = menuitem_collection.find_one({"_id": ObjectId(data["item_id"])})
        if menuitem_data:
            menuitem_data["_id"] = str(menuitem_data["_id"])  
            data["menuitem"] = menuitem_data  
        else:
            data["menuitem"] = None  

        datas.append(data)
    return datas

def ser_getbyid_table_tablemenuitem(table_id:str):
    if not ObjectId.is_valid(table_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    table_menuitem_data = table_menuitem_collection.find({"table_id": table_id})
    
    if table_menuitem_data is None:
        raise HTTPException(status_code=404, detail="table menuitem not found")

    result = []
    for item in table_menuitem_data:
        item["_id"] = str(item["_id"])

        menuitem_data = menuitem_collection.find_one({"_id": ObjectId(item["item_id"])})
        if menuitem_data:
            menuitem_data["_id"] = str(menuitem_data["_id"])
            item["menuitem"] = menuitem_data
        else:
            item["menuitem"] = None 

        result.append(item)

    return result


def ser_insert_table_menuitem(_data: TableMenuItems) -> str:
    menu_item = menuitem_collection.find_one({"_id": ObjectId(_data.item_id)})

    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item không tồn tại.")

    if menu_item["stock_quantity"] < _data.quantity:
        raise HTTPException(status_code=400, detail=f"Không đủ số lượng trong kho. Trong kho còn {menu_item['stock_quantity']} sản phẩm.")

    existing_menuitem = table_menuitem_collection.find_one({"table_id": _data.table_id, "item_id": _data.item_id})

    if existing_menuitem:
        updated_quantity = existing_menuitem["quantity"] + _data.quantity

        if menu_item["stock_quantity"] < updated_quantity:
            raise HTTPException(status_code=400, detail=f"Không đủ số lượng trong kho sau khi cập nhật. Trong kho còn {menu_item['stock_quantity']} sản phẩm.")

        updated_total_price = updated_quantity * existing_menuitem["unit_price"]
        
        table_menuitem_collection.update_one(
            {"_id": existing_menuitem["_id"]},
            {"$set": {"quantity": updated_quantity, "total_price": updated_total_price}}
        )

        menuitem_collection.update_one(
            {"_id": ObjectId(_data.item_id)},
            {"$inc": {"stock_quantity": -_data.quantity}}
        )
        return str(existing_menuitem["_id"])
    else:
        result = table_menuitem_collection.insert_one(_data.dict(exclude={"id"}))
    
        menuitem_collection.update_one(
            {"_id": ObjectId(_data.item_id)},
            {"$inc": {"stock_quantity": -_data.quantity}}
        )
        return str(result.inserted_id)



def ser_update_table_menuitem(_data: TableMenuItems, 
                              table_menuitem_collection: Collection, 
                              menuitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_menuitem = table_menuitem_collection.find_one({"_id": object_id})
    if not existing_menuitem:
        raise HTTPException(status_code=404, detail="Table menuitem not found")

    menu_item = menuitem_collection.find_one({"_id": ObjectId(existing_menuitem["item_id"])})
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    quantity_difference = _data.quantity - existing_menuitem["quantity"]

    if quantity_difference > 0 and menu_item["stock_quantity"] < quantity_difference:
        raise HTTPException(status_code=400, detail=f"Không đủ số lượng trong kho sau khi cập nhật. Trong kho còn {menu_item['stock_quantity']} sản phẩm.")

    updated_table_menuitem = table_menuitem_collection.update_one(
        {"_id": object_id},
        {"$set": _data.dict(exclude={"id"})}
    )

    if updated_table_menuitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    menuitem_collection.update_one(
        {"_id": ObjectId(existing_menuitem["item_id"])},
        {"$inc": {"stock_quantity": -quantity_difference}}
    )

    return {"message": "Updated successfully"}



def ser_delete_table_menuitem(table_id: str, table_menuitem_collection: Collection):
    if not ObjectId.is_valid(table_id):
        raise HTTPException(status_code=400, detail="Invalid menuitem ID")

    result = table_menuitem_collection.delete_many({"table_id": table_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="table menuitem not found")
    
    return {"message": "table menuitem deleted successfully"}

def ser_delete_menuitem(id: str, table_menuitem_collection: Collection, menuitem_collection: Collection):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid menuitem ID")

    existing_menuitem = table_menuitem_collection.find_one({"_id": ObjectId(id)})
    if not existing_menuitem:
        raise HTTPException(status_code=404, detail="Table menuitem not found")

    result = table_menuitem_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Delete failed")

    menuitem_collection.update_one(
        {"_id": ObjectId(existing_menuitem["item_id"])},
        {"$inc": {"stock_quantity": +existing_menuitem["quantity"]}}
    )

    return {"message": "Menuitem deleted successfully"}
