<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/news">Tin tức</NuxtLink>
        </div>
        <div class="row">
            <div
                class="col-xl-4 col-lg-4 col-md-6 col-6 mb-4"
                v-for="product in news"
                :key="product._id"
            >
                <item-new :newItem="product" />
            </div>
        </div>
        <nav v-if="news.length > 0" aria-label="Page navigation example">
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

<script setup lang="ts">
import { ref } from "vue";
import { type News } from "~/constant/api";
import { getNews } from "~/services/new.service";

const currentPage = ref(1);
const totalPages = ref(1);

const news = ref<News[]>([]);

const fetchNews = async (page: number) => {
    const { data, error } = await useAsyncData("product", () =>
        getNews({
            page,
            pageSize: 6,
        })
    );

    if (data.value) {
        news.value = data.value?.data;
        totalPages.value = Math.ceil(data.value?.totalItems / 6);
        console.log(news.value);
    } else if (error.value) {
        console.error("Error while fetching:", error.value);
    }
};

const changePage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        fetchNews(page);
    }
};

fetchNews(currentPage.value);
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
