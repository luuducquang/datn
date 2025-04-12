from fastapi import APIRouter, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import RentalItems, Searchs, CheckorUpdateQuantityRequest
from service.rentalItems import ser_check_and_update_quantities, ser_check_quantities, ser_getbyid_rentalitem,ser_search_rentalitem,ser_get_rentalitem,ser_delete_rentalitem, ser_insert_rentalitem, ser_update_rentalitem


router = APIRouter()

rentalitem_collection: Collection = database['RentalItems']

@router.get("/rentalitems/get")
async def get_rentalitem():
    return ser_get_rentalitem()

@router.get("/rentalitems/get/{rentalitem_id}")
async def get_rentalitem_by_id(rentalitem_id: str):
    return ser_getbyid_rentalitem(rentalitem_id)

@router.post("/rentalitems/search")
async def search_rentalitem(_data:Searchs):
    return ser_search_rentalitem(_data)

@router.post("/rentalitems/add")
async def create_rentalitem(_data: RentalItems):
    _id = ser_insert_rentalitem(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/rentalitems/update")
def edit_rentalitem(_data: RentalItems):
    result = ser_update_rentalitem(_data, rentalitem_collection)
    return result

@router.delete("/rentalitems/delete/{rentalitem_id}")
def remove_rentalitem(rentalitem_id: str):
    response = ser_delete_rentalitem(rentalitem_id, rentalitem_collection)
    return response

@router.post("/rentalitems/check-quantities")
async def check_and_update_quantities(data: CheckorUpdateQuantityRequest):
    if len(data.ids) != len(data.quantities):
        raise HTTPException(status_code=400, detail="List of IDs and quantities must have the same length")

    insufficient_items = ser_check_quantities(data.ids, data.quantities)

    if insufficient_items:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Some items do not have enough quantity.",
                "insufficient_items": insufficient_items,
            }
        )

    return True

@router.post("/rentalitems/check-and-update-quantities")
async def check_and_update_quantities(data: CheckorUpdateQuantityRequest):
    if len(data.ids) != len(data.quantities):
        raise HTTPException(status_code=400, detail="List of IDs and quantities must have the same length")

    insufficient_items = ser_check_and_update_quantities(data.ids, data.quantities)

    if insufficient_items:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Some items do not have enough quantity.",
                "insufficient_items": insufficient_items,
            }
        )

    return {"message": "Quantities updated successfully"}