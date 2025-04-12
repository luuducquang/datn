import axios from "axios";

export const getCountry = async (): Promise<Record<string,string|[]>[]> => {
    const res = await axios("https://vapi.vnappmob.com/api/province");
    return res?.data;
};

export const getDistrict = async (province_id: number): Promise<Record<string,string|[]>[]> => {
    const res = await axios(
        `https://vapi.vnappmob.com/api/province/district/${province_id}`
    );
    return res?.data;
};

export const getWard = async (district_id: number): Promise<Record<string,string|[]>[]> => {
    const res = await axios(
        `https://vapi.vnappmob.com/api/province/ward/${district_id}`
    );
    return res?.data;
};
