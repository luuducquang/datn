import { Discounts, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { DiscountUrl } from "~/constant/endpoints";

export const getAllDiscount = async (): Promise<Discounts[]> => {
    const res = await apiClient?.get(`${DiscountUrl}/get`);
    return res?.data;
};

export const searchDiscount = async (
    data: Record<string, string | number>
): Promise<ResponseData<Discounts>> => {
    const res = await apiClient?.post(`${DiscountUrl}/search`, data);
    return res?.data;
};

export const createDiscount = async (
    data: Record<string, string | number | boolean>
): Promise<Discounts> => {
    const res = await apiClient?.post(`${DiscountUrl}/add`, data);
    return res?.data;
};

export const updateDiscount = async (
    data: Record<string, string | number | boolean>
): Promise<Discounts> => {
    const res = await apiClient?.put(`${DiscountUrl}/update`, data);
    return res?.data;
};

export const deleteDiscount = async (id: String): Promise<Discounts> => {
    const res = await apiClient?.delete(`${DiscountUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdDiscount = async (id: string): Promise<Discounts> => {
    const res = await apiClient?.get(`${DiscountUrl}/get/` + id);
    return res?.data;
};
