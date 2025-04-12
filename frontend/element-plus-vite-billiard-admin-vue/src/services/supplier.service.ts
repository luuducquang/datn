import { Suppliers, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { SuppliersUrl } from "~/constant/endpoints";

export const searchSuppliers = async (
    data: Record<string, string | number>
): Promise<ResponseData<Suppliers>> => {
    const res = await apiClient?.post(`${SuppliersUrl}/search`, data);
    return res?.data;
};

export const createSuppliers = async (
    data: Record<string, string | number>
): Promise<Suppliers> => {
    const res = await apiClient?.post(`${SuppliersUrl}/add`, data);
    return res?.data;
};

export const updateSuppliers = async (
    data: Record<string, string | number>
): Promise<Suppliers> => {
    const res = await apiClient?.put(`${SuppliersUrl}/update`, data);
    return res?.data;
};

export const deleteSuppliers = async (id: string): Promise<Suppliers> => {
    const res = await apiClient?.delete(`${SuppliersUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdSuppliers = async (id: string): Promise<Suppliers> => {
    const res = await apiClient?.get(`${SuppliersUrl}/get/` + id);
    return res?.data;
};
