import { Tables, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { TableUrl } from "~/constant/endpoints";

export const searchTable = async (
    data: Record<string, string | number>
): Promise<ResponseData<Tables>> => {
    const res = await apiClient?.post(`${TableUrl}/search`, data);
    return res?.data;
};

export const createTable = async (
    data: Record<string, string | number | boolean>
): Promise<Tables> => {
    const res = await apiClient?.post(`${TableUrl}/add`, data);
    return res?.data;
};

export const updateTable = async (
    data: Record<string, string | number | boolean>
): Promise<Tables> => {
    const res = await apiClient?.put(`${TableUrl}/update`, data);
    return res?.data;
};

export const deleteTable = async (id: String): Promise<Tables> => {
    const res = await apiClient?.delete(`${TableUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdTable = async (id: string): Promise<Tables> => {
    const res = await apiClient?.get(`${TableUrl}/get/` + id);
    return res?.data;
};

export const getbyAllTable = async (): Promise<Tables> => {
    const res = await apiClient?.get(`${TableUrl}/get/`);
    return res?.data;
};
