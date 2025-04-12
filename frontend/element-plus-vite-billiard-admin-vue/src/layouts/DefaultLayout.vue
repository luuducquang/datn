<template>
    <el-config-provider namespace="ep">
        <BaseHeader />
        <div class="flex main-container">
            <BaseSide />
            <div style="overflow: auto; width: 100%">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item
                        v-for="(crumb, index) in breadcrumbs"
                        :key="index"
                        :to="crumb.path"
                    >
                        {{ crumb.meta.breadcrumbName }}
                    </el-breadcrumb-item>
                </el-breadcrumb>
                <router-view />
            </div>
        </div>
    </el-config-provider>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const breadcrumbs = computed(() => {
    return route.matched.map((record) => ({
        path: record.path,
        meta: record.meta,
    }));
});
</script>

<style lang="scss">
#app {
    text-align: center;
    color: var(--ep-text-color-primary);
}

.main-container {
    height: calc(100vh - var(--ep-menu-item-height) - 3px);
}

.ep-breadcrumb {
    height: 40px;
    display: flex;
}
</style>
