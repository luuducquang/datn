import type {
    BookingItems,
    Bookings,
    MenuItems,
    ResponseData,
    Tables,
} from "~/constant/api";
import {
    BookingItemUrl,
    BookingUrl,
    MenuItemUrl,
    TableUrl,
} from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllTable = async (): Promise<Tables[]> => {
    const res = await apiClient?.get(`${TableUrl}/get`);
    return res?.data;
};

export const getTableById = async (id: string): Promise<Tables> => {
    const res = await apiClient?.get(`${TableUrl}/get/${id}`);
    return res?.data;
};

export const updateStatusBooking = async (id: string): Promise<Tables> => {
    const res = await apiClient?.put(`${BookingUrl}/update-status/${id}`);
    return res?.data;
};

export const updateTableStatus = async (id: string): Promise<Tables> => {
    const res = await apiClient?.put(`${TableUrl}/updatestatus/${id}`);
    return res?.data;
};

export const createBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<Bookings> => {
    const res = await apiClient?.post(`${BookingUrl}/add`, data);
    return res?.data;
};

export const createBookingItem = async (
    data: Record<string, string | number | Boolean>
): Promise<BookingItems> => {
    const res = await apiClient?.post(`${BookingItemUrl}/add`, data);
    return res?.data;
};

export const checkBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<Boolean> => {
    const res = await apiClient?.post(
        `${BookingUrl}/check-availability-booking`,
        data
    );
    return res?.data;
};

export const getBookingByID = async (id: string): Promise<Bookings[]> => {
    const res = await apiClient?.get(`${BookingUrl}/get-by-table/${id}`);
    return res?.data;
};

export const getAllMenuItem = async (): Promise<MenuItems[]> => {
    const res = await apiClient?.get(`${MenuItemUrl}/get`);
    return res?.data;
};
