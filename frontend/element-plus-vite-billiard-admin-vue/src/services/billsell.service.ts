import {
    BillSells,
    RentalItems,
    ResponseData,
    SellItems,
} from "~/constant/api";
import { BillSellUrl, RentalItemUrl, SellItemUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const searchBillSell = async (
    data: Record<string, string | number>
): Promise<ResponseData<BillSells>> => {
    const res = await apiClient?.post(`${BillSellUrl}/search`, data);
    return res?.data;
};

export const getAllProduct = async (): Promise<RentalItems[]> => {
    const res = await apiClient?.get(`${RentalItemUrl}/get`);
    return res?.data;
};

export const getDetailSellItemById = async (
    id: string
): Promise<SellItems[]> => {
    const res = await apiClient?.get(`${BillSellUrl}/get-billsell-id/${id}`);
    return res?.data;
};

export const getDetailBillById = async (id: string): Promise<BillSells[]> => {
    const res = await apiClient?.get(
        `${BillSellUrl}/get-detail-billsell/${id}`
    );
    return res?.data;
};

export const createBillSell = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<BillSells> => {
    const res = await apiClient?.post(`${BillSellUrl}/add`, data);
    return res?.data;
};

export const updateBillSell = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<BillSells> => {
    const res = await apiClient?.put(`${BillSellUrl}/update`, data);
    return res?.data;
};

export const deleteBillSell = async (id: string): Promise<BillSells> => {
    const res = await apiClient?.delete(`${BillSellUrl}/delete/${id}`);
    return res?.data;
};

export const createSellItem = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<SellItems> => {
    const res = await apiClient?.post(`${SellItemUrl}/add`, data);
    return res?.data;
};

export const updateSellItem = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<SellItems> => {
    const res = await apiClient?.put(`${SellItemUrl}/update`, data);
    return res?.data;
};

export const deleteSellItem = async (id: string): Promise<SellItems> => {
    const res = await apiClient?.delete(`${SellItemUrl}/delete/${id}`);
    return res?.data;
};
