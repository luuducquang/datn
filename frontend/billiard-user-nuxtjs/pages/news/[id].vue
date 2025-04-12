<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/news">Tin tức</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink :to="`/news/${id}`">{{ dataNewDetail?.title }}</NuxtLink>
        </div>
        <div class="newsDetail">
            <h1 class="titleDetail">{{ dataNewDetail?.title }}</h1>
            <div class="content_detail" v-html="dataNewDetail?.content"></div>
            <div class="view_detail">{{ dataNewDetail?.view }} lượt xem</div>
            <div class="view_detail">
                Người đăng: {{ dataNewDetail?.fullname }}
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useRoute } from "vue-router";
import { ref } from "vue";
import { type News } from "~/constant/api";
import { getNewById } from "~/services/new.service";

const route = useRoute();
const id = route.params.id;

const dataNewDetail = ref<News>();

const fetchProducts = async (id: string) => {
    const { data, error } = await useAsyncData("dataNewDetail", () =>
        getNewById(id)
    );

    if (data.value) {
        dataNewDetail.value = data.value;
    } else if (error.value) {
        console.error("Error while fetching data:", error.value);
    }
};

fetchProducts(String(id));
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

.newsDetail {
    margin: 10px 0;
    padding: 10px;
}

.view_detail {
    text-align: right;
}

.content_detail {
    overflow: hidden;
}

.content_detail img {
    width: 100% !important;
}
</style>
