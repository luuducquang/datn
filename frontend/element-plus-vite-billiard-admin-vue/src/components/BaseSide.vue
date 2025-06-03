<template>
    <el-menu
        :default-active="activeIndex"
        class="custom-sidebar"
        :collapse="isCollapse"
        @open="handleOpen"
        @close="handleClose"
        background-color="#f9fbfc"
        text-color="#000000"
    >
        <el-sub-menu index="1-2-3-4">
            <template #title>
                <el-icon><House /></el-icon>
                <span class="fw-bold">Tổng quan</span>
            </template>
            <router-link to="/" class="menu-link">
                <el-menu-item index="1">Trang chủ</el-menu-item>
            </router-link>
            <router-link to="/statistic" class="menu-link">
                <el-menu-item index="2">Thống kê</el-menu-item>
            </router-link>
            <router-link v-if="checkIsAdmin()" to="/discount" class="menu-link">
                <el-menu-item index="3">Mã giảm giá</el-menu-item>
            </router-link>
            <router-link to="/ratebooking" class="menu-link">
                <el-menu-item index="4">Đánh giá</el-menu-item>
            </router-link>
            <router-link to="/booking" class="menu-link">
                <el-menu-item index="21">Đặt bàn</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="8-9">
            <template #title>
                <el-icon><Mug /></el-icon>
                <span class="fw-bold">Hoá đơn</span>
            </template>
            <router-link to="/pay" class="menu-link">
                <el-menu-item index="20">Hoá đơn bàn</el-menu-item>
            </router-link>
            <router-link to="/billsell" class="menu-link">
                <el-menu-item index="8">Đơn hàng bán</el-menu-item>
            </router-link>
            <router-link to="/importbill" class="menu-link">
                <el-menu-item index="9">Đơn hàng nhập</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu v-if="checkIsAdmin()" index="5-6-7">
            <template #title>
                <el-icon><Box /></el-icon>
                <span class="fw-bold">Quản lý bàn</span>
            </template>
            <router-link to="/tabletype" class="menu-link">
                <el-menu-item index="5">Loại bàn</el-menu-item>
            </router-link>
            <router-link to="/table" class="menu-link">
                <el-menu-item index="6">Bàn</el-menu-item>
            </router-link>
            <router-link to="/pricingrule" class="menu-link">
                <el-menu-item index="7">Quy tắc giá</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="10-11">
            <template #title>
                <el-icon><Mug /></el-icon>
                <span class="fw-bold">Sản phẩm</span>
            </template>
            <router-link to="/menuitem" class="menu-link">
                <el-menu-item index="10">Sản phẩm dịch vụ</el-menu-item>
            </router-link>
            <router-link to="/product" class="menu-link">
                <el-menu-item index="11">Sản phẩm bán</el-menu-item>
            </router-link>
        </el-sub-menu>

        <router-link to="/news" class="menu-link">
            <el-menu-item index="12">
                <el-icon><Tickets /></el-icon>
                <span class="fw-bold">Tin tức</span>
            </el-menu-item>
        </router-link>

        <router-link to="/banner" class="menu-link">
            <el-menu-item index="13">
                <el-icon><Files /></el-icon>
                <span class="fw-bold">Banner</span>
            </el-menu-item>
        </router-link>

        <el-sub-menu index="14-15">
            <template #title>
                <el-icon><CollectionTag /></el-icon>
                <span class="fw-bold">Danh mục</span>
            </template>
            <router-link to="/categorymenuitem" class="menu-link">
                <el-menu-item index="14">Danh mục dịch vụ</el-menu-item>
            </router-link>
            <router-link to="/categoryproduct" class="menu-link">
                <el-menu-item index="15">Danh mục sản phẩm</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="16-17">
            <template #title>
                <el-icon><OfficeBuilding /></el-icon>
                <span class="fw-bold">Nhà cung cấp</span>
            </template>
            <router-link to="/manufactor" class="menu-link">
                <el-menu-item index="16">Hãng sản xuất</el-menu-item>
            </router-link>
            <router-link to="/supplier" class="menu-link">
                <el-menu-item index="17">Nhà phân phối</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu v-if="checkIsAdmin()" index="18-19">
            <template #title>
                <el-icon><User /></el-icon>
                <span class="fw-bold">Tài khoản</span>
            </template>
            <router-link to="/typeaccount" class="menu-link">
                <el-menu-item index="18">Loại tài khoản</el-menu-item>
            </router-link>
            <router-link to="/account" class="menu-link">
                <el-menu-item index="19">Tài khoản</el-menu-item>
            </router-link>
        </el-sub-menu>
    </el-menu>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import {
    House,
    Files,
    CollectionTag,
    OfficeBuilding,
    User,
    Mug,
    Box,
    Tickets,
} from "@element-plus/icons-vue";
import { checkIsAdmin } from "~/utils/checkRole";

const isCollapse = ref(false);
const route = useRoute();

const activeIndex = computed(() => {
    const path = route.path;
    if (path === "/") return "1";
    if (path.startsWith("/statistic")) return "2";
    if (path.startsWith("/discount")) return "3";
    if (path.startsWith("/ratebooking")) return "4";
    if (path.startsWith("/tabletype")) return "5";
    if (path.startsWith("/table")) return "6";
    if (path.startsWith("/pricingrule")) return "7";
    if (path.startsWith("/billsell")) return "8";
    if (path.startsWith("/importbill")) return "9";
    if (path.startsWith("/menuitem")) return "10";
    if (path.startsWith("/product")) return "11";
    if (path.startsWith("/news")) return "12";
    if (path.startsWith("/banner")) return "13";
    if (path.startsWith("/categorymenuitem")) return "14";
    if (path.startsWith("/categoryproduct")) return "15";
    if (path.startsWith("/manufactor")) return "16";
    if (path.startsWith("/supplier")) return "17";
    if (path.startsWith("/typeaccount")) return "18";
    if (path.startsWith("/account")) return "19";
    if (path.startsWith("/pay")) return "20";
    if (path.startsWith("/booking")) return "21";

    return "1";
});

const handleOpen = (key: string, keyPath: string[]) => {};
const handleClose = (key: string, keyPath: string[]) => {};
</script>

<style lang="scss" scoped>
.custom-sidebar {
    width: 240px;
    min-height: 100vh;
    background-color: #fff;
    box-shadow: 2px 0 12px rgba(46, 204, 113, 0.3);
    border-right: none;
    transition: width 0.3s ease;
    .menu-link {
        display: block;
        color: inherit;
        text-decoration: none;
        outline: none;
    }
}
.ep-menu {
    overflow: auto;
    padding-bottom: 10%;
}
</style>
