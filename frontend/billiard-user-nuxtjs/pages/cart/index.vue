<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/cart">Giỏ Hàng</NuxtLink>
        </div>
        <div class="null_content">
            <h4 class="null_item" v-if="dataCart.length === 0">
                Giỏ hàng trống
            </h4>
            <div class="text-center">
                <NuxtLink v-if="dataCart.length === 0" to="/"
                    >Quay Lại trang chủ</NuxtLink
                >
            </div>
        </div>
        <item-cart
            :dataCart="dataCart"
            :fetch="fetchDataCart"
            :totalPrice="totalPrice"
            :order="false"
        />
        <div class="recomend">
            <h1>Gợi ý sản phẩm</h1>
            <div class="list_item_recomend">
                <div class="row justify-content-center">
                    <div
                        class="col-lg-2 col-md-4 col-sm-6 col-6"
                        v-for="product in productRecomend"
                        :key="product._id"
                    >
                        <item-product-recomend
                            :product="product"
                            :isSale="true"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Cookies from "js-cookie";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { type Product, type Cart } from "~/constant/api";
import { getGioHangByIdTaiKhoan } from "~/services/cart.service";
import { getProductRecomend } from "~/services/detail.service";

const router = useRouter();

const dataCart = ref<Cart[]>([]);
const productRecomend = ref<Product[]>([]);
const totalPrice = ref(0);

const fetchDataCart = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            dataCart.value = await getGioHangByIdTaiKhoan(customer._id);
            const dataBuy = dataCart.value.filter(
                (value) => value?.status === true
            );
            const total = dataBuy.reduce((total, item) => {
                return (
                    total +
                    Number(item?.rentalitem?.price_reduction) *
                        Number(item?.quantity)
                );
            }, 0);

            totalPrice.value = total;
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
            router.push("/login");
        }
    } else {
        router.push("/login");
    }
};

const fetchProductRecomend = async () => {
    try {
        const res = await getProductRecomend({
            page: 1,
            pageSize: 6,
        });
        productRecomend.value = res?.data ?? [];
    } catch (error) {
        console.error("Error while fetching recommended products:", error);
    }
};

onMounted(async () => {
    await fetchDataCart();
    await fetchProductRecomend();
});
</script>

<style lang="css" scoped>
.type {
    background: linear-gradient(
        90deg,
        var(--color-primary),
        var(--color-linear-gradient)
    );
    padding: 12px 20px;
    color: var(--color-text);
    margin-top: 10px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    font-size: 13px;
}

.type a {
    text-decoration: none;
    color: var(--color-text);
    font-size: 13px;
    text-transform: uppercase;
    font-weight: 600;
    transition: color 0.3s;
}

.type a:hover {
    color: #eaffd0;
}

.type i {
    color: var(--color-text);
    font-size: 12px;
    margin: 0 8px;
}

.null_content {
    padding: 10px 0;
}

.null_item {
    text-align: center;
    text-transform: uppercase;
    margin: 0;
}
.recomend > h1 {
    font-size: 30px;
    text-align: center;
    text-transform: uppercase;
    margin: 0;
    padding-bottom: 10px;
    padding-top: 20px;
    color: var(--color-primary);
}
</style>
