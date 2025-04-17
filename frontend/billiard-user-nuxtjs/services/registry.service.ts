import type { Account } from "~/constant/api";
import { AccountUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const registryUser = async (
    data: Record<string, string | number>
): Promise<Account> => {
    const res = await apiClient?.post(`/register`, data);
    return res?.data;
};


export const sentOtp = async (
    data: Record<string, string>
): Promise<string> => {
    const res = await apiClient?.post(`/resend-otp`, data);
    return res?.data;
};

export const verifyOtp = async (
    data: Record<string, string>
): Promise<string> => {
    const res = await apiClient?.post(`/verify-otp`, data);
    return res?.data;
};


export const sendForgotPasswordOtp = async (
    data: Record<string, string>
): Promise<string> => {
    const res = await apiClient?.post(`/forgot-password`, data);
    return res?.data;
};

export const resetPasswordWithOtp = async (
    data: Record<string, string | number>
): Promise<string> => {
    const res = await apiClient?.post(`/reset-password`, data);
    return res?.data;
};
