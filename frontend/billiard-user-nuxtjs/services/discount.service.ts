import { apiClient } from "~/constant/request";
import type { Discounts } from "~/constant/api";
import { DiscountUrl } from "~/constant/endpoints";

export const getAllDiscount = async (): Promise<Discounts[]> => {
    const res = await apiClient?.get(`${DiscountUrl}/get/`);
    return res?.data;
};

export const getDiscountByCode = async (id: string): Promise<number> => {
    const res = await apiClient?.get(`${DiscountUrl}/code/` + id);
    return res?.data;
};


export const getDiscountUseCode = async (id: string): Promise<number> => {
    const res = await apiClient?.post(`${DiscountUrl}/use/` + id);
    return res?.data;
};