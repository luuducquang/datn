import { defineStore } from "pinia";
import { type Cart } from "~/constant/api";

export const useCartStore = defineStore("cart", {
    state: () => ({
        dataCart: [] as Cart[],
    }),
    getters: {
        totalItems: (state) => {
            return state.dataCart.length;
        },
    },
    actions: {
        setCart(cart: Cart[]) {
            this.dataCart = cart;
        },
        clearCart() {
            this.dataCart = [];
        },
    },
});
