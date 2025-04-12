from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import ImportItems
from config.database import database

importitem_collection: Collection = database['ImportItems']
rentalitem_collection: Collection = database['RentalItems']
menuitem_collection: Collection = database['MenuItems']

def ser_get_importitem():
    datas = []
    for data in importitem_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_importitem(_data: ImportItems) -> str:
    result = importitem_collection.insert_one(_data.dict(exclude={"id"}))
    import_item_id = str(result.inserted_id)

    rental_item = rentalitem_collection.find_one({"_id": ObjectId(_data.item_id)})
    
    if rental_item:
        available_quantity = rental_item.get("quantity_available", 0)
        calculated_price_reduction = int(_data.unit_price + (_data.unit_price * 0.2))
        calculated_price = int(_data.unit_price + (_data.unit_price * 0.5))
        rentalitem_collection.update_one(
            {"_id": ObjectId(_data.item_id)},
            {"$set": {"quantity_available": available_quantity + _data.quantity,
                      "price_reduction":calculated_price_reduction,
                              "price":calculated_price}}
        )
    else:
        menu_item = menuitem_collection.find_one({"_id": ObjectId(_data.item_id)})
        calculated_price = int(_data.unit_price + (_data.unit_price * 0.2))
        if menu_item:
            available_quantity = menu_item.get("stock_quantity", 0)
            menuitem_collection.update_one(
                {"_id": ObjectId(_data.item_id)},
                {"$set": {"stock_quantity": available_quantity + _data.quantity,
                          "price":calculated_price}}
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy món hàng với ID {_data.item_id} trong cả MenuItems và RentalItems"
            )

    return import_item_id


def ser_update_importitem(_data: ImportItems, importitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_importitem = importitem_collection.find_one({"_id": object_id})
    if not existing_importitem:
        raise HTTPException(status_code=404, detail="Import item not found")
    
    item_id = _data.item_id
    
    rental_item = rentalitem_collection.find_one({"_id": ObjectId(item_id)})
    
    if rental_item:
        available_quantity = rental_item.get("quantity_available", 0)
        
        new_quantity_in_stock = available_quantity + (_data.quantity - existing_importitem['quantity'])
        
        if new_quantity_in_stock < 0:
            raise HTTPException(status_code=400, detail=f"Trong kho không còn đủ số lượng. Kho còn {available_quantity} sản phẩm")
        
        rentalitem_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"quantity_available": new_quantity_in_stock}}
        )
    
    else:
        menu_item = menuitem_collection.find_one({"_id": ObjectId(item_id)})
        if menu_item:
            stock_quantity = menu_item.get("stock_quantity", 0)
            
            new_quantity_in_stock = stock_quantity + (_data.quantity - existing_importitem['quantity'])
            
            if new_quantity_in_stock < 0:
                raise HTTPException(status_code=400, detail=f"Trong kho không còn đủ số lượng. Kho còn {stock_quantity} sản phẩm")
            
            menuitem_collection.update_one(
                {"_id": ObjectId(item_id)},
                {"$set": {"stock_quantity": new_quantity_in_stock}}
            )
        
        else:
            raise HTTPException(status_code=404, detail="Item not found in both RentalItems and MenuItems")

    updated_importitem = importitem_collection.update_one(
        {"_id": ObjectId(_data.id)},  
        {"$set": _data.dict(exclude={"id"})}
    )
    
    if updated_importitem.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "Updated successfully"}




def ser_delete_importitem(importitem_id: str, importitem_collection: Collection, rentalitem_collection: Collection, menuitem_collection: Collection):
    if not ObjectId.is_valid(importitem_id):
        raise HTTPException(status_code=400, detail="Invalid importitem ID")

    importitem = importitem_collection.find_one({"_id": ObjectId(importitem_id)})
    if not importitem:
        raise HTTPException(status_code=404, detail="Import item not found")

    item_id = importitem.get("item_id")
    quantity_to_remove = importitem.get("quantity", 0)

    rental_item = rentalitem_collection.find_one({"_id": ObjectId(item_id)})
    
    if rental_item:
        available_quantity = rental_item.get("quantity_available", 0)
        
        if available_quantity < quantity_to_remove:
            raise HTTPException(
                status_code=400,
                detail=f"Số lượng trong kho không đủ để giảm, kho còn {available_quantity} sản phẩm"
            )

        updated_quantity_available = available_quantity - quantity_to_remove
        rentalitem_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"quantity_available": updated_quantity_available}}
        )
    
    else:
        menu_item = menuitem_collection.find_one({"_id": ObjectId(item_id)})
        if menu_item:
            stock_quantity = menu_item.get("stock_quantity", 0)
            
            if stock_quantity < quantity_to_remove:
                raise HTTPException(
                    status_code=400,
                    detail=f"Số lượng trong kho không đủ để giảm, kho còn {stock_quantity} sản phẩm"
                )

            updated_stock_quantity = stock_quantity - quantity_to_remove
            menuitem_collection.update_one(
                {"_id": ObjectId(item_id)},
                {"$set": {"stock_quantity": updated_stock_quantity}}
            )
        
        else:
            raise HTTPException(status_code=404, detail="Item not found in both RentalItems and MenuItems")

    result = importitem_collection.delete_one({"_id": ObjectId(importitem_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Import item not found")

    return {"message": "Import item deleted and stock updated successfully"}

