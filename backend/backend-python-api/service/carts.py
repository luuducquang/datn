from typing import List
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Carts
from config.database import database

cart_collection: Collection = database['Carts']
rentalitem_collection: Collection = database['RentalItems']

def ser_get_cart():
    datas = []
    for data in cart_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_cart_by_user_id(user_id:str):
    if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    cart_data = cart_collection.find({"user_id": user_id})
    
    if cart_data is None:
        raise HTTPException(status_code=404, detail="cart not found")

    result = []
    for item in cart_data:
        item["_id"] = str(item["_id"])

        data_rentalitem = rentalitem_collection.find_one({"_id": ObjectId(item["item_id"])})
        if data_rentalitem:
            data_rentalitem["_id"] = str(data_rentalitem["_id"])
            item["rentalitem"] = data_rentalitem
        else:
            item["rentalitem"] = None

        result.append(item)

    return result

def ser_insert_cart(_data: Carts) -> str:
    result = cart_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)


def ser_update_cart(_data: Carts, cart_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_cart = cart_collection.find_one({"_id": object_id})
    if not existing_cart:
        raise HTTPException(status_code=404, detail="cart not found")
    
    update_data = _data.dict(exclude={"id", "user_id"}) 
    
    updated_cart = cart_collection.update_one(
        {"_id": object_id},  
        {"$set": update_data} 
    )
    
    if updated_cart.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}

def ser_update_cart_false_status(user_id: str, cart_collection: Collection):
    try:
        user_object_id = user_id
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    updated_carts = cart_collection.update_many(
        {"user_id": user_object_id},  
        {"$set": {"status": False}}   
    )
    
    # if updated_carts.modified_count == 0:
    #     raise HTTPException(status_code=404, detail="No carts found with the given user_id")

    return {"message": f"{updated_carts.modified_count} cart(s) updated successfully"}



def ser_delete_cart(cart_id: str, cart_collection: Collection):
    if not ObjectId.is_valid(cart_id):
        raise HTTPException(status_code=400, detail="Invalid cart ID")

    result = cart_collection.delete_one({"_id": ObjectId(cart_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="cart not found")
    
    return {"message": "cart deleted successfully"}


def ser_delete_carts(cart_ids: List[str], cart_collection: Collection):
    if not cart_ids:
        raise HTTPException(status_code=400, detail="No cart IDs provided")

    invalid_ids = [cart_id for cart_id in cart_ids if not ObjectId.is_valid(cart_id)]
    if invalid_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cart IDs: {', '.join(invalid_ids)}"
        )

    object_ids = [ObjectId(cart_id) for cart_id in cart_ids]
    result = cart_collection.delete_many({"_id": {"$in": object_ids}})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No carts found to delete")

    return {
        "message": f"Successfully deleted {result.deleted_count} carts",
        "deleted_count": result.deleted_count
    }
