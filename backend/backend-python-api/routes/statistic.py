from typing import Dict, List
from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from service.statistic import ser_get_info_overview,generate_revenue_data


router = APIRouter()

@router.get("/statistic/get")
def get_overview():
    return ser_get_info_overview()

@router.get("/statistic/monthly-revenue")
def get_monthly_revenue():
    return generate_revenue_data()