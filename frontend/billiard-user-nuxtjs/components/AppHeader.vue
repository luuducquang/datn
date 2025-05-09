<template>
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
            <NuxtLink class="navbar-brand" to="/">
                <img
                    src="/images/logo1.png"
                    alt="images"
                    width="50"
                    height="50"
                />
            </NuxtLink>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <i class="fa-solid fa-bars"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <NuxtLink
                            class="nav-link active"
                            aria-current="page"
                            to="/"
                            >Trang chủ</NuxtLink
                        >
                    </li>
                    <li class="nav-item">
                        <NuxtLink class="nav-link" to="/news">Tin tức</NuxtLink>
                    </li>
                    <li class="nav-item dropdown">
                        <NuxtLink
                            class="nav-link dropdown-toggle"
                            href="#"
                            role="button"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            Danh mục
                        </NuxtLink>
                        <ul class="dropdown-menu">
                            <div v-for="item in category" :key="item._id">
                                <li>
                                    <a
                                        class="dropdown-item"
                                        :href="`/category/${item.category_name}`"
                                        >{{ item.category_name }}</a
                                    >
                                </li>
                            </div>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <NuxtLink class="nav-link booking-link" to="/booking"
                            >Đặt bàn</NuxtLink
                        >
                    </li>
                </ul>

                <form
                    class="d-flex position-relative"
                    role="search"
                    @submit.prevent="submitSearch"
                >
                    <input
                        v-model="searchQuery"
                        class="form-control pe-5"
                        type="search"
                        placeholder="Tìm kiếm sản phẩm"
                        aria-label="Search"
                    />
                    <button
                        class="btn position-absolute top-0 end-0 rounded-start"
                        type="submit"
                    >
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </button>
                </form>

                <ul class="navbar-nav me-auto mb-2 mb-lg-0 menu_item_right">
                    <li class="nav-item">
                        <NuxtLink to="/cart" class="nav-link"
                            ><i class="fa-solid fa-cart-shopping"></i>
                            <span
                                >({{
                                    store.totalItems > 0 ? store.totalItems : 0
                                }})</span
                            >
                        </NuxtLink>
                    </li>
                </ul>

                <ul class="navbar-nav me-auto mb-2 mb-lg-0 menu_item_right">
                    <div v-if="!customer" class="user">
                        <li class="nav-item">
                            <NuxtLink to="/login">Đăng nhập</NuxtLink>
                        </li>
                        <li class="nav-item">
                            <NuxtLink to="/registry">Đăng ký</NuxtLink>
                        </li>
                    </div>
                    <div v-if="customer" class="dropdown">
                        <!-- <button
                            class="btn btn-secondary dropdown-toggle"
                            type="button"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            Dropdown button
                        </button> -->
                        <div
                            class="user dropdown-toggle"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            <img
                                class="img_user"
                                :src="apiImage + customer?.avatar"
                                alt="Image"
                            />
                            <p>{{ customer.fullname }}</p>
                        </div>

                        <ul class="dropdown-menu w-100">
                            <li>
                                <span class="dropdown-item nav-link disabled">
                                    Số dư ví: {{ ConvertPrice(customer?.loyalty_points) }}
                                </span>
                            </li>

                            <li>
                                <NuxtLink
                                    class="dropdown-item nav-link"
                                    to="/information"
                                >
                                    Thông tin tài khoản
                                </NuxtLink>
                            </li>
                            <li>
                                <NuxtLink
                                    class="dropdown-item nav-link"
                                    to="/invoice"
                                    >Lịch sử đơn hàng</NuxtLink
                                >
                            </li>
                            <li>
                                <NuxtLink
                                    class="dropdown-item nav-link"
                                    to="/mybooking"
                                    >Lịch sử đặt bàn</NuxtLink
                                >
                            </li>

                            <li>
                                <a
                                    class="dropdown-item nav-link"
                                    href="/login"
                                    @click="logoutHandler"
                                >
                                    Đăng xuất
                                </a>
                            </li>
                        </ul>
                    </div>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import { useRouter } from "vue-router";
import { type Category, type User } from "~/constant/api";
import { getCategory } from "~/services/home.service";
import { apiImage } from "~/constant/request";
import { useCartStore } from "~/store";
import { getGioHangByIdTaiKhoan } from "~/services/cart.service";
import ConvertPrice from "~/store/convertprice";

const category = ref<Category[]>([]);

const searchQuery = ref("");
const router = useRouter();
const customer = ref<User>();

const store = useCartStore();

const logoutHandler = () => {
    Cookies.remove("customer");
};

onMounted(async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const parseCustomer = JSON.parse(customerData);
            customer.value = parseCustomer;
            const listCarts = await getGioHangByIdTaiKhoan(parseCustomer._id);
            store.setCart(listCarts);
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
        }
    }

    try {
        const categoryData = await getCategory();
        category.value = categoryData;
    } catch (error) {
        console.error("Error while fetching categories:", error);
    }
});

