import type { BookingItems } from "~/constant/api";
import { BookingItemUrl} from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getBookingItemByIDBooking = async (id: string): Promise<BookingItems[]> => {
    const res = await apiClient?.get(`${BookingItemUrl}/get/${id}`);
    return res?.data;
};
