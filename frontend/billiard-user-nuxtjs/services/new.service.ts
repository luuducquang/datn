import type { News, ResponseData } from "~/constant/api";
import { NewUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getNews = async (
    data: Record<string, string | number>
): Promise<ResponseData<News>> => {
    const res = await apiClient?.post(`${NewUrl}/search`, data);
    return res?.data;
};

export const getNewById = async (id: string): Promise<News> => {
    const res = await apiClient?.get(`${NewUrl}/get/` + id);
    return res?.data;
};
