import { OrderMenuItems, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { OrderMenuItemUrl } from "~/constant/endpoints";

export const getbyOrderId = async (id: string): Promise<OrderMenuItems[]> => {
    const res = await apiClient?.get(`${OrderMenuItemUrl}/get/` + id);
    return res?.data;
};
