import { TimeSessions } from "~/constant/api";
import { TimeSessionUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createTimeSession = async (
    data: TimeSessions
): Promise<string> => {
    const res = await apiClient?.post(`${TimeSessionUrl}/add`, data);
    return res?.data;
};

export const getCountByPhone = async (phone: string): Promise<number> => {
    const res = await apiClient?.get(
        `${TimeSessionUrl}/count-by-phone/` + phone
    );
    return res?.data;
};
