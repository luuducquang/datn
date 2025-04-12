import { apiClient } from "~/constant/request";

export const uploadImage = async (data: FormData): Promise<boolean> => {
    const res = await apiClient?.post(`upload`, data);
    return res?.data;
};
