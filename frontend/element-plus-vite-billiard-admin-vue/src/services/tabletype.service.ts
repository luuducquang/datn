import { TableTypes, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { TableTypeUrl } from "~/constant/endpoints";

export const getAllTableType = async (): Promise<TableTypes[]> => {
    const res = await apiClient?.get(`${TableTypeUrl}/get`);
    return res?.data;
};

export const searchTableType = async (
    data: Record<string, string | number>
): Promise<ResponseData<TableTypes>> => {
    const res = await apiClient?.post(`${TableTypeUrl}/search`, data);
    return res?.data;
};

export const createTableType = async (
    data: Record<string, string | number | boolean>
): Promise<TableTypes> => {
    const res = await apiClient?.post(`${TableTypeUrl}/add`, data);
    return res?.data;
};

export const updateTableType = async (
    data: Record<string, string | number | boolean>
): Promise<TableTypes> => {
    const res = await apiClient?.put(`${TableTypeUrl}/update`, data);
    return res?.data;
};

export const deleteTableType = async (id: String): Promise<TableTypes> => {
    const res = await apiClient?.delete(`${TableTypeUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdTableType = async (id: string): Promise<TableTypes> => {
    const res = await apiClient?.get(`${TableTypeUrl}/get/` + id);
    return res?.data;
};
