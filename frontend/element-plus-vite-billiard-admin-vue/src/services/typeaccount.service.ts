import { Roles } from "~/constant/api";
import { TypeAccountUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllTypeAccount = async (): Promise<Roles[]> => {
    const res = await apiClient?.get(`${TypeAccountUrl}/get`);
    return res?.data;
};

export const createTypeAccount = async (
    data: Record<string, string | number>
): Promise<Roles> => {
    const res = await apiClient?.post(`${TypeAccountUrl}/add`, data);
    return res?.data;
};

export const updateTypeAccount = async (
    data: Record<string, string | number>
): Promise<Roles> => {
    const res = await apiClient?.put(`${TypeAccountUrl}/update`, data);
    return res?.data;
};

export const deleteTypeAccount = async (id: string): Promise<Roles> => {
    const res = await apiClient?.delete(`${TypeAccountUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdTypeAccount = async (id: string): Promise<Roles> => {
    const res = await apiClient?.get(`${TypeAccountUrl}/get/` + id);
    return res?.data;
};
