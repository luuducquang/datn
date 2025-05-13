export interface ResponseData<T> {
    data: T[];
    page: number;
    pageSize: number;
    totalItems: number;
}

export interface Banner {
    _id?: string;
    description: string;
    image: string;
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

export interface Product {
    maSanPham?: number;
    tenSanPham: string;
    anhDaiDien: string;
    giaGiam: number;
    soLuong: number;
    luotBan: number;
    danhGia: number;
    trongLuong: string;
    tenDanhMuc?: string;
    tendanhmucuudai?: string;
    trangThai: boolean;
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
    start_date?: Date | string;
    end_date?: Date | string;
    tabletype?: TableTypes;
    pricingrule?: PricingRules;
}

export interface TableMenuItems {
    _id?: string;
    table_id: string;
    item_id: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    menuitem?: MenuItems;
}

export interface TableRentalItems {
    _id?: string;
    table_id: string;
    item_id: string;
    unit_price: number;
    rentalitem?: RentalItems;
    start_time: Date | string;
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

export interface CategoryMenuItems {
    _id?: string;
    category_name: string;
}

export interface CategoryRentalItems {
    _id?: string;
    category_name: string;
}

export interface Roles {
    _id?: string;
    role_name: string;
    role_description: string;
}

export interface Users {
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

export interface Manufactors {
    _id?: string;
    name: string;
    phone: string;
    address: string;
}

export interface Suppliers {
    _id?: string;
    name: string;
    phone: string;
    address: string;
}

export interface PricingRules {
    _id?: string;
    type_table_id: string;
    rate_per_hour: number;
    rate_per_minute: number;
    tabletype?: TableTypes;
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

export interface Discounts {
    _id?: string;
    code: String;
    discount_value: Number;
    decription: String;
    quantity: Number;
    used_count: Number;
    status: boolean;
}

export interface RateBookings {
    _id?: string;
    booking_id: string;
    user_id: string;
    quality: number;
    text: string;
}

export interface Rentals {
    _id?: string;
    user_id: string;
    item_id: string;
    rental_date: Date | string;
    return_date: Date | string;
    price: number;
    status: boolean;
}

export interface FoodOrders {
    _id?: string;
    user_id: string;
    table_id: string;
    item_id: string;
    pay_date: Date | string;
    quantity: number;
    unit_price: number;
    total_price: number;
}

export interface TimeSessions {
    _id?: string;
    table_id: string;
    start_time: Date | string;
    end_time: Date | string;
    price: number;
}

export interface RentalItems {
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

export interface SellItems {
    _id?: string;
    sell_id: string;
    item_id: string;
    quantity: number;
    unit_price: number;
    total_price: number;
    rentalitem?: RentalItems[];
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
    user_info?: Users[];
}

export interface TableBillSell {
    maChiTietHoaDon?: string;
    stt?: number;
    maSanPham: string;
    hinhAnh?: string;
    soLuong: number | string;
    donGia: number;
    tongTien: number;
}

export interface ImportBills {
    _id?: string;
    user_id: string;
    supplier_id: string;
    import_date: Date | string;
    total_price: number;
    import_items?: ImportItems[];
    user_info?: Users[];
    supplier_info?: Suppliers[];
}

export interface ImportItems {
    _id?: string;
    import_id?: string;
    item_id: string;
    quantity: number;
    unit_price: number;
    total_price: number;
}

export interface TableImportBill {
    maChiTietHoaDon?: string;
    stt?: number;
    maSanPham: string;
    hinhAnh?: string;
    soLuong: number | string;
    donGia: number;
    tongTien: number;
}

export interface OptionSelect {
    value: string | number;
    label: string;
    price?: number;
    gia?: number;
    hinhAnh?: string;
}
