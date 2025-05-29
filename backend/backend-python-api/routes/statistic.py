from typing import Dict, List
from fastapi import APIRouter
from pymongo.collection import Collection
from config.database import database
from service.statistic import ser_get_info_overview,generate_revenue_data,generate_playtime_data,get_quantity_item,get_low_stock_products


router = APIRouter()

@router.get("/statistic/get")
def get_overview():
    return ser_get_info_overview()

@router.get("/statistic/monthly-revenue")
def get_monthly_revenue():
    return generate_revenue_data()

@router.get("/statistic/playtime")
def get_daily_playtime():
    return generate_playtime_data()

@router.get("/statistic/inventory-item")
def get_inventory_item():
    return get_quantity_item()

@router.get("/statistic/low-stock")
def get_low_stock_item():
    return get_low_stock_products()