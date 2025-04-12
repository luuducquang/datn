import { apiClient } from "~/constant/request";
import type { Cart } from "~/constant/api";
import { CartUrl } from "~/constant/endpoints";

export const getGioHangByIdTaiKhoan = async (id: string): Promise<Cart[]> => {
    const res = await apiClient?.get(`${CartUrl}/get/` + id);
    return res?.data;
};

export const createCart = async (
    data: Record<string, string | number | boolean>
): Promise<Cart> => {
    const res = await apiClient?.post(`${CartUrl}/add`, data);
    return res?.data;
};

export const updateCart = async (
    data: Record<string, string | number | boolean>
): Promise<Cart> => {
    const res = await apiClient?.put(`${CartUrl}/update`, data);
    return res?.data;
};

export const updateCartsFalse = async (mataikhoan: string): Promise<Cart> => {
    const res = await apiClient?.put(
        `${CartUrl}/updatefalsestatus/${mataikhoan}`
    );
    return res?.data;
};

export const deleteCarts = async (id: string): Promise<Cart> => {
    const res = await apiClient?.delete(`${CartUrl}/delete/${id}`);
    return res?.data;
};

export const deleteManyCarts = async (listid: string[]): Promise<Cart> => {
    const res = await apiClient?.delete(`${CartUrl}/delete`, {
        data: listid,
    });
    return res?.data;
};