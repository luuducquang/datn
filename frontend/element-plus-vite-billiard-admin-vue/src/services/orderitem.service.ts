import { OrderItems, ResponseData } from "~/constant/api";
import { OrderItemUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createOrderItem = async (
    data: OrderItems
): Promise<OrderItems> => {
    const res = await apiClient?.post(`${OrderItemUrl}/add`, data);
    return res?.data;
};

export const searchOrderItem = async (
    data: Record<string, string | number>
): Promise<ResponseData<OrderItems>> => {
    const res = await apiClient?.post(`${OrderItemUrl}/search`, data);
    return res?.data;
};