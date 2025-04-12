import { FoodOrders } from "~/constant/api";
import { FoodOrderUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createFoodOrder = async (data: FoodOrders): Promise<FoodOrders> => {
    const res = await apiClient?.post(`${FoodOrderUrl}/add`, data);
    return res?.data;
};
