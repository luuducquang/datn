from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import SellItems
from config.database import database

sellitem_collection: Collection = database['SellItems']

def ser_get_sellitem():
    datas = []
    for data in sellitem_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_insert_sellitem(_data: SellItems, sellitem_collection: Collection, rentalitem_collection: Collection) -> str:
    rental_item = rentalitem_collection.find_one({"_id": ObjectId(_data.item_id)})
    if not rental_item:
        raise HTTPException(status_code=404, detail="Rental item not found")

    available_quantity = rental_item.get("quantity_available", 0)
    if _data.quantity > available_quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Số lượng không đủ, kho còn: {available_quantity} sản phẩm"
        )

    updated_quantity_available = available_quantity - _data.quantity
    update_result = rentalitem_collection.update_one(
        {"_id": ObjectId(_data.item_id)},
        {"$set": {"quantity_available": updated_quantity_available}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to update RentalItem stock"
        )

    result = sellitem_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)


def ser_update_sellitem(_data: SellItems, sellitem_collection: Collection, rentalitem_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_sellitem = sellitem_collection.find_one({"_id": object_id})
    if not existing_sellitem:
        raise HTTPException(status_code=404, detail="Sell item not found")

    rental_item = rentalitem_collection.find_one({"_id": ObjectId(_data.item_id)})
    if not rental_item:
        raise HTTPException(status_code=404, detail="Rental item not found")

    old_quantity = existing_sellitem.get("quantity", 0)
    new_quantity = _data.quantity
    quantity_difference = new_quantity - old_quantity

    available_quantity = rental_item.get("quantity_available", 0)
    updated_quantity_available = available_quantity - quantity_difference


    if updated_quantity_available < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Số lượng không đủ, trong kho còn: {available_quantity} sản phẩm"
        )

    rentalitem_collection.update_one(
        {"_id": ObjectId(_data.item_id)},
        {"$set": {"quantity_available": updated_quantity_available}}
    )

    sellitem_collection.update_one(
        {"_id": object_id},
        {"$set": _data.dict(exclude={"id"})}
    )

    return {"message": "Updated successfully"}


def ser_delete_sellitem(sellitem_id: str, sellitem_collection: Collection, rentalitem_collection: Collection):
    if not ObjectId.is_valid(sellitem_id):
        raise HTTPException(status_code=400, detail="Invalid sellitem ID")
    
    sellitem = sellitem_collection.find_one({"_id": ObjectId(sellitem_id)})
    if not sellitem:
        raise HTTPException(status_code=404, detail="SellItem not found")
    
    rental_item = rentalitem_collection.find_one({"_id": ObjectId(sellitem["item_id"])})
    if not rental_item:
        raise HTTPException(status_code=404, detail="Related RentalItem not found")

    updated_quantity_available = rental_item.get("quantity_available", 0) + sellitem.get("quantity", 0)
    update_result = rentalitem_collection.update_one(
        {"_id": ObjectId(sellitem["item_id"])},
        {"$set": {"quantity_available": updated_quantity_available}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update RentalItem stock")
    
    delete_result = sellitem_collection.delete_one({"_id": ObjectId(sellitem_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="SellItem not found or could not be deleted")

    return {"message": "SellItem deleted successfully and stock updated"}
