import { Users } from "~/constant/api";
import { apiClient } from "~/constant/request";

export const login = async (
    data: Record<string, string | number>
): Promise<Users> => {
    const res = await apiClient?.post(`/login`, data);
    return res?.data;
};
