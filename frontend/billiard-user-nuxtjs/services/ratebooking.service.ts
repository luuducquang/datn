import type { RateBookings } from "~/constant/api";
import { RateBookingUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createRateBooking = async (data: RateBookings): Promise<RateBookings> => {
    const res = await apiClient?.post(`${RateBookingUrl}/add`, data);
    return res?.data;
};

export const getRateBookingByIdBooking = async (id: string): Promise<RateBookings> => {
    const res = await apiClient?.get(
        `${RateBookingUrl}/booking/` + id
    );
    return res?.data;
};