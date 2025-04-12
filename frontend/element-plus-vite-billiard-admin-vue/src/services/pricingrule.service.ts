import { PricingRules } from "~/constant/api";
import { PricingRuleUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllPricingRule = async (): Promise<PricingRules[]> => {
    const res = await apiClient?.get(`${PricingRuleUrl}/get`);
    return res?.data;
};

export const createPricingRule = async (
    data: Record<string, string | number>
): Promise<PricingRules> => {
    const res = await apiClient?.post(`${PricingRuleUrl}/add`, data);
    return res?.data;
};

export const updatePricingRule = async (
    data: Record<string, string | number>
): Promise<PricingRules> => {
    const res = await apiClient?.put(`${PricingRuleUrl}/update`, data);
    return res?.data;
};

export const deletePricingRule = async (id: string): Promise<PricingRules> => {
    const res = await apiClient?.delete(`${PricingRuleUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdPricingRule = async (id: string): Promise<PricingRules> => {
    const res = await apiClient?.get(`${PricingRuleUrl}/get/` + id);
    return res?.data;
};
