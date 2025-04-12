<template>
    <div class="content_heder">
        <h4 class="type">{{ title }}</h4>
        <a v-if="isShowLink" :href="link">Xem thêm</a>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    title: string;
    link: string;
    isShowLink: boolean;
}>();
</script>

<style lang="css" scoped>
.type {
    margin: 0;
}

.content_heder {
    padding: 10px;
    margin: 8px 0;
    color: #000000;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #000000;
}

a {
    color: #000000;
}
</style>
