import { RateBookings, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { RateBookingUrl } from "~/constant/endpoints";

export const getAllRateBooking = async (): Promise<RateBookings[]> => {
    const res = await apiClient?.get(`${RateBookingUrl}/get`);
    return res?.data;
};

export const searchRateBooking = async (
    data: Record<string, string | number>
): Promise<ResponseData<RateBookings>> => {
    const res = await apiClient?.post(`${RateBookingUrl}/search`, data);
    return res?.data;
};

export const createRateBooking = async (
    data: Record<string, string | number | boolean>
): Promise<RateBookings> => {
    const res = await apiClient?.post(`${RateBookingUrl}/add`, data);
    return res?.data;
};

export const updateRateBooking = async (
    data: Record<string, string | number | boolean>
): Promise<RateBookings> => {
    const res = await apiClient?.put(`${RateBookingUrl}/update`, data);
    return res?.data;
};

export const deleteRateBooking = async (id: String): Promise<RateBookings> => {
    const res = await apiClient?.delete(`${RateBookingUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdRateBooking = async (id: string): Promise<RateBookings> => {
    const res = await apiClient?.get(`${RateBookingUrl}/get/` + id);
    return res?.data;
};
