import axios from "axios";

export const getCountry = async (): Promise<any> => {
    const res = await axios("https://provinces.open-api.vn/api/");
    return res?.data;
};

export const getDistrict = async (province_id: number): Promise<any> => {
    const res = await axios(
        `https://provinces.open-api.vn/api/p/${province_id}?depth=2`
    );
    return res?.data;
};

export const getWard = async (district_id: number): Promise<any> => {
    const res = await axios(
        `https://provinces.open-api.vn/api/d/${district_id}?depth=2`
    );
    return res?.data;
};
