import { Employees, ResponseData } from "~/constant/api";
import { apiClient } from "../constant/request";
import { EmployeeUrl } from "~/constant/endpoints";

export const searchEmployee = async (
    data: Record<string, string | number>
): Promise<ResponseData<Employees>> => {
    const res = await apiClient?.post(`${EmployeeUrl}/search`, data);
    return res?.data;
};

export const createEmployee = async (
    data: Record<string, string | number | boolean>
): Promise<Employees> => {
    const res = await apiClient?.post(`${EmployeeUrl}/add`, data);
    return res?.data;
};

export const updateEmployee = async (
    data: Record<string, string | number | boolean>
): Promise<Employees> => {
    const res = await apiClient?.put(`${EmployeeUrl}/update`, data);
    return res?.data;
};

export const deleteEmployee = async (id: String): Promise<Employees> => {
    const res = await apiClient?.delete(`${EmployeeUrl}/delete/` + id);
    return res?.data;
};

export const getbyIdEmployee = async (id: string): Promise<Employees> => {
    const res = await apiClient?.get(`${EmployeeUrl}/get/` + id);
    return res?.data;
};
