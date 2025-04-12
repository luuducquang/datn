import { Users, ResponseData } from "~/constant/api";
import { TypeAccountUrl, AccountUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getDetailAccount = async (id: string): Promise<Users> => {
    const res = await apiClient?.get(`${AccountUrl}/get/` + id);
    return res?.data;
};

export const searchAccount = async (
    data: Record<string, string | number>
): Promise<ResponseData<Users>> => {
    const res = await apiClient?.post(`${AccountUrl}/search`, data);
    return res?.data;
};

export const createAccount = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<Users> => {
    const res = await apiClient?.post(`${AccountUrl}/add`, data);
    return res?.data;
};

export const updateAccount = async (
    data: Record<string | number, string | number | Array<object>>
): Promise<Users> => {
    const res = await apiClient?.put(`${AccountUrl}/update`, data);
    return res?.data;
};

export const deleteAccount = async (id: string): Promise<Users> => {
    const res = await apiClient?.delete(`${AccountUrl}/delete/` + id);
    return res?.data;
};
