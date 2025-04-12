import { TimeSessions } from "~/constant/api";
import { TimeSessionUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const createTimeSession = async (
    data: TimeSessions
): Promise<TimeSessions> => {
    const res = await apiClient?.post(`${TimeSessionUrl}/add`, data);
    return res?.data;
};
