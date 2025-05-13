import { Products, ResponseData } from "~/constant/api";
import { ProductUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllProduct = async (): Promise<Products[]> => {
    const res = await apiClient?.get(`${ProductUrl}/get`);
    return res?.data;
};

export const searchProduct = async (
    data: Record<string, string | number>
): Promise<ResponseData<Products>> => {
    const res = await apiClient?.post(`${ProductUrl}/search`, data);
    return res?.data;
};

export const createProduct = async (
    data: Record<string, string | number | boolean>
): Promise<Products> => {
    const res = await apiClient?.post(`${ProductUrl}/add`, data);
    return res?.data;
};

export const updateProduct = async (
    data: Record<string, string | number | boolean>
): Promise<Products> => {
    const res = await apiClient?.put(`${ProductUrl}/update`, data);
    return res?.data;
};

export const deleteProduct = async (id: string): Promise<Products> => {
    const res = await apiClient?.delete(`${ProductUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdProducts = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${ProductUrl}/get/` + id);
    return res?.data;
};
