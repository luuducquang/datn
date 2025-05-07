import type { Bookings, ResponseData, Tables } from "~/constant/api";
import { BookingUrl, TableUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllTable = async (): Promise<Tables[]> => {
    const res = await apiClient?.get(`${TableUrl}/get`);
    return res?.data;
};

export const getTableById = async (id: string): Promise<Tables> => {
    const res = await apiClient?.get(`${TableUrl}/get/${id}`);
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

export const checkBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<Boolean> => {
    const res = await apiClient?.post(
        `${BookingUrl}/check-availability-booking`,
        data
    );
    return res?.data;
};

export const searchBooking = async (
    data: Record<string, string | number | Boolean>
): Promise<ResponseData<Bookings>> => {
    const res = await apiClient?.post(`${BookingUrl}/search`, data);
    return res?.data;
};
