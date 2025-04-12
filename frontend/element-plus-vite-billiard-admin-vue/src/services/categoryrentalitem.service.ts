import { CategoryRentalItems, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { CategoryRentalItemUrl } from "~/constant/endpoints";

export const getAllCategoryRentalItem = async (): Promise<
    CategoryRentalItems[]
> => {
    const res = await apiClient?.get(`${CategoryRentalItemUrl}/get`);
    return res?.data;
};

export const searchCategoryRentalItem = async (
    data: Record<string, string | number>
): Promise<ResponseData<CategoryRentalItems>> => {
    const res = await apiClient?.post(`${CategoryRentalItemUrl}/search`, data);
    return res?.data;
};

export const createCategoryRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryRentalItems> => {
    const res = await apiClient?.post(`${CategoryRentalItemUrl}/add`, data);
    return res?.data;
};

export const updateCategoryRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryRentalItems> => {
    const res = await apiClient?.put(`${CategoryRentalItemUrl}/update`, data);
    return res?.data;
};

export const deleteCategoryRentalItem = async (
    id: String
): Promise<CategoryRentalItems> => {
    const res = await apiClient?.delete(
        `${CategoryRentalItemUrl}/delete/` + id
    );
    return res?.data;
};

export const getbyIdCategoryRentalItem = async (
    id: string
): Promise<CategoryRentalItems> => {
    const res = await apiClient?.get(`${CategoryRentalItemUrl}/get/` + id);
    return res?.data;
};
