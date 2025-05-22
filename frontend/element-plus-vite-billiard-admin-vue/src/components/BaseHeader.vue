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
                            <el-dropdown-item
                                :icon="CaretRight"
                                @click="logout"
                            >
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
import { Users } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { useUserStore } from "~/store";

const userStore = useUserStore();

const user = computed<any>(() => userStore.getUser);

const logout = () => {
    userStore.logout();
};

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
    background: linear-gradient(90deg, #2ecc71, #27ae60);
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    height: 70px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logo {
    height: 50px;
    width: 50px;
    cursor: pointer;
    margin-left: 20px;
    transition: transform 0.3s ease;
}

.logo:hover {
    transform: scale(1.1);
}

.header_right_item {
    display: flex;
    align-items: center;
    gap: 24px;
}

.el-dropdown-link {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    color: #fff;
    font-weight: 500;
    transition: color 0.2s ease;
}

.el-dropdown-link:hover {
    color: #f1f1f1;
}

.user-image {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease;
}

.user-image:hover {
    transform: scale(1.05);
}
</style>
