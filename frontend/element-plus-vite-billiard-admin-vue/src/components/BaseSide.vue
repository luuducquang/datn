<template>
    <el-menu
        :default-active="activeIndex"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        @open="handleOpen"
        @close="handleClose"
    >
        <el-sub-menu index="1-2-3-4">
            <template #title>
                <el-icon><House /></el-icon>
                <span>Tổng quan</span>
            </template>
            <router-link to="/">
                <el-menu-item index="1">Trang chủ</el-menu-item>
            </router-link>
            <router-link to="/statistic">
                <el-menu-item index="2">Thống kê</el-menu-item>
            </router-link>
            <router-link to="/discount">
                <el-menu-item index="3">Mã giảm giá</el-menu-item>
            </router-link>
            <router-link to="/ratebooking">
                <el-menu-item index="4">Đánh giá</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="8-9">
            <template #title>
                <el-icon><Mug /></el-icon>
                <span>Hoá đơn</span>
            </template>
            <router-link to="/pay">
                <el-menu-item index="20">Thanh toán</el-menu-item>
            </router-link>
            <router-link to="/billsell">
                <el-menu-item index="8">Đơn hàng bán</el-menu-item>
            </router-link>
            <router-link to="/importbill">
                <el-menu-item index="9">Đơn hàng nhập</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="5-6-7">
            <template #title>
                <el-icon><Box /></el-icon>
                <span>Quản lý bàn</span>
            </template>
            <router-link to="/tabletype">
                <el-menu-item index="5">Loại bàn</el-menu-item>
            </router-link>
            <router-link to="/table">
                <el-menu-item index="6">Bàn</el-menu-item>
            </router-link>
            <router-link to="/pricingrule">
                <el-menu-item index="7">Quy tắc giá</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="10-11">
            <template #title>
                <el-icon><Mug /></el-icon>
                <span>Sản phẩm</span>
            </template>
            <router-link to="/menuitem">
                <el-menu-item index="10">Sản phẩm thuê</el-menu-item>
            </router-link>
            <router-link to="/product">
                <el-menu-item index="11">Sản phẩm bán</el-menu-item>
            </router-link>
        </el-sub-menu>

        <router-link to="/news">
            <el-menu-item index="12">
                <el-icon><Files /></el-icon>
                <template #title>Tin tức</template>
            </el-menu-item>
        </router-link>

        <router-link to="/banner">
            <el-menu-item index="13">
                <el-icon><Files /></el-icon>
                <template #title>Banner</template>
            </el-menu-item>
        </router-link>

        <el-sub-menu index="14-15">
            <template #title>
                <el-icon><CollectionTag /></el-icon>
                <span>Danh mục</span>
            </template>
            <router-link to="/categorymenuitem">
                <el-menu-item index="14">Danh mục dịch vụ</el-menu-item>
            </router-link>
            <router-link to="/categoryproduct">
                <el-menu-item index="15">Danh mục sản phẩm</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="16-17">
            <template #title>
                <el-icon><OfficeBuilding /></el-icon>
                <span>Nhà cung cấp</span>
            </template>
            <router-link to="/manufactor">
                <el-menu-item index="16">Hãng sản xuất</el-menu-item>
            </router-link>
            <router-link to="/supplier">
                <el-menu-item index="17">Nhà phân phối</el-menu-item>
            </router-link>
        </el-sub-menu>

        <el-sub-menu index="18-19">
            <template #title>
                <el-icon><User /></el-icon>
                <span>Tài khoản</span>
            </template>
            <router-link to="/typeaccount">
                <el-menu-item index="18">Loại tài khoản</el-menu-item>
            </router-link>
            <router-link to="/account">
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
    Document,
    Menu as IconMenu,
    Tickets,
    Notebook,
    Files,
    ChatLineRound,
    CollectionTag,
    PriceTag,
    OfficeBuilding,
    School,
    CreditCard,
    Picture,
    Connection,
    User,
    Mug,
    Ship,
    Box,
} from "@element-plus/icons-vue";

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

    return "0";
});

const handleOpen = (key: string, keyPath: string[]) => {
    // console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
    // console.log(key, keyPath);
};
</script>

<style lang="scss" scoped>
a {
    text-decoration: none;
    color: #333;
}

.el-menu-vertical-demo {
    min-width: 192px;
    overflow-y: scroll;
}
</style>
