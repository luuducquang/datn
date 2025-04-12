import type { User } from "~/constant/api";
import { UserUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const login = async (
    data: Record<string, string | number>
): Promise<User> => {
    const res = await apiClient?.post(`/login`, data);
    return res?.data;
};
