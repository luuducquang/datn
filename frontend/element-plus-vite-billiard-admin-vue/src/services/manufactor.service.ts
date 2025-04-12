import { Manufactors, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { ManufactorUrl } from "~/constant/endpoints";

export const getAllManufactor = async (): Promise<Manufactors[]> => {
    const res = await apiClient?.get(`${ManufactorUrl}/get`);
    return res?.data;
};

export const searchManufactor = async (
    data: Record<string, string | number>
): Promise<ResponseData<Manufactors>> => {
    const res = await apiClient?.post(`${ManufactorUrl}/search`, data);
    return res?.data;
};

export const createManufactor = async (
    data: Record<string, string | number>
): Promise<Manufactors> => {
    const res = await apiClient?.post(`${ManufactorUrl}/add`, data);
    return res?.data;
};

export const updateManufactor = async (
    data: Record<string, string | number>
): Promise<Manufactors> => {
    const res = await apiClient?.put(`${ManufactorUrl}/update`, data);
    return res?.data;
};

export const deleteManufactor = async (id: string): Promise<Manufactors> => {
    const res = await apiClient?.delete(`${ManufactorUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdManufactor = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${ManufactorUrl}/get/` + id);
    return res?.data;
};
