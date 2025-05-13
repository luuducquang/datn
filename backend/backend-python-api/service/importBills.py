from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import ImportBills, Searchs
from config.database import database

importbill_collection: Collection = database['ImportBills']
importitem_collection: Collection = database['ImportItems']
product_collection: Collection = database['Products']
menuitem_collection: Collection = database['MenuItems']
user_collection: Collection = database['Users']
supplier_collection: Collection = database['Suppliers']

def ser_get_importbill():
    datas = []
    for data in importbill_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_get_import_item_by_import_id(import_id: str):
    datas = []
    for data in importitem_collection.find({"import_id": import_id}):
        data["_id"] = str(data["_id"])

        rental_item_data = product_collection.find_one({"_id": ObjectId(data["item_id"])})
        if rental_item_data:
            rental_item_data["_id"] = str(rental_item_data["_id"])
            data["item"] = rental_item_data
        else:
            menu_item_data = menuitem_collection.find_one({"_id": ObjectId(data["item_id"])})
            if menu_item_data:
                menu_item_data["_id"] = str(menu_item_data["_id"])
                data["item"] = menu_item_data
            else:
                data["item"] = None

        datas.append(data)
    return datas

def ser_get_importbill_by_importbill_id(import_id: str):
    datas = []
    for data in importbill_collection.find({"_id": ObjectId(import_id)}):
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_search_importbills(_data: Searchs) -> dict:
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}
    if _data.search_term:
        suppliers = supplier_collection.find({"name": {"$regex": _data.search_term, "$options": "i"}})
        supplier_ids = [str(supplier["_id"]) for supplier in suppliers]

        if supplier_ids:
            query["supplier_id"] = {"$in": supplier_ids}
        else:
            return {
                "page": _data.page,
                "pageSize": _data.pageSize,
                "totalItems": 0,
                "data": []
            }

    total_items = importbill_collection.count_documents(query)
    importbills = importbill_collection.find(query).skip(skip).limit(_data.pageSize)

    data = []
    for importbill in importbills:
        importbill["_id"] = str(importbill["_id"])

        user_info = None
        if "user_id" in importbill:
            user = user_collection.find_one({"_id": ObjectId(importbill["user_id"])})
            if user:
                user["_id"] = str(user["_id"])
                user_info = {
                    "user_id": user["_id"],
                    "fullname": user.get("fullname", ""),
                }
        importbill["user_info"] = user_info

        supplier_info = None
        if "supplier_id" in importbill:
            supplier = supplier_collection.find_one({"_id": ObjectId(importbill["supplier_id"])})
            if supplier:
                supplier["_id"] = str(supplier["_id"])
                supplier_info = {
                    "supplier_id": supplier["_id"],
                    "name": supplier.get("name", ""),
                }
        importbill["supplier_info"] = supplier_info

        data.append(importbill)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }




def ser_insert_importbill(_data: ImportBills) -> str:

    bill_data = {
        "user_id": _data.user_id,
        "supplier_id": _data.supplier_id,
        "import_date": _data.import_date,
        "total_price": _data.total_price,
    }

    result = importbill_collection.insert_one(bill_data)
    bill_id = str(result.inserted_id)

    if _data.import_items:
        for item in _data.import_items:
            item.import_id = bill_id 
            product = product_collection.find_one({"_id": ObjectId(item.item_id)})
            
            if product:
                available_quantity = product.get("quantity_available", 0)
                calculated_price_reduction = int(item.unit_price + (item.unit_price * 0.2))
                calculated_price = int(item.unit_price + (item.unit_price * 0.5))
                update_result = product_collection.update_one(
                    {"_id": ObjectId(item.item_id)},
                    {"$set": {"quantity_available": available_quantity + item.quantity,
                              "price_reduction":calculated_price_reduction,
                              "price":calculated_price,
                              "price_origin":item.unit_price}
                    }
                )
                if update_result.modified_count == 0:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Không thể cập nhật số lượng kho cho món hàng {item.item_id} trong Products"
                    )
            else:
                menu_item = menuitem_collection.find_one({"_id": ObjectId(item.item_id)})
                if menu_item:
                    available_quantity = menu_item.get("stock_quantity", 0)
                    
                    calculated_price = int(item.unit_price + (item.unit_price * 0.2))
                    update_result = menuitem_collection.update_one(
                        {"_id": ObjectId(item.item_id)},
                        {"$set": {"stock_quantity": available_quantity + item.quantity,"price":calculated_price,
                              "price_origin":item.unit_price}}
                    )
                    if update_result.modified_count == 0:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Không thể cập nhật số lượng kho cho món hàng {item.item_id} trong MenuItems"
                        )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Không tìm thấy món hàng với ID {item.item_id} trong cả Products và MenuItems"
                    )

        import_items_data = [item.dict(exclude={"id"}) for item in _data.import_items]
        importitem_collection.insert_many(import_items_data)

    return bill_id



def ser_update_importbill(_data: ImportBills, importbill_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_importbill = importbill_collection.find_one({"_id": object_id})
    if not existing_importbill:
        raise HTTPException(status_code=404, detail="importbill not found")
    
    updated_importbill = importbill_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_importbill.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_importbill(importbill_id: str, importbill_collection: Collection):
    if not ObjectId.is_valid(importbill_id):
        raise HTTPException(status_code=400, detail="Invalid importbill ID")

    result = importbill_collection.delete_one({"_id": ObjectId(importbill_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="importbill not found")
    
    return {"message": "importbill deleted successfully"}
