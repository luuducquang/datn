import { Rentals } from "~/constant/api";
import { RentalUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createRental = async (
    data: Rentals[]
): Promise<Rentals> => {
    const res = await apiClient?.post(`${RentalUrl}/add`, data);
    return res?.data;
};
