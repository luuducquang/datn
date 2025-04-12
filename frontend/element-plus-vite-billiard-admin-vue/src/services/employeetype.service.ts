import { EmployeeTypes } from "~/constant/api";
import { EmployeeTypeUrl } from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllEmployeeType = async (): Promise<EmployeeTypes[]> => {
    const res = await apiClient?.get(`${EmployeeTypeUrl}/get`);
    return res?.data;
};

export const createEmployeeType = async (
    data: Record<string, string | number>
): Promise<EmployeeTypes> => {
    const res = await apiClient?.post(`${EmployeeTypeUrl}/add`, data);
    return res?.data;
};

export const updateEmployeeType = async (
    data: Record<string, string | number>
): Promise<EmployeeTypes> => {
    const res = await apiClient?.put(`${EmployeeTypeUrl}/update`, data);
    return res?.data;
};

export const deleteEmployeeType = async (
    id: string
): Promise<EmployeeTypes> => {
    const res = await apiClient?.delete(`${EmployeeTypeUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdEmployeeType = async (
    id: string
): Promise<EmployeeTypes> => {
    const res = await apiClient?.get(
        `${EmployeeTypeUrl}/get/` + id
    );
    return res?.data;
};
