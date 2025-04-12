import { ResponseData, Banner } from "~/constant/api";
import { BannerUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const searchBanner = async (
    data: Record<string, string | number>
): Promise<ResponseData<Banner>> => {
    const res = await apiClient?.post(`${BannerUrl}/search`, data);
    return res?.data;
};

export const createBanner = async (
    data: Record<string, string | number>
): Promise<Banner> => {
    const res = await apiClient?.post(`${BannerUrl}/add`, data);
    return res?.data;
};

export const updateBanner = async (
    data: Record<string, string | number>
): Promise<Banner> => {
    const res = await apiClient?.put(`${BannerUrl}/update`, data);
    return res?.data;
};

export const deleteBanner = async (id: string): Promise<Banner> => {
    const res = await apiClient?.delete(`${BannerUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdBanner = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${BannerUrl}/get/` + id);
    return res?.data;
};
