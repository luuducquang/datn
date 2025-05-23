from datetime import datetime, timedelta
from random import random
from typing import Dict, List
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection
import pytz
from config.database import database

tables_collection: Collection = database['Tables']
bookings_collection: Collection = database['Bookings']
billsells_collection: Collection = database['BillSells']
importbills_collection: Collection = database['ImportBills']
products_collection: Collection = database['Products']
orderitems_collection: Collection = database['OrderItems']
timesessions_collection: Collection = database['TimeSessions']
menuitems_collection: Collection = database['MenuItems']


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

    today_start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    today_bookings = bookings_collection.count_documents({
        "status": True,
        "start_time": {"$gte": today_start, "$lt": today_end}
    })

    month_start = datetime(current_year, current_month, 1)
    month_end = datetime(next_month_year, next_month, 1)

    month_bookings = bookings_collection.count_documents({
        "status": True,
        "start_time": {"$gte": month_start, "$lt": month_end}
    })

    total_bill_sells = billsells_collection.count_documents({"status": {"$ne": "Huỷ đơn"}})

    
    total_import_bills = importbills_collection.count_documents({})

    total_timesessions = timesessions_collection.count_documents({})

    
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

    sessions = timesessions_collection.find({
        "start_time": {"$exists": True},
        "end_time": {"$exists": True}
    })

    total_seconds = 0

    for session in sessions:
        start = session["start_time"]
        end = session["end_time"]
        
        if isinstance(start, datetime) and isinstance(end, datetime):
            delta = end - start
            total_seconds += delta.total_seconds()

    total_hours = total_seconds / 3600

    
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

    revenue_from_orderitems = list(orderitems_collection.aggregate([
        {"$group": {"_id": None, "total_price": {"$sum": "$total_price"}}}
    ]))
    total_revenue += revenue_from_orderitems[0]["total_price"] if revenue_from_orderitems else 0

    revenue_from_timesessions = list(timesessions_collection.aggregate([
        {"$group": {"_id": None, "total_price": {"$sum": "$price_paid"}}}
    ]))
    total_revenue += revenue_from_timesessions[0]["total_price"] if revenue_from_timesessions else 0

    revenue_from_booking = list(bookings_collection.aggregate([
        {"$match": {"status": True}},
        {"$group": {"_id": None, "total_price": {"$sum": "$money_paid"}}}
    ]))
    total_revenue += revenue_from_booking[0]["total_price"] if revenue_from_booking else 0

    
    
    return { "tongSoBan": total_tables,
         "banDangDung": tables_in_use,
         "banTrong": tables_available,
         "soLuongBookingHomNay": today_bookings,
        "soLuongBookingTrongThang": month_bookings,
         "hoaDonBan": total_bill_sells,
         "hoaDonNhap": total_import_bills,
         "hoaDonGioChoi": total_timesessions,
         "tongGioChoi": total_hours,
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
    # Lấy thời gian hiện tại theo UTC
    now_utc = datetime.now(pytz.UTC)

    # Xác định ngày đầu tháng và ngày đầu tháng kế tiếp theo UTC
    year = now_utc.year
    month = now_utc.month

    if month == 12:
        first_day_of_month = datetime(year=year, month=12, day=1, tzinfo=pytz.UTC)
        next_month = datetime(year=year+1, month=1, day=1, tzinfo=pytz.UTC)
    else:
        first_day_of_month = datetime(year=year, month=month, day=1, tzinfo=pytz.UTC)
        next_month = datetime(year=year, month=month+1, day=1, tzinfo=pytz.UTC)

    # Số ngày trong tháng
    last_day_of_month = (next_month - timedelta(days=1)).day

    days_in_month = []

    for day in range(1, last_day_of_month + 1):
        date = first_day_of_month.replace(day=day)
        next_date = date + timedelta(days=1)
        day_str = date.strftime("%Y-%m-%d")

        # Doanh thu từ orderitems (giả sử pay_date là datetime UTC)
        orderitems_revenue = list(orderitems_collection.aggregate([
            {"$match": {"pay_date": {"$gte": date, "$lt": next_date}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_price"}}}
        ]))
        food_orders_total = orderitems_revenue[0]['total_revenue'] if orderitems_revenue else 0

        # Doanh thu từ timesessions (end_time trong ngày)
        time_sessions_revenue = list(timesessions_collection.aggregate([
            {"$match": {"end_time": {"$gte": date, "$lt": next_date}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$price_paid"}}}
        ]))
        time_sessions_total = time_sessions_revenue[0]['total_revenue'] if time_sessions_revenue else 0

        # Doanh thu từ billsells (tránh trạng thái "Huỷ đơn"), giả sử sell_date là datetime UTC
        bill_sells_revenue = list(billsells_collection.aggregate([
            {"$match": {
                "sell_date": {"$gte": date, "$lt": next_date},
                "status": {"$ne": "Huỷ đơn"}
            }},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_price"}}}
        ]))
        bill_sells_total = bill_sells_revenue[0]['total_revenue'] if bill_sells_revenue else 0

        # Doanh thu từ bookings (status True và start_time trong ngày)
        revenue_from_booking = list(bookings_collection.aggregate([
            {"$match": {
                "status": True,
                "start_time": {"$gte": date, "$lt": next_date}
            }},
            {"$group": {"_id": None, "total_price": {"$sum": "$money_paid"}}}
        ]))
        booking_total = revenue_from_booking[0]["total_price"] if revenue_from_booking else 0

        total_revenue = food_orders_total + time_sessions_total + bill_sells_total + booking_total

        days_in_month.append({
            "date": day_str,
            "revenue": total_revenue
        })

    return days_in_month


def generate_playtime_data() -> List[Dict]:
    now_utc = datetime.now(pytz.UTC)
    year = now_utc.year
    month = now_utc.month

    if month == 12:
        first_day = datetime(year=year, month=12, day=1, tzinfo=pytz.UTC)
        next_month = datetime(year=year + 1, month=1, day=1, tzinfo=pytz.UTC)
    else:
        first_day = datetime(year=year, month=month, day=1, tzinfo=pytz.UTC)
        next_month = datetime(year=year, month=month + 1, day=1, tzinfo=pytz.UTC)

    last_day = (next_month - timedelta(days=1)).day
    results = []

    for day in range(1, last_day + 1):
        start_day = first_day.replace(day=day)
        end_day = start_day + timedelta(days=1)
        day_str = start_day.strftime("%Y-%m-%d")

        # Lọc các timesessions trong ngày
        sessions = list(timesessions_collection.find({
            "end_time": {"$gte": start_day, "$lt": end_day}
        }))

        total_seconds = 0
        for session in sessions:
            start = session.get("start_time")
            end = session.get("end_time")
            if start and end:
                duration = (end - start).total_seconds()
                total_seconds += max(duration, 0)

        total_hours = round(total_seconds / 3600, 2)

        results.append({
            "date": day_str,
            "hours_played": total_hours
        })

    return results


def get_quantity_item() -> List[Dict]:
    products = products_collection.find({}, {"item_name": 1, "quantity_available": 1})
    product_data = [
        {
            "product_name": p.get("item_name", "Không tên"),
            "quantity": p.get("quantity_available", 0)
        }
        for p in products
    ]

    menuitems = menuitems_collection.find({}, {"name": 1, "stock_quantity": 1})
    menuitem_data = [
        {
            "product_name": m.get("name", "Không tên"),
            "quantity": m.get("stock_quantity", 0)
        }
        for m in menuitems
    ]

    return product_data + menuitem_data