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
import { ref } from "vue";
import { type Products } from "~/constant/api";
import { getProductCategory } from "~/services/category.service";

const route = useRoute();
const name = route.params.search;

const currentPage = ref(1);
const totalPages = ref(1);
const itemFit = ref(0);

const products = ref<Products[]>([]);

const fetchProducts = async (page: number) => {
    try {
        const response = await getProductCategory({
            page,
            pageSize: 12,
            search_term: String(name),
        });

        products.value = response.data;
        totalPages.value = Math.ceil(response.totalItems / 12);
        itemFit.value = response.totalItems;
        console.log(products.value);
    } catch (error) {
        console.error("Error while fetching products:", error);
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

.pagination {
    flex-wrap: wrap;
    gap: 5px;
}

.page-item {
    margin: 0 3px;
}

.page-link {
    color: #333;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.25s ease-in-out;
    background-color: #fff;
}

.page-link:hover {
    background-color: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
}

.page-item.active .page-link {
    background-color: var(--color-primary);
    border-color: var(--color-primary);
    color: white;
}

.page-item.disabled .page-link {
    color: #999;
    background-color: #f9f9f9;
    pointer-events: none;
    border-color: #ddd;
}
</style>
