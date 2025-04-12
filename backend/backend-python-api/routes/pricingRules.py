from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from schemas.schemas import PricingRules
from service.pricingRules import ser_getbyid_pricingrule,ser_get_pricingrule,ser_delete_pricingrule, ser_insert_pricingrule, ser_update_pricingrule


router = APIRouter()

pricingrule_collection: Collection = database['PricingRules']

@router.get("/pricingrules/get")
async def get_pricingrule():
    return ser_get_pricingrule()

@router.get("/pricingrules/get/{pricingrule_id}")
async def get_pricingrule_by_id(pricingrule_id: str):
    return ser_getbyid_pricingrule(pricingrule_id)

@router.post("/pricingrules/add")
async def create_pricingrule(_data: PricingRules):
    _id = ser_insert_pricingrule(_data)
    return {"message": "Created successfully", "_id": _id}

@router.put("/pricingrules/update")
def edit_pricingrule(_data: PricingRules):
    result = ser_update_pricingrule(_data, pricingrule_collection)
    return result

@router.delete("/pricingrules/delete/{pricingrule_id}")
def remove_pricingrule(pricingrule_id: str):
    response = ser_delete_pricingrule(pricingrule_id, pricingrule_collection)
    return response