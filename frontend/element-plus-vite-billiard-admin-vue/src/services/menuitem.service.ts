import { MenuItems, ResponseData } from "~/constant/api";
import { MenuItemUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllMenuItem = async (): Promise<MenuItems[]> => {
    const res = await apiClient?.get(`${MenuItemUrl}/get`);
    return res?.data;
};

export const searchMenuItem = async (
    data: Record<string, string | number>
): Promise<ResponseData<MenuItems>> => {
    const res = await apiClient?.post(`${MenuItemUrl}/search`, data);
    return res?.data;
};

export const createMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<MenuItems> => {
    const res = await apiClient?.post(`${MenuItemUrl}/add`, data);
    return res?.data;
};

export const updateMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<MenuItems> => {
    const res = await apiClient?.put(`${MenuItemUrl}/update`, data);
    return res?.data;
};

export const deleteMenuItem = async (id: string): Promise<MenuItems> => {
    const res = await apiClient?.delete(`${MenuItemUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdMenuItems = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${MenuItemUrl}/get/` + id);
    return res?.data;
};
