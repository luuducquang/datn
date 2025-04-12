export interface ResponseData<T> {
    data: T[];
    page: number;
    pageSize: number;
    totalItems: number;
}

export interface TableTypes {
    _id?: string;
    table_type_name: string;
}

export interface Tables {
    _id?: string;
    table_number: number;
    table_type_id: string;
    status: boolean;
    start_date?: String;
    end_date?: String;
    tabletype?: TableTypes;
    pricingrule?: PricingRules;
}

export interface Bookings {
    _id?: string;
    table_id: string;
    name: string;
    phone: string;
    start_time: Date;
    end_time: Date;
    status: Boolean;
    created_at: Date;
    table?: Tables;
}

export interface PricingRules {
    _id?: string;
    type_table_id: string;
    rate_per_hour: number;
    rate_per_minute: number;
    tabletype?: TableTypes;
}

export interface Product {
    _id?: string;
    manufactor_id: string;
    category_id: string;
    item_name: string;
    image: string;
    price: number;
    price_reduction: number;
    rental_price_day: number;
    rental_price_hours: number;
    quantity_available: number;
    view?: number;
    sales?: number;
    origin: string;
    description: string;
    description_detail: string;
    categoryrentalitem?: CategoryRentalItems;
    manufactor?: Manufactors;
}

export interface CheckorUpdateQuantityRequest{
    ids: string[]
    quantities: number[]
}

export interface CategoryRentalItems {
    _id?: string;
    category_name: string;
}

export interface Manufactors {
    _id?: string;
    name: string;
    phone: string;
    address: string;
}

export interface User {
    _id?: string;
    username: string;
    password: string;
    fullname: string;
    email: string;
    phone: string;
    address: string;
    avatar: string;
    loyalty_points: number;
    role_name: string;
    token?: string;
}

export interface ImgDetail {
    id?: number;
    maSanPham?: number;
    linkAnh: string;
    status: number;
}

export interface BillSells {
    _id?: string;
    user_id: string;
    sell_date: Date | string;
    name: string;
    email: string;
    phone: string;
    address: string;
    address_detail: string;
    total_price: number;
    status: string;
    sell_items?: SellItems[];
}

export interface SellItems {
    id?: string ;
    sell_id?: string;
    item_id: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    rentalitem: Product;
}

export interface News {
    _id?: string;
    user_id?: string;
    title: string;
    content: string;
    image: string;
    view?: number;
    status: boolean;
    fullname?: string;
}

export interface Category {
    _id?: string;
    category_name: string;
}

export interface CategoryOffer {
    madanhmucuudai?: number;
    tendanhmucuudai: string;
    dacBiet: boolean;
    noiDung: string;
}

export interface Banner {
    _id?: string;
    description: string;
    image: string;
}

export interface Account {
    _id?: string;
    username: string;
    password: string;
    fullname: string;
    email: string;
    phone: string;
    address: string;
    avatar: string;
    loyalty_points: number;
    role_name: string;
    token?: string;
}

export interface Cart {
    _id?: string;
    user_id: string;
    item_id: string;
    quantity: number;
    status: boolean;
    rentalitem?: Product;
}
