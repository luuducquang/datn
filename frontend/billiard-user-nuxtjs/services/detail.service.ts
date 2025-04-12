import type { Product, ResponseData } from "~/constant/api";
import { ProductUrl, RateUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getProductById = async (id: string): Promise<Product> => {
    const res = await apiClient?.get(`${ProductUrl}/get/` + id);
    return res?.data;
};

export const getProductRecomend = async (
    data: Record<string, string | number>
): Promise<ResponseData<Product>> => {
    const res = await apiClient?.post(`${ProductUrl}/search`, data);
    return res?.data;
};

export const getImgProductDetail = async (maSanPham: number): Promise<any> => {
    const res = await apiClient?.get(
        `${ProductUrl}/getbyid-anhsanphamdetail/` + maSanPham
    );
    return res?.data;
};

export const getRatingProduct = async (
    data: Record<string, string>
): Promise<any> => {
    const res = await apiClient?.post(`${RateUrl}/search-danhgia`, data);
    return res?.data;
};
