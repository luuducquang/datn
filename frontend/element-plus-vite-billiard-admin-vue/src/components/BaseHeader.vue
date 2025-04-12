<template>
    <el-menu class="el-menu-demo" mode="horizontal">
        <a class="link_logo" href="/">
            <img class="logo" src="/src/assets/logo.png" alt="Images" />
        </a>
        <div class="header_right_item">
            <!-- <el-icon class="bell-icon">
                <BellFilled />
            </el-icon> -->
            <el-dropdown trigger="click">
                <span class="el-dropdown-link">
                    <img
                        :src="info.avt"
                        :title="info.name"
                        alt="User Image"
                        class="user-image"
                    />
                    <span>Xin chào, {{ info.name }}</span>
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item :icon="Setting">
                            Cài đặt
                        </el-dropdown-item>
                        <router-link to="/login">
                            <el-dropdown-item :icon="CaretRight">
                                Đăng xuất
                            </el-dropdown-item>
                        </router-link>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </el-menu>
</template>

<script lang="ts" setup>
import {
    Setting,
    CaretRight,
    BellFilled,
    ArrowDown,
} from "@element-plus/icons-vue";
import { computed } from "vue";
import { apiImage } from "~/constant/request";
import { useUserStore } from "~/store";

interface User {
    avatar: string;
    fullname: string;
}

const userStore = useUserStore();

const user = computed<User>(() => userStore.getUser);

const info = computed(() => {
    return {
        avt: apiImage + user.value.avatar,
        name: user.value.fullname,
    };
});
</script>

<style lang="scss" scoped>
a {
    text-decoration: none;
}
.el-menu-demo {
    background-color: #2f2d2d;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
}

.link_logo {
    display: flex;
    align-items: center;
}

.logo {
    height: 50px;
    width: 50px;
    cursor: pointer;
    margin-left: 40px;
}

.header_right_item {
    display: flex;
    align-items: center;
    gap: 20px;
}

.bell-icon {
    font-size: 24px;
    cursor: pointer;
}

.el-dropdown-link {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    color: #fff;
}

.user-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}
</style>
