import { News, ResponseData } from "~/constant/api";
import { NewUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const searchNews = async (
    data: Record<string, string | number>
): Promise<ResponseData<News>> => {
    const res = await apiClient?.post(`${NewUrl}/search`, data);
    return res?.data;
};

export const createNew = async (
    data: Record<string, string | number | boolean>
): Promise<News> => {
    const res = await apiClient?.post(`${NewUrl}/add`, data);
    return res?.data;
};

export const updateNew = async (
    data: Record<string, string | number | boolean>
): Promise<News> => {
    const res = await apiClient?.put(`${NewUrl}/update`, data);
    return res?.data;
};

export const deleteNew = async (id: string): Promise<News> => {
    const res = await apiClient?.delete(`${NewUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdNews = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${NewUrl}/get/` + id);
    return res?.data;
};
