import { apiClient } from "~/constant/request";

export const createPaypalOrder = async (
    amount: number
): Promise<{ id: string }> => {
    const res = await apiClient?.post("/paypal/create-order", { amount });
    return res?.data;
};

export const capturePaypalOrder = async (orderID: string): Promise<any> => {
    const res = await apiClient?.post(`/paypal/capture-order/${orderID}`);
    return res?.data;
};
