from datetime import datetime, timedelta
from random import random
from typing import Dict, List
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
from config.database import database

tables_collection: Collection = database['Tables']
bookings_collection: Collection = database['Bookings']
billsells_collection: Collection = database['BillSells']
importbills_collection: Collection = database['ImportBills']
products_collection: Collection = database['Products']
rentals_collection: Collection = database['Rentals']
orderitems_collection: Collection = database['OrderItems']
timesessions_collection: Collection = database['TimeSessions']


def ser_get_info_overview():
    today = datetime.today()  
    current_month = today.month
    current_year = today.year

   
    if current_month == 12:
        next_month = 1
        next_month_year = current_year + 1
    else:
        next_month = current_month + 1
        next_month_year = current_year

    
    total_tables = tables_collection.count_documents({})

    
    tables_in_use = tables_collection.count_documents({"status": True})

    
    tables_available = tables_collection.count_documents({"status": False})

    
    today_bookings = bookings_collection.count_documents({"start_time": {"$gte": today}})

    
    total_bill_sells = billsells_collection.count_documents({"status": {"$ne": "Huỷ đơn"}})

    
    total_import_bills = importbills_collection.count_documents({})

    
    total_customers = len(bookings_collection.distinct("phone"))

    
    new_customers_in_month = len(
        bookings_collection.distinct(
            "phone",
            {
                "start_time": {
                    "$gte": datetime(current_year, current_month, 1),
                    "$lt": datetime(next_month_year, next_month, 1)
                }
            }
        )
    )

    
    canceled_orders = billsells_collection.count_documents({"status": "Huỷ đơn"})

    
    pending_orders = billsells_collection.count_documents({"status": "Đang xử lý"})

    
    shipping_orders = billsells_collection.count_documents({"status": "Đang giao hàng"})

    
    completed_orders = billsells_collection.count_documents({"status": {"$in": ["Đã giao hàng", "Hoàn tất"]}})

    
    returned_orders = billsells_collection.count_documents({"status": {"$in": ["Đổi hàng", "Trả hàng"]}})

    
    total_product_views = list(products_collection.aggregate([{"$group": {"_id": None, "total_views": {"$sum": "$view"}}}]))
    total_product_views = total_product_views[0]["total_views"] if total_product_views else 0

    
    total_import_value = list(importbills_collection.aggregate([{"$group": {"_id": None, "total_price": {"$sum": "$total_price"}}}]))
    total_import_value = total_import_value[0]["total_price"] if total_import_value else 0

    
    total_revenue = 0
    revenue_from_bills = list(billsells_collection.aggregate([
        {"$match": {"status": {"$ne": "Huỷ đơn"}}},
        {"$group": {"_id": None, "total_price": {"$sum": "$total_price"}}}
    ]))
    total_revenue += revenue_from_bills[0]["total_price"] if revenue_from_bills else 0

    revenue_from_rentals = list(rentals_collection.aggregate([
        {"$group": {"_id": None, "total_price": {"$sum": "$price"}}}
    ]))
    total_revenue += revenue_from_rentals[0]["total_price"] if revenue_from_rentals else 0

    revenue_from_orderitems = list(orderitems_collection.aggregate([
        {"$group": {"_id": None, "total_price": {"$sum": "$total_price"}}}
    ]))
    total_revenue += revenue_from_orderitems[0]["total_price"] if revenue_from_orderitems else 0

    revenue_from_timesessions = list(timesessions_collection.aggregate([
        {"$group": {"_id": None, "total_price": {"$sum": "$price"}}}
    ]))
    total_revenue += revenue_from_timesessions[0]["total_price"] if revenue_from_timesessions else 0

    
    
    return { "tongSoBan": total_tables,
         "banDangDung": tables_in_use,
         "banTrong": tables_available,
         "soLuongBanNgay": today_bookings,
         "hoaDonBan": total_bill_sells,
         "hoaDonNhap": total_import_bills,
         "khachHang": total_customers,
         "khachHangMoi": new_customers_in_month,
         "donHuy": canceled_orders,
         "donCho": pending_orders,
         "dangGiao": shipping_orders,
         "hoantat": completed_orders,
         "doiTra": returned_orders,
         "luotXem": total_product_views,
         "tienNhap": total_import_value,
         "doanhThu": total_revenue}
    

def generate_revenue_data() -> List[Dict]:
    today = datetime.today()
    
    
    if today.month == 12:
        first_day_of_month = today.replace(year=today.year, month=12, day=1)
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        first_day_of_month = today.replace(month=today.month, day=1)
        next_month = today.replace(month=today.month + 1, day=1)
    
    
    last_day_of_month = (next_month - timedelta(days=1)).day
    
    days_in_month = []
    
    for day in range(1, last_day_of_month + 1):
        date = first_day_of_month.replace(day=day)
        day_str = date.strftime("%Y-%m-%d")
        
        
        rentals_revenue = list(rentals_collection.aggregate([
            {"$match": {"rental_date": {"$eq": date}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$price"}}}
        ]))
        
        rentals_total = rentals_revenue[0]['total_revenue'] if rentals_revenue else 0
        
        food_orders_revenue = list(orderitems_collection.aggregate([
            {"$match": {"pay_date": {"$eq": date}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_price"}}}
        ]))
        
        food_orders_total = food_orders_revenue[0]['total_revenue'] if food_orders_revenue else 0
        
        time_sessions_revenue = list(timesessions_collection.aggregate([
            {"$match": {"start_time": {"$gte": date, "$lt": date + timedelta(days=1)}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$price"}}}
        ]))
        
        time_sessions_total = time_sessions_revenue[0]['total_revenue'] if time_sessions_revenue else 0
        
        bill_sells_revenue = list(billsells_collection.aggregate([
            {"$match": {"sell_date": {"$eq": date}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_price"}}}
        ]))
        
        bill_sells_total = bill_sells_revenue[0]['total_revenue'] if bill_sells_revenue else 0
        
        total_revenue = rentals_total + food_orders_total + time_sessions_total + bill_sells_total
        
        days_in_month.append({
            "date": day_str,
            "revenue": total_revenue
        })
    
    return days_in_month
