from typing import List, Tuple
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Products, Searchs
from config.database import database

product_collection: Collection = database['Products']
categoryproduct_collection: Collection = database['CategoryProducts']
manufactor_collection: Collection = database['Manufactors']

def ser_get_product():
    datas = []
    for data in product_collection.find():
        data["_id"] = str(data["_id"])
        datas.append(data)
    return datas

def ser_getbyid_product(_data: Products) -> str:
    result = product_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_getbyid_product(product_id:str):
    if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    product_data = product_collection.find_one({"_id": ObjectId(product_id)})

    if product_data is None:
        raise HTTPException(status_code=404, detail="product not found")
    
    product_collection.update_one(
        {"_id": ObjectId(product_id)},  
        {"$inc": {"view": 1}}  
    )

    product_data["_id"] = str(product_data["_id"])

    categoryproduct_data = categoryproduct_collection.find_one({"_id": ObjectId(product_data["category_id"])})
    if categoryproduct_data:
        categoryproduct_data["_id"] = str(categoryproduct_data["_id"])  
        product_data["categoryproduct"] = categoryproduct_data  
    else:
        product_data["categoryproduct"] = None  

    manufactor_data = manufactor_collection.find_one({"_id": ObjectId(product_data["manufactor_id"])})
    if manufactor_data:
        manufactor_data["_id"] = str(manufactor_data["_id"])  
        product_data["manufactor"] = manufactor_data  
    else:
        product_data["manufactor"] = None  
    
    return product_data

# def ser_search_product(_data:Searchs):
#     if _data.page <= 0 or _data.pageSize <= 0:
#         raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
#     skip = (_data.page - 1) * _data.pageSize

#     query = {}
#     if _data.search_term:
#         query["$or"] = [
#             {"item_name": {"$regex": _data.search_term, "$options": "i"}},
#             {"price": {"$regex": _data.search_term, "$options": "i"}},
#             {"price_reduction": {"$regex": _data.search_term, "$options": "i"}},
#             {"rental_price_day": {"$regex": _data.search_term, "$options": "i"}},
#             {"rental_price_hours": {"$regex": _data.search_term, "$options": "i"}},
#             {"quantity_available": {"$regex": _data.search_term, "$options": "i"}},
#             {"view": {"$regex": _data.search_term, "$options": "i"}},
#             {"origin": {"$regex": _data.search_term, "$options": "i"}},
#             {"description": {"$regex": _data.search_term, "$options": "i"}},
#             {"description_detail": {"$regex": _data.search_term, "$options": "i"}},
#         ]

#     total_items = product_collection.count_documents(query)

#     products = product_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

#     data = []
#     for product in products:
#         product["_id"] = str(product["_id"])
#         categoryproduct_data = categoryproduct_collection.find_one({"_id": ObjectId(product["category_id"])})
#         if categoryproduct_data:
#             categoryproduct_data["_id"] = str(categoryproduct_data["_id"])  
#             product["categoryproduct"] = categoryproduct_data  
#         else:
#             product["categoryproduct"] = None  

#         manufactor_data = manufactor_collection.find_one({"_id": ObjectId(product["manufactor_id"])})
#         if manufactor_data:
#             manufactor_data["_id"] = str(manufactor_data["_id"])  
#             product["manufactor"] = manufactor_data  
#         else:
#             product["manufactor"] = None  

#         data.append(product)

#     return {
#         "page":_data.page,
#         "pageSize":_data.pageSize,
#         "totalItems": total_items,
#         "data": data,
#     }

def ser_search_product(_data: Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize
    query = {}
    if _data.search_term:
        query["$or"] = [
            {"item_name": {"$regex": _data.search_term, "$options": "i"}},
            {"price": {"$regex": _data.search_term, "$options": "i"}},
            {"price_reduction": {"$regex": _data.search_term, "$options": "i"}},
            {"rental_price_day": {"$regex": _data.search_term, "$options": "i"}},
            {"rental_price_hours": {"$regex": _data.search_term, "$options": "i"}},
            {"quantity_available": {"$regex": _data.search_term, "$options": "i"}},
            {"view": {"$regex": _data.search_term, "$options": "i"}},
            {"origin": {"$regex": _data.search_term, "$options": "i"}},
            {"description": {"$regex": _data.search_term, "$options": "i"}},
            {"description_detail": {"$regex": _data.search_term, "$options": "i"}},
        ]

    if _data.category_name:
        category = categoryproduct_collection.find_one({"category_name": {"$regex": _data.category_name, "$options": "i"}})
        print(_data.category_name)
        print(category)
        if category:
            query["category_id"] = str(category["_id"])
        else:
            return {
                "page": _data.page,
                "pageSize": _data.pageSize,
                "totalItems": 0,
                "data": []
            }

    total_items = product_collection.count_documents(query)
    products = product_collection.find(query).sort("_id", -1).skip(skip).limit(_data.pageSize)

    data = []
    for product in products:
        product["_id"] = str(product["_id"])

        categoryproduct_data = categoryproduct_collection.find_one({"_id": ObjectId(product["category_id"])})
        if categoryproduct_data:
            categoryproduct_data["_id"] = str(categoryproduct_data["_id"])
            product["categoryproduct"] = categoryproduct_data
        else:
            product["categoryproduct"] = None

        manufactor_data = manufactor_collection.find_one({"_id": ObjectId(product["manufactor_id"])})
        if manufactor_data:
            manufactor_data["_id"] = str(manufactor_data["_id"])
            product["manufactor"] = manufactor_data
        else:
            product["manufactor"] = None

        data.append(product)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_product(_data: Products) -> str:
    result = product_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_product(_data: Products, product_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_product = product_collection.find_one({"_id": object_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="product not found")
    
    updated_product = product_collection.update_one(
    {"_id": ObjectId(_data.id)},  
    {"$set": _data.dict(exclude={"id"})} 
)
    
    if updated_product.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "updated successfully"}


def ser_delete_product(product_id: str, product_collection: Collection):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="product not found")
    
    return {"message": "product deleted successfully"}

def ser_check_quantities(ids: List[str], quantities: List[int]) -> List[dict]:
    insufficient_items = ""

    for item_id, quantity_to_add in zip(ids, quantities):
        item = product_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            insufficient_items ={"id": item_id,"item_name":item['item_name'], "reason": "Item not found"}
            continue

        if item["quantity_available"] < quantity_to_add:
            insufficient_items = {
                "id": item_id,
                "item_name":item['item_name'],
                "quantity_available": item['quantity_available'],
                "quantity_add": quantity_to_add
            }

    return insufficient_items


def ser_check_and_update_quantities(ids: List[str], quantities: List[int]) -> List[dict]:
    insufficient_items = [] 

    for item_id, quantity_to_subtract in zip(ids, quantities):
        item = product_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            insufficient_items.append({
                "id": item_id,
                "reason": "Item not found"
            })
            continue

        if item["quantity_available"] < quantity_to_subtract:
            insufficient_items.append({
                "id": item_id,
                "item_name": item['item_name'],
                "quantity_available": item['quantity_available'],
                "quantity_subtract": quantity_to_subtract,
                "reason": "Not enough quantity"
            })
            continue

        product_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$inc": {"quantity_available": -quantity_to_subtract}}
        )

    return insufficient_items
