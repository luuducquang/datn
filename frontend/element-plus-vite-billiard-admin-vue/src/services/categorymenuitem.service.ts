import { CategoryMenuItems, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { CategoryMenuItemUrl } from "~/constant/endpoints";

export const getAllCategoryMenuItem = async (): Promise<CategoryMenuItems[]> => {
    const res = await apiClient?.get(`${CategoryMenuItemUrl}/get`);
    return res?.data;
};

export const searchCategoryMenuItem = async (
    data: Record<string, string | number>
): Promise<ResponseData<CategoryMenuItems>> => {
    const res = await apiClient?.post(`${CategoryMenuItemUrl}/search`, data);
    return res?.data;
};

export const createCategoryMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryMenuItems> => {
    const res = await apiClient?.post(`${CategoryMenuItemUrl}/add`, data);
    return res?.data;
};

export const updateCategoryMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<CategoryMenuItems> => {
    const res = await apiClient?.put(`${CategoryMenuItemUrl}/update`, data);
    return res?.data;
};

export const deleteCategoryMenuItem = async (
    id: String
): Promise<CategoryMenuItems> => {
    const res = await apiClient?.delete(`${CategoryMenuItemUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdCategoryMenuItem = async (
    id: string
): Promise<CategoryMenuItems> => {
    const res = await apiClient?.get(`${CategoryMenuItemUrl}/get/` + id);
    return res?.data;
};
