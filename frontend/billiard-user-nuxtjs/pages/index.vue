<template>
    <AppSlide />
    <div class="container">
        <HeaderComponent
            title="Sản phẩm mới nhất"
            link=""
            :isShowLink="false"
        />
        <div class="row" v-if="productNew">
            <div
                class="col-xl-2 col-lg-3 col-md-4 col-sm-4 col-6 mb-4 d-flex"
                v-for="product in productNew"
                :key="product._id"
            >
                <ItemProductHome :product="product" :isSale="true" />
            </div>
        </div>

        <HeaderComponent
            v-if="productCoBan"
            title="Cơ bắn"
            :link="'/category/cơ bắn'"
            :isShowLink="true"
        />
        <div class="row" v-if="productCoBan">
            <div
                class="col-xl-2 col-lg-3 col-md-4 col-sm-4 col-6 mb-4 d-flex"
                v-for="product in productCoBan"
                :key="product._id"
            >
                <ItemProductHome :product="product" :isSale="false" />
            </div>
        </div>

        <HeaderComponent
            v-if="productCoPha"
            title="Cơ phá"
            :link="'/category/cơ phá'"
            :isShowLink="true"
        />
        <div class="row" v-if="productCoPha">
            <div
                class="col-xl-2 col-lg-3 col-md-4 col-sm-4 col-6 mb-4 d-flex"
                v-for="product in productCoPha"
                :key="product._id"
            >
                <ItemProductHome :product="product" :isSale="false" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { type Product } from "~/constant/api";
import { getProductHome } from "~/services/home.service";
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import { getGioHangByIdTaiKhoan } from "~/services/cart.service";
import { useCartStore } from "~/store";

useHead({
    title: "Trang chủ",
});

const productNew = ref<Product[]>([]);
const productCoBan = ref<Product[]>([]);
const productCoPha = ref<Product[]>([]);
const store = useCartStore();

const { data: newData, error: er } = await useAsyncData("productNew", () =>
    getProductHome({
        page: 1,
        pageSize: 12,
    })
);

if (newData.value) {
    productNew.value = newData.value?.data;
} else if (er.value) {
    console.error("Error while fetching products:", er.value);
}

const { data: coBanData, error: erBan } = await useAsyncData(
    "productCoBan",
    () =>
        getProductHome({
            page: 1,
            pageSize: 12,
            category_name: "Cơ bắn",
        })
);

if (coBanData.value) {
    productCoBan.value = coBanData.value?.data;
} else if (erBan.value) {
    console.error("Error while fetching products:", erBan.value);
}

const { data: cophaData, error: erCoPha } = await useAsyncData(
    "productCoPha",
    () =>
        getProductHome({
            page: 1,
            pageSize: 12,
            category_name: "Cơ phá",
        })
);

if (cophaData.value) {
    productCoPha.value = cophaData.value?.data;
} else if (erCoPha.value) {
    console.error("Error while fetching products:", erCoPha.value);
}

onMounted(async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            const cart = await getGioHangByIdTaiKhoan(customer._id);

            store.setCart(cart);
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
        }
    }
});
</script>