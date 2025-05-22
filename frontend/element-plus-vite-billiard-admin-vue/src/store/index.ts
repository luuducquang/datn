import { defineStore } from "pinia";
import Cookies from "js-cookie";
import type { Users } from "~/constant/api";

export const useUserStore = defineStore("user", {
    state: () => ({
        user: JSON.parse(Cookies.get("user") || "null") as Users | null,
    }),
    getters: {
        getUser: (state) => state.user,
        isLoggedIn: (state) => !!state.user?.token,
    },
    actions: {
        setUser(user: Users) {
            this.user = user;
            Cookies.set("user", JSON.stringify(user), { expires: 1 });
        },
        logout() {
            this.user = null;
            Cookies.remove("user");
        },
    },
});
