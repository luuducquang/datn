import type { Banner } from "~/constant/api";
import { BannerUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllImagesBanner = async (): Promise<Banner[]> => {
    const res = await apiClient?.get(`${BannerUrl}/get`);
    return res?.data;
};
