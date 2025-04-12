import { defineStore } from "pinia";
import { Users } from "~/constant/api";

export const useUserStore = defineStore("user", {
    state: () => ({
        user: {
            _id: "670f17f5279b5da63b9bdc7a",
            username: "quang",
            password: "1",
            fullname: "Lưu Đức Quang",
            email: "adasd",
            phone: "ádasdas",
            address: "ada",
            avatar: "/static/uploads/DALL·E 2024-10-10 22.42.17 - A modern and sleek logo design for a billiards hall named 'NewSunClub'. The logo should feature elements of billiards, such as a cue stick or a billia.webp",
            loyalty_points: 0,
            role_name: "ADMIN",
            token: "eyJhbGciOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0.eyJ1bmlxdWVfbmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJyb2xlIjoiOCIsIm5iZiI6MTcyMTI4MTM2NCwiZXhwIjoxNzIxODg2MTY0LCJpYXQiOjE3MjEyODEzNjR9.cZIvgGriKLcRIQ2M9LtXFC7zDgA5HyfJVPwJtTjXNBc",
        },
    }),
    getters: {
        getUser: (state) => state.user,
    },
    actions: {
        setUser(user: Users) {
            this.user = user;
        },
    },
});
