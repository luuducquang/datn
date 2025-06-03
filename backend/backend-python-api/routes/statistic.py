from typing import Dict, List
from fastapi import APIRouter
from pymongo.collection import Collection
from service.statistic import get_imports_by_current_year_service,ser_get_info_overview,generate_revenue_data,generate_playtime_data,get_quantity_item,get_low_stock_products,generate_weekly_revenue_data,generate_yearly_revenue_data


router = APIRouter()

@router.get("/statistic/get")
def get_overview():
    return ser_get_info_overview()

@router.get("/statistic/monthly-revenue")
def get_monthly_revenue():
    return generate_revenue_data()

@router.get("/statistic/weekly-revenue")
def get_weekly_revenue():
    return generate_weekly_revenue_data()

@router.get("/statistic/yearly-revenue")
def get_yearly_revenue():
    return generate_yearly_revenue_data()

@router.get("/statistic/playtime")
def get_daily_playtime():
    return generate_playtime_data()

@router.get("/statistic/inventory-item")
def get_inventory_item():
    return get_quantity_item()

@router.get("/statistic/low-stock")
def get_low_stock_item():
    return get_low_stock_products()

@router.get("/statistic/imports-by-current-year")
def get_imports_by_current_year():
    return get_imports_by_current_year_service()