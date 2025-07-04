from datetime import datetime, timedelta
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from schemas.schemas import Searchs, Tables
from config.database import database


table_collection: Collection = database['Tables']
tabletype_collection: Collection = database['TableTypes']
pricingrule_collection: Collection = database['PricingRules']


def ser_get_table():
    datas = []
    for data in table_collection.find():
        data["_id"] = str(data["_id"])
        tabletype_id = ObjectId(data["table_type_id"])
        tabletype_data = tabletype_collection.find_one({"_id": tabletype_id})
        if tabletype_data:
            tabletype_data["_id"] = str(tabletype_data["_id"])  
            data["tabletype"] = tabletype_data  
        else:
            data["tabletype"] = None  
        datas.append(data)
    return datas

def ser_getbyid_table(table_id:str):
    if not ObjectId.is_valid(table_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

    table = table_collection.find_one({"_id": ObjectId(table_id)})

    if table is None:
        raise HTTPException(status_code=404, detail="table not found")

    table["_id"] = str(table["_id"])
    tabletype_id = ObjectId(table["table_type_id"])
    tabletype_data = tabletype_collection.find_one({"_id": tabletype_id})
    if tabletype_data:
        tabletype_data["_id"] = str(tabletype_data["_id"])  
        table["tabletype"] = tabletype_data  

        pricingrule_cursor  = pricingrule_collection.find({"type_table_id": tabletype_data["_id"]})
        pricingrule_list = []

        for rule in pricingrule_cursor:
            rule["_id"] = str(rule["_id"])
            rule["type_table_id"] = str(rule["type_table_id"])
            pricingrule_list.append(rule)

        table["pricingrule"] = pricingrule_list
    else:
        table["tabletype"] = None  
    return table

def ser_search_table(_data: Searchs):
    if _data.page <= 0 or _data.pageSize <= 0:
        raise HTTPException(status_code=400, detail="Page and pageSize must be greater than 0")
    
    skip = (_data.page - 1) * _data.pageSize

    query = {}

    if _data.search_term:
        tabletype_query = {"table_type_name": {"$regex": _data.search_term, "$options": "i"}}
        tabletypes = tabletype_collection.find(tabletype_query)
        tabletype_ids = [str(tabletype["_id"]) for tabletype in tabletypes] 

        query["$or"] = [
            {"table_number": {"$regex": _data.search_term, "$options": "i"}},
            {"status": {"$regex": _data.search_term, "$options": "i"}},
        ]

        if tabletype_ids:
            query["$or"].append({"table_type_id": {"$in": tabletype_ids}})

    total_items = table_collection.count_documents(query)

    tables = table_collection.find(query).sort("_id", 1).skip(skip).limit(_data.pageSize)

    data = []
    for table in tables:
        table["_id"] = str(table["_id"])
        tabletype_id = ObjectId(table["table_type_id"])

        tabletype_data = tabletype_collection.find_one({"_id": tabletype_id})
        if tabletype_data:
            tabletype_data["_id"] = str(tabletype_data["_id"])  
            table["tabletype"] = tabletype_data  
        else:
            table["tabletype"] = None  
        data.append(table)

    return {
        "page": _data.page,
        "pageSize": _data.pageSize,
        "totalItems": total_items,
        "data": data,
    }

def ser_insert_table(_data: Tables) -> str:
    existing_table = table_collection.find_one({"table_number": _data.table_number})
    if existing_table  or _data.table_number == 0:
        raise HTTPException(status_code=400, detail=f"table '{_data.table_number}' already exists.")
    result = table_collection.insert_one(_data.dict(exclude={"id"}))
    return str(result.inserted_id)

def ser_update_table(_data: Tables, table_collection: Collection):
    if not _data.id:
        raise HTTPException(status_code=400, detail="ID is required for update")

    try:
        object_id = ObjectId(_data.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_table = table_collection.find_one({"_id": object_id})
    if not existing_table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    updated_table = table_collection.update_one(
        {"_id": object_id},  
        {"$set": _data.dict(exclude={"id"})} 
    )
    
    if updated_table.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
    
    return {"message": "Updated successfully"}


async def ser_update_tablestatus(table_id: str):
    try:
        object_id = ObjectId(table_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    existing_table = table_collection.find_one({"_id": object_id})
    if not existing_table:
        raise HTTPException(status_code=404, detail="Table not found")

    current_status = existing_table.get("status", False)
    new_status = not current_status

    updated_table = table_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": new_status}}
    )

    if updated_table.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "Updated successfully", "new_status": new_status}





def ser_delete_table(table_id: str, table_collection: Collection):
    if not ObjectId.is_valid(table_id):
        raise HTTPException(status_code=400, detail="Invalid table ID")

    result = table_collection.delete_one({"_id": ObjectId(table_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="table not found")
    
    return {"message": "table deleted successfully"}


def calculate_bill_service(table_id: str):
    if not ObjectId.is_valid(table_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    table = table_collection.find_one({"_id": ObjectId(table_id)})
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    if not table.get("start_date"):
        raise HTTPException(status_code=400, detail="Start time is missing")

    start_time = table["start_date"]
    end_time = datetime.now()

    total_seconds = int((end_time - start_time).total_seconds())

    table_type_id = table["table_type_id"]
    pricing_rules = list(pricingrule_collection.find({"type_table_id": table_type_id}))

    if not pricing_rules:
        raise HTTPException(status_code=404, detail="No pricing rules found")

    min_price_rule = min(pricing_rules, key=lambda r: r["rate_per_hour"])

    total_price = 0
    current_time = start_time

    while current_time < end_time:
        hour = current_time.hour
        matched_rule = None

        for rule in pricing_rules:
            start_hour = int(rule["start_hour"])
            end_hour = int(rule["end_hour"])

            if start_hour < end_hour:
                if start_hour <= hour < end_hour:
                    matched_rule = rule
                    break
            else:
                if hour >= start_hour or hour < end_hour:
                    matched_rule = rule
                    break

        if matched_rule is None:
            matched_rule = min_price_rule 

        rate_per_hour = matched_rule["rate_per_hour"]
        rate_per_minute = rate_per_hour / 60
        total_price += rate_per_minute
        current_time += timedelta(minutes=1)

    return {
        "table_id": str(table["_id"]),
        "start_time": start_time,
        "end_time": end_time,
        "total_seconds": total_seconds,
        "total_price": round(total_price, 2),
        "display_price": f"{round(total_price):,} ₫"
    }