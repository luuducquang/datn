import type { Account } from "~/constant/api";
import { AccountUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getInformation = async (id: string): Promise<Account> => {
    const res = await apiClient?.get(`${AccountUrl}/get/` + id);
    return res?.data;
};

export const updateInformation = async (
    data: Record<string, string, number | [object]>
): Promise<Account> => {
    const res = await apiClient?.put(`${AccountUrl}/update`, data);
    return res?.data;
};

export const updateInformationWalletPoint = async (
    data: Record<string, string, number | [object]>
): Promise<Account> => {
    const res = await apiClient?.put(`${AccountUrl}/updateuserwallet`, data);
    return res?.data;
};
