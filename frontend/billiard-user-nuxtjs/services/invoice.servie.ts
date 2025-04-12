import type { BillSells, SellItems } from "~/constant/api";
import { BillSellUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getInvoiceAll = async (id: string): Promise<BillSells[]> => {
    const res = await apiClient?.get(`${BillSellUrl}/get/` + id);
    return res?.data;
};

export const getInvoiceById = async (id: string): Promise<SellItems[]> => {
    const res = await apiClient?.get(`${BillSellUrl}/get-billsell-id/` + id);
    return res?.data;
};
