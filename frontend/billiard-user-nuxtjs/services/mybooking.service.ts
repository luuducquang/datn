import type { Bookings, BookingItems } from "~/constant/api";
import { BookingItemUrl, BookingUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getBookingByID = async (id: string): Promise<Bookings[]> => {
    const res = await apiClient?.get(
        `${BookingUrl}/get-booking-by-userid/` + id
    );
    return res?.data;
};

export const getDetailBookingItemById = async (id: string): Promise<BookingItems[]> => {
    const res = await apiClient?.get(`${BookingItemUrl}/get/` + id);
    return res?.data;
};
