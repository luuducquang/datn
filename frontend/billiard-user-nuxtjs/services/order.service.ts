import type { BillSells } from "~/constant/api";
import { BillSellUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const sendOrder = async (
    data: BillSells
): Promise<BillSells> => {
    const res = await apiClient?.post(`${BillSellUrl}/add`, data);
    return res?.data;
};