function submitSearch() {
    if (searchQuery.value === "") {
        return;
    }
    router.push(`/search/${searchQuery.value}`);
    searchQuery.value = "";
}
</script>

<style scoped>
/* .navbar {
    background-color: var(--color-primary) !important;
    padding: 0 10%;
    min-height: 60px;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
}

.navbar-collapse {
    gap: 10px;
}
.navbar a {
    white-space: nowrap;
    text-decoration: none;
    color: #fff;
}

.navbar a:hover {
    color: var(--color-primary-two);
    background-color: transparent;
}

li {
    list-style: none;
}

.shopping i {
    font-size: 20px;
}

.user {
    display: flex;
    align-items: center;
    gap: 15px;
}
.btn,
.form-control {
    padding: 0.25rem 0.75rem;
}

::placeholder {
    font-size: 13px;
    color: var(--color-primary-two);
}

input {
    font-size: 15px;
}

.dropdown-menu {
    background-color: var(--color-primary);
}

.fa-bars {
    color: #fff;
}

.img_user {
    height: 40px;
    width: 40px;
    border-radius: 50%;
    cursor: pointer;
}

.user p {
    margin: 0;
    color: #fff;
    cursor: pointer;
}

.booking-link {
    position: relative;
    display: inline-block; 
}

.booking-link::after {
    content: "Mới"; 
    position: absolute;
    top: -5px; 
    right: -20px; 
    font-size: 10px; 
    color: red; 
    background-color: yellow; 
    padding: 2px 5px; 
    border-radius: 5px; 
    font-weight: bold; 
} */

.navbar {
    background-color: #ffffff !important;
    padding: 0.5rem 10%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    font-family: "Montserrat", sans-serif;
    position: sticky;
    top: 0;
    z-index: 999;
}

.navbar a {
    color: #333;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
    text-decoration: none;
}

.navbar a:hover {
    color: var(--color-primary);
}

.navbar .nav-item {
    margin: 0 8px;
}

.navbar-brand img {
    border-radius: 8px;
    border: 2px solid var(--color-primary);
}

.navbar-toggler {
    border: none;
    background: transparent;
}

.fa-bars {
    font-size: 1.2rem;
    color: var(--color-primary);
}

form[role="search"] {
    min-width: 250px;
    margin: 0 15px;
}

form[role="search"] input {
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #ccc;
    padding-right: 40px;
}

form[role="search"] input:focus {
    border-color: var(--color-primary);
    box-shadow: none;
    background-color: #fff;
}

form[role="search"] button {
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    padding: 0.375rem 0.75rem;
    font-size: 15px;
}

form[role="search"] button:hover {
    background-color: #5cc14f;
}

.user {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}

.img_user {
    height: 38px;
    width: 38px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--color-primary);
}

.user p {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #333;
}

.dropdown-menu {
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.dropdown-menu .dropdown-item {
    font-size: 0.9rem;
    padding: 8px 20px;
    color: #333;
    transition: background-color 0.2s;
}

.dropdown-menu .dropdown-item:hover {
    background-color: var(--color-primary-two);
    color: #111;
}

.menu_item_right {
    display: flex;
    align-items: center;
    gap: 15px;
}

.booking-link {
    position: relative;
}

.booking-link::after {
    content: "Mới";
    position: absolute;
    top: -5px;
    right: -25px;
    font-size: 10px;
    background-color: var(--color-sale);
    color: white;
    padding: 2px 5px;
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

@media (max-width: 992px) {
    .navbar {
        padding: 0.5rem 5%;
    }

    .navbar .nav-item {
        margin: 0 6px;
    }

    .navbar a {
        font-size: 0.9rem;
    }

    form[role="search"] {
        min-width: unset;
        width: 100%;
        margin: 10px 0;
    }

    form[role="search"] input {
        width: 100%;
        font-size: 13px;
    }

    form[role="search"] button {
        font-size: 13px;
    }

    .menu_item_right {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        padding: 10px 15px;
    }

    .menu_item_right > div {
        width: 100%;
    }

    .user p {
        font-size: 0.85rem;
    }

    .img_user {
        height: 32px;
        width: 32px;
    }

    .booking-link::after {
        top: -2px;
        right: -20px;
        font-size: 9px;
    }
}

@media (max-width: 576px) {
    .navbar {
        padding: 0.4rem 4%;
    }

    .navbar-brand img {
        height: 36px;
    }

    .navbar-toggler {
        font-size: 1.1rem;
    }

    .dropdown-menu {
        width: 100%;
        left: 0 !important;
        right: 0 !important;
        border-radius: 0;
    }

    .dropdown-menu .dropdown-item {
        padding: 10px 16px;
        font-size: 0.95rem;
    }
}
</style>
