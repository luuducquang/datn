import { RentalItems, ResponseData } from "~/constant/api";
import { RentalItemUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllRentalItem = async (): Promise<RentalItems[]> => {
    const res = await apiClient?.get(`${RentalItemUrl}/get`);
    return res?.data;
};

export const searchRentalItem = async (
    data: Record<string, string | number>
): Promise<ResponseData<RentalItems>> => {
    const res = await apiClient?.post(`${RentalItemUrl}/search`, data);
    return res?.data;
};

export const createRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<RentalItems> => {
    const res = await apiClient?.post(`${RentalItemUrl}/add`, data);
    return res?.data;
};

export const updateRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<RentalItems> => {
    const res = await apiClient?.put(`${RentalItemUrl}/update`, data);
    return res?.data;
};

export const deleteRentalItem = async (id: string): Promise<RentalItems> => {
    const res = await apiClient?.delete(`${RentalItemUrl}/delete/${id}`);
    return res?.data;
};

export const getbyIdRentalItems = async (id: string): Promise<any> => {
    const res = await apiClient?.get(`${RentalItemUrl}/get/` + id);
    return res?.data;
};
