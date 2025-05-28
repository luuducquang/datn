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
import { ref, onMounted } from "vue";
import { type News } from "~/constant/api";
import { getNewById } from "~/services/new.service";
import { useHead } from "@unhead/vue";

const route = useRoute();
const id = route.params.id;

const dataNewDetail = ref<News>();

const fetchNewDetail = async (id: string) => {
    try {
        const res = await getNewById(id);
        dataNewDetail.value = res;

        useHead({
            title: `${dataNewDetail?.value ? dataNewDetail?.value?.title:""}`,
        });
    } catch (error) {
        console.error("Error while fetching data:", error);
    }
};

onMounted(() => {
    fetchNewDetail(String(id));
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
    flex-wrap: wrap;
    font-family: "Montserrat", sans-serif;
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
    color: #eaffd0; /* Nhẹ nhàng, giữ trong cùng tone màu */
}

.type i {
    color: var(--color-text);
    font-size: 12px;
    margin: 0 8px;
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
