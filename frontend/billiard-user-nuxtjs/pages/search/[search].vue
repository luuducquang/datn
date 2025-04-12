<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink :to="`/search/${name}`"> Tìm kiếm - {{ name }}</NuxtLink>
        </div>
        <h4 class="mt-2">Có {{ itemFit }} kết quả phù hợp</h4>
        <div class="row">
            <div
                class="col-xl-2 col-lg-3 col-md-4 col-sm-6 col-6 mb-4 d-flex"
                v-for="product in products"
                :key="product._id"
            >
                <item-product-home :product="product" :isSale="false" />
            </div>
        </div>
        <h3 v-if="products.length === 0" class="text-center mt-4">
            Không có sản phẩm nào
        </h3>
        <nav v-if="products.length > 0" aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <NuxtLink
                        class="page-link"
                        to="#"
                        aria-label="Previous"
                        @click="changePage(currentPage - 1)"
                    >
                        <span aria-hidden="true">&laquo;</span>
                    </NuxtLink>
                </li>
                <li
                    class="page-item"
                    v-for="page in totalPages"
                    :key="page"
                    :class="{ active: page === currentPage }"
                >
                    <NuxtLink
                        class="page-link"
                        to="#"
                        @click="changePage(page)"
                        >{{ page }}</NuxtLink
                    >
                </li>
                <li
                    class="page-item"
                    :class="{ disabled: currentPage === totalPages }"
                >
                    <NuxtLink
                        class="page-link"
                        to="#"
                        aria-label="Next"
                        @click="changePage(currentPage + 1)"
                    >
                        <span aria-hidden="true">&raquo;</span>
                    </NuxtLink>
                </li>
            </ul>
        </nav>
    </div>
</template>
<script lang="ts" setup>
import { useRoute } from "vue-router";
import { onUnmounted, ref } from "vue";
import { type Product } from "~/constant/api";
import { getProductCategory } from "~/services/category.service";

const route = useRoute();
const name = route.params.search;

const currentPage = ref(1);
const totalPages = ref(1);
const itemFit = ref(0);

const products = ref<Product[]>([]);

const fetchProducts = async (page: number) => {
    const { data, error } = await useAsyncData("product", () =>
        getProductCategory({
            page,
            pageSize: 12,
            search_term: name,
        })
    );

    if (data.value) {
        products.value = data.value?.data;
        totalPages.value = Math.ceil(data.value?.totalItems / 12);
        itemFit.value = data.value?.totalItems;
        console.log(products.value);
    } else if (error.value) {
        console.error("Error while fetching products:", error.value);
    }
};

const changePage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        fetchProducts(page);
    }
};

fetchProducts(currentPage.value);
</script>
<style lang="css" scoped>
.type {
    background: linear-gradient(90deg, var(--color-primary) 0%, #001815 100%) 0%
        0% no-repeat;
    padding: 10px;
    color: #fff;
    margin-top: 10px;
}

.type a {
    text-decoration: none;
    color: #ddd;
    font-size: 14px;
    text-transform: uppercase;
}

.type i {
    color: #fff;
    font-size: 10px;
    padding: 0 10px;
}
</style>
