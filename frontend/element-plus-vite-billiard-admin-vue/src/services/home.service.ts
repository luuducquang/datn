import { TableMenuItems, TableRentalItems, Tables } from "~/constant/api";
import {
    TableMenuItemUrl,
    TableRentalItemUrl,
    TableUrl,
} from "~/constant/endpoints";
import { apiClient } from "~/constant/request";

export const getAllTable = async (): Promise<Tables[]> => {
    const res = await apiClient?.get(`${TableUrl}/get`);
    return res?.data;
};

export const getbyIdTable = async (id: string): Promise<Tables> => {
    const res = await apiClient?.get(`${TableUrl}/get/` + id);
    return res?.data;
};

export const getbyIdTableMenuItem = async (
    table_id: string
): Promise<TableMenuItems[]> => {
    const res = await apiClient?.get(`${TableMenuItemUrl}/get/` + table_id);
    return res?.data;
};

export const getbyIdTableRentalItem = async (
    table_id: string
): Promise<TableRentalItems[]> => {
    const res = await apiClient?.get(`${TableRentalItemUrl}/get/` + table_id);
    return res?.data;
};

export const createTableMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<TableMenuItems> => {
    const res = await apiClient?.post(`${TableMenuItemUrl}/add`, data);
    return res?.data;
};

export const createTableRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<TableRentalItems> => {
    const res = await apiClient?.post(`${TableRentalItemUrl}/add`, data);
    return res?.data;
};

export const updateTable = async (
    data: Record<string, string | number | boolean | Date>
): Promise<Tables> => {
    const res = await apiClient?.put(`${TableUrl}/update`, data);
    return res?.data;
};

export const updateTableMenuItem = async (
    data: Record<string, string | number | boolean>
): Promise<TableMenuItems> => {
    const res = await apiClient?.put(`${TableMenuItemUrl}/update`, data);
    return res?.data;
};

export const updateTableRentalItem = async (
    data: Record<string, string | number | boolean>
): Promise<TableRentalItems> => {
    const res = await apiClient?.put(`${TableRentalItemUrl}/update`, data);
    return res?.data;
};

export const deleteMenuItem = async (id: string): Promise<TableMenuItems> => {
    const res = await apiClient?.delete(`${TableMenuItemUrl}/deleteitem/${id}`);
    return res?.data;
};

export const deleteRentalItem = async (
    id: string
): Promise<TableRentalItems> => {
    const res = await apiClient?.delete(
        `${TableRentalItemUrl}/deleteitem/${id}`
    );
    return res?.data;
};

export const deleteMenuItembyTable = async (id: string): Promise<TableMenuItems> => {
    const res = await apiClient?.delete(`${TableMenuItemUrl}/deletes/${id}`);
    return res?.data;
};