import type {
    BookingItems,
    Bookings,
    ResponseData,
    Tables,
} from "~/constant/api";
import { BookingItemUrl, BookingUrl, TableUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const searchBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<ResponseData<Bookings>> => {
    const res = await apiClient?.post(`${BookingUrl}/search`, data);
    return res?.data;
};

export const createBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<Bookings> => {
    const res = await apiClient?.post(`${BookingUrl}/add`, data);
    return res?.data;
};

export const updateBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<Bookings> => {
    const res = await apiClient?.put(`${BookingUrl}/update`, data);
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

export const checkAvailableTables = async (
    data: Record<string, string | number | Boolean>
): Promise<string> => {
    const res = await apiClient?.post(`${BookingUrl}/available`, data);
    return res?.data;
};

export const setFalseStatusBooking = async (id: string): Promise<Bookings> => {
    const res = await apiClient?.put(`${BookingUrl}/false-status/${id}`);
    return res?.data;
};

export const getBookingByIDTable = async (id: string): Promise<Bookings[]> => {
    const res = await apiClient?.get(`${BookingUrl}/get-by-table/${id}`);
    return res?.data;
};

export const getBookingByIDBooking = async (id: string): Promise<Bookings> => {
    const res = await apiClient?.get(`${BookingUrl}/get-by-id/${id}`);
    return res?.data;
};

export const deleteBooking = async (id: String): Promise<Tables> => {
    const res = await apiClient?.delete(`${BookingUrl}/delete/` + id);
    return res?.data;
};

export const getBookingAvailable = async (): Promise<BookingItems[]> => {
    const res = await apiClient?.get(`${BookingUrl}/get-booking-active`);
    return res?.data;
};
