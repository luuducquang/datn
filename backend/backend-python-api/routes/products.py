from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import Products, Searchs, CheckorUpdateQuantityRequest
from sercurity import require_role
from service.products import ser_check_and_update_quantities, ser_check_quantities, ser_getbyid_product,ser_search_product,ser_get_product,ser_delete_product, ser_insert_product, ser_update_product


router = APIRouter()

product_collection: Collection = database['Products']

@router.get("/products/get")
async def get_product():
    return ser_get_product()

@router.get("/products/get/{product_id}")
async def get_product_by_id(product_id: str):
    return ser_getbyid_product(product_id)

# @router.post("/products/search", dependencies=[Depends(require_role(["ADMIN"]))])
@router.post("/products/search")
async def search_product(_data:Searchs):
    return ser_search_product(_data)

@router.post("/products/add")
async def create_product(_data: Products):
    _id = ser_insert_product(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/products/update")
def edit_product(_data: Products):
    result = ser_update_product(_data, product_collection)
    return result

@router.delete("/products/delete/{product_id}")
def remove_product(product_id: str):
    response = ser_delete_product(product_id, product_collection)
    return response

@router.post("/products/check-quantities")
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

@router.post("/products/check-and-update-quantities")
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