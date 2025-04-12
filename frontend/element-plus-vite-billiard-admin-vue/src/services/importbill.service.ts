import {
    ImportBills,
    ImportItems,
    ResponseData,
    Suppliers,
} from "~/constant/api";
import {
    ImportBillUrl,
    ImportItemUrl,
    SuppliersUrl,
} from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const searchImportBill = async (
    data: Record<string, string | number>
): Promise<ResponseData<ImportBills>> => {
    const res = await apiClient?.post(`${ImportBillUrl}/search`, data);
    return res?.data;
};

export const getAllSuppliers = async (): Promise<Suppliers[]> => {
    const res = await apiClient?.get(`${SuppliersUrl}/get`);
    return res?.data;
};

export const getDetailImportBillById = async (
    id: string
): Promise<ImportBills[]> => {
    const res = await apiClient?.get(
        `${ImportBillUrl}/get-detail-importbill/${id}`
    );
    return res?.data;
};

export const getListImportItemById = async (
    id: string
): Promise<ImportItems[]> => {
    const res = await apiClient?.get(`${ImportBillUrl}/get-import_item/${id}`);
    return res?.data;
};

export const createImportBill = async (
    data: ImportBills
): Promise<ImportBills> => {
    const res = await apiClient?.post(`${ImportBillUrl}/add`, data);
    return res?.data;
};

export const updateImportBill = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<ImportBills> => {
    const res = await apiClient?.put(`${ImportBillUrl}/update`, data);
    return res?.data;
};

export const deleteImportBill = async (id: string): Promise<ImportBills> => {
    const res = await apiClient?.delete(`${ImportBillUrl}/delete/${id}`);
    return res?.data;
};

export const createImportItem = async (
    data: ImportItems
): Promise<ImportItems> => {
    const res = await apiClient?.post(`${ImportItemUrl}/add`, data);
    return res?.data;
};

export const updateImportItem = async (
    data: ImportItems
): Promise<ImportItems> => {
    const res = await apiClient?.put(`${ImportItemUrl}/update`, data);
    return res?.data;
};

export const deleteImportItem = async (id: string): Promise<ImportItems> => {
    const res = await apiClient?.delete(`${ImportItemUrl}/delete/${id}`);
    return res?.data;
};
