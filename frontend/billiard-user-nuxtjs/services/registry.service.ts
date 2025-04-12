import type { Account } from "~/constant/api";
import { AccountUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const registryUser = async (
    data: Record<string, string | number>
): Promise<Account> => {
    const res = await apiClient?.post(`${AccountUrl}/add`, data);
    return res?.data;
};
