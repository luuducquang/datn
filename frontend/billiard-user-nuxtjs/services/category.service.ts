import type { Product, ResponseData } from "~/constant/api";
import { ProductUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getProductCategory = async (
    data: Record<string  , string | number>
): Promise<ResponseData<Product>> => {
    const res = await apiClient?.post(`${ProductUrl}/search`, data);
    return res?.data;
};

