import { CategoryProducts, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { CategoryProductUrl } from "~/constant/endpoints";

export const getAllCategoryProduct = async (): Promise<CategoryProducts[]> => {
    const res = await apiClient?.get(`${CategoryProductUrl}/get`);
    return res?.data;
};

export const searchCategoryProduct = async (
    data: Record<string, string | number>
): Promise<ResponseData<CategoryProducts>> => {
    const res = await apiClient?.post(`${CategoryProductUrl}/search`, data);
    return res?.data;
};

export const createCategoryProduct = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryProducts> => {
    const res = await apiClient?.post(`${CategoryProductUrl}/add`, data);
    return res?.data;
};

export const updateCategoryProduct = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryProducts> => {
    const res = await apiClient?.put(`${CategoryProductUrl}/update`, data);
    return res?.data;
};

export const deleteCategoryProduct = async (
    id: String
): Promise<CategoryProducts> => {
    const res = await apiClient?.delete(`${CategoryProductUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdCategoryProduct = async (
    id: string
): Promise<CategoryProducts> => {
    const res = await apiClient?.get(`${CategoryProductUrl}/get/` + id);
    return res?.data;
};
