import { apiClient } from "~/constant/request";

export const createMomoOrder = async (
    amount: number
): Promise<any> => {
    const res = await apiClient?.post("/momo/create-payment", { amount });
    return res?.data;
};


export const captureMomoOrder = async (orderID: string): Promise<any> => {
    const res = await apiClient?.get(`/momo/status/${orderID}`);
    return res?.data;
};
