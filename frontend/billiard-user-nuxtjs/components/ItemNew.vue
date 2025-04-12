<template>
    <div class="news_content">
        <NuxtLink :to="`/news/${newItem?._id}`">
            <img :src="apiImage + newItem?.image" alt="" />
            <div :title="newItem?.title" class="title_news">
                {{ newItem?.title }}
            </div>
            <div class="view_news">
                <i class="fa-solid fa-eye"></i>
                <span>{{
                    Number(newItem?.view) > 0
                        ? Number(newItem?.view).toLocaleString("de-DE")
                        : "0"
                }}</span>
            </div>
            <div class="author">Người đăng: {{ newItem?.fullname }}</div>
        </NuxtLink>
    </div>
</template>

<script lang="ts" setup>
import { type News } from "~/constant/api";
import { apiImage } from "~/constant/request";

const props = defineProps<{
    newItem: News;
}>();
</script>

<style scoped>
.news_content {
    margin: 1%;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.news_content img {
    width: 100%;
    height: 100%;
    transition: transform 0.3s, filter 0.3s;
}

.news_content:hover img {
    transform: scale(1.1);
    filter: brightness(0.7);
}

.title_news {
    position: absolute;
    bottom: 5px;
    font-size: 1.5rem;
    font-weight: 600;
    margin-left: 20px;
    margin-bottom: 20px;
    opacity: 0;
    transition: opacity 0.3s;
    color: #fff;
    max-height: 80%;
    width: 80%;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    white-space: normal;
}

.view_news {
    display: flex;
    position: absolute;
    justify-content: center;
    align-items: center;
    gap: 5px;
    bottom: 5px;
    right: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-left: 20px;
    transition: opacity 0.3s;
    color: #fff;
    opacity: 0;
}

.author {
    position: absolute;
    top: 5px;
    left: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    transition: opacity 0.3s;
    color: #fff;
    opacity: 0;
}

.news_content:hover .title_news,
.news_content:hover .view_news,
.news_content:hover .author {
    opacity: 1;
}
</style>
