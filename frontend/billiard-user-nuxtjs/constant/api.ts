export interface ResponseData<T> {
    data: T[];
    page: number;
    pageSize: number;
    totalItems: number;
}

export interface OptionSelect {
    value: string | number;
    label: string;
    price?: number;
    gia?: number;
    hinhAnh?: string;
}

export interface TableTypes {
    _id?: string;
    table_type_name: string;
}

export interface Tables {
    _id?: string;
    description: string;
    table_number: number;
    table_type_id: string;
    name: string;
    phone: string;
    status: boolean;
    start_date?: String;
    end_date?: String;
    tabletype?: TableTypes;
    pricingrule?: PricingRules[];
}

export interface Discounts {
    _id?: string;
    code: String;
    discount_value: Number;
    decription: String;
    quantity: Number;
    used_count: Number;
    status: boolean;
}

export interface Bookings {
    _id?: string;
    table_id: string;
    user_id: string;
    name: string;
    phone: string;
    start_time: Date;
    end_time: Date;
    money_paid: number;
    status: Boolean;
    created_at: Date;
    table?: Tables;
}

export interface BookingItems {
    _id?: string;
    booking_id: string;
    item_id: string;
    image: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    name?: string;
}

export interface RateBookings {
    _id?: string;
    booking_id: string;
    user_id: string;
    quality: number;
    text: string;
}

export interface CategoryMenuItems {
    _id?: string;
    category_name: string;
}

export interface MenuItems {
    _id?: string;
    name: string;
    image: string;
    stock_quantity: number;
    price: number;
    category_id: string;
    categorymenuitem?: CategoryMenuItems;
}

export interface PricingRules {
    _id?: string;
    type_table_id: string;
    start_hour: number;
    end_hour: number;
    rate_per_hour: number;
    tabletype?: TableTypes;
}

export interface Products {
    _id?: string;
    manufactor_id: string;
    category_id: string;
    item_name: string;
    image: string;
    price_origin: number;
    price: number;
    price_reduction: number;
    quantity_available: number;
    view?: number;
    sales?: number;
    origin: string;
    description: string;
    description_detail: string;
    categoryproduct?: CategoryProducts;
    manufactor?: Manufactors;
}

export interface CheckorUpdateQuantityRequest {
    ids: string[];
    quantities: number[];
}

export interface CategoryProducts {
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
    wallet: number;
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
    is_paid: boolean;
    created_at?: string;
    sell_items?: SellItems[];
}

export interface SellItems {
    id?: string;
    sell_id?: string;
    item_id: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    product?: Products;
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
    wallet: number;
    role_name: string;
    token?: string;
}

export interface Cart {
    _id?: string;
    user_id: string;
    item_id: string;
    quantity: number;
    status: boolean;
    product?: Products;
}
