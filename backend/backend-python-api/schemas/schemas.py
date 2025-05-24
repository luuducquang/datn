from fastapi import Body
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class Searchs(BaseModel):
    page: int = Body(...),
    pageSize: int = Body(...),
    search_term: Optional[str] = Body(None)
    category_name:Optional[str] = Body(None)
    status:Optional[bool] = Body(None)

class PaymentRequest(BaseModel):
    amount: float

class LoginRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class EmailRequest(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: str
    otp: str
    new_password: str

class Roles(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    role_name: str
    role_description: Optional[str] = None

class StockUpdateItem(BaseModel):
    item_id: str
    quantity: int

class Users(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    email: EmailStr
    password: str
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar: Optional[str] = None
    loyalty_points: Optional[int] = 0
    wallet: Optional[int] = 0
    role_name: str
    is_verified: bool = False
    otp: Optional[str] = None
    otp_expires_at: Optional[datetime] = None
    created_at: Optional[datetime]

class News(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    user_id: str
    title: str
    content: str
    image: str
    view: Optional[int] = 0
    status: bool

class Discounts(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    code: str
    discount_value: int
    decription: str
    quantity: Optional[int] = 0
    used_count: Optional[int] = 0
    status: bool

class Bookings(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    table_id: str
    user_id: str
    name: str
    phone: str
    start_time: datetime
    end_time: datetime
    money_paid:int
    status: Optional[bool]

class BookingItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    booking_id: str
    item_id: str
    name:str
    image:str
    quantity: int
    unit_price: int
    total_price: int

class RateBookings(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    booking_id: str
    user_id:str
    quality: int
    text:str

class TableTypes(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    table_type_name: str

class Tables(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    booking_id: str = None
    description: str
    table_number: int
    table_type_id: str
    status: Optional[bool]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class TableMenuItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    table_id:str
    item_id: str
    quantity: int
    unit_price: int
    total_price: int

class Suppliers(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    name: str
    phone:str
    address: str

class Manufactors(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    name: str
    phone:str
    address: str

class CategoryProducts(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    category_name: str

class Products (BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    manufactor_id: str
    category_id: str
    item_name: str
    image: str
    price: int
    price_reduction: int
    price_origin: int
    quantity_available: int = Field(default=0)
    view: int = Field(default=0)
    sales: int = Field(default=0)
    origin: str
    description: str
    description_detail: str

class CheckorUpdateQuantityRequest(BaseModel):
    ids: List[str]
    quantities: List[int]

class OrderMenuItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    order_id: str = None
    item_id: str
    quantity: int
    unit_price: int
    total_price: Optional[int]

class OrderItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    user_id: str
    table_id: str
    timesession_id: str
    pay_date: datetime = None
    total_price: Optional[int]
    menu_items: Optional[List[OrderMenuItems]] = None

class CategoryMenuItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    category_name: str

class MenuItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    category_id: Optional[str]
    name: str
    image:str
    stock_quantity: int
    price_origin: Optional[int]
    price: Optional[int]
    is_rental: bool

class TimeSessions(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    table_id: str
    start_time: datetime
    end_time: datetime
    price: Optional[int]
    price_paid: Optional[int]


class PricingRules(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    type_table_id: str
    rate_per_hour: int

class ImportItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    import_id: Optional[str] = None
    item_id: str
    quantity: int
    unit_price: int
    total_price: int

class ImportBills(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    user_id: str
    supplier_id:str
    import_date: datetime
    total_price: int
    import_items: Optional[List[ImportItems]] = None

class SellItems(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    sell_id: Optional[str] = None
    item_id: str
    quantity: int
    unit_price: int
    total_price: int

class BillSells(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    user_id: str
    sell_date: datetime
    name:str
    email:str
    phone:str
    address:str
    address_detail:str
    total_price: int
    status:str
    is_paid:bool
    created_at:Optional[datetime]
    sell_items: Optional[List[SellItems]] = None

class Carts(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    user_id:str
    item_id:str
    quantity:int
    status:bool
    
class Banners(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    description:str
    image:str


