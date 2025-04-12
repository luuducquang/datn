import { StatisticUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getOverview = async (): Promise<
    Record<string, string | number>
> => {
    const res = await apiClient?.get(`${StatisticUrl}/get`);
    return res?.data;
};

export const getRevenue = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/monthly-revenue`);
    return res?.data;
};
