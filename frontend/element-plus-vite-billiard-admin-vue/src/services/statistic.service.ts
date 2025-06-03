import { StatisticUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getOverview = async (): Promise<
    Record<string, string | number>
> => {
    const res = await apiClient?.get(`${StatisticUrl}/get`);
    return res?.data;
};

export const getRevenueWeek = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/weekly-revenue`);
    return res?.data;
};

export const getRevenue = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/monthly-revenue`);
    return res?.data;
};

export const getRevenueYear = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/yearly-revenue`);
    return res?.data;
};

export const getProfitYear = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/imports-by-current-year`);
    return res?.data;
};

export const getPlaytime = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/playtime`);
    return res?.data;
};

export const getInventoryItem = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/inventory-item`);
    return res?.data;
};

export const getLowStock = async (): Promise<any> => {
    const res = await apiClient?.get(`${StatisticUrl}/low-stock`);
    return res?.data;
};
