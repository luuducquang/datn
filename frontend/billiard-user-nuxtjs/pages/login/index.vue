<template>
    <div class="login-container">
        <div class="login-form card">
            <div class="card-body">
                <h2 class="login-form-title">Q-Billiard Club</h2>
                <form @submit.prevent="onFinish">
                    <div class="form-group mb-3">
                        <input
                            type="text"
                            id="email"
                            v-model="email"
                            class="form-control"
                            required
                            placeholder="Email"
                        />
                    </div>
                    <div class="form-group mb-3">
                        <input
                            type="password"
                            id="password"
                            v-model="password"
                            class="form-control"
                            required
                            placeholder="Mật khẩu"
                        />
                    </div>
                    <!-- <div class="form-check mb-3 d-flex remember_item"> -->
                    <!-- <input
                            type="checkbox"
                            id="remember"
                            v-model="remember"
                            class="form-check-input"
                        /> -->
                    <!-- <label
                            for="remember"
                            class="form-check-label text-white remember_label"
                        >
                            Remember username
                        </label> -->
                    <!-- </div> -->

                    <button
                        type="submit"
                        class="btn btn-primary w-100 d-flex justify-content-center align-items-center login_btn"
                        :disabled="loading"
                    >
                        <span
                            v-if="loading"
                            class="spinner-border spinner-border-sm me-2"
                            role="status"
                            aria-hidden="true"
                        ></span>
                        <span>{{
                            loading ? "Đang xử lý..." : "Đăng nhập"
                        }}</span>
                    </button>

                    <NuxtLink class="createAccount" to="/registry"
                        >Tạo tài khoản</NuxtLink
                    >
                </form>
            </div>
            <div class="text-center mt-3">
                <p style="color: #fff; font-size: 11px">
                    Phần mềm quản lý quán bi-a
                    <i class="fa-solid fa-copyright"></i> Q-Billiard Club 2025
                    NuxtJs by LuuDucQuang
                </p>
            </div>
        </div>
    </div>
    <alert-toast :visible="alertVisible" :message="title" />
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "~/services/login.service";
import Cookies from "js-cookie";
import axios from "axios";

definePageMeta({
    layout: "onlychildren",
});

const email = ref("");
const password = ref("");
const remember = ref(false);
const loading = ref(false);
const router = useRouter();
const alertVisible = ref(false);
const title = ref("");

const onFinish = async () => {
    loading.value = true;
    try {
        const res = await login({
            email: email.value,
            password: password.value,
        });
        res.isRemember = remember.value;

        await loginSuccess(res);
    } catch (error) {
        if (axios.isAxiosError(error)) {
            alertVisible.value = true;
            const status = error.response?.status;
            title.value = error.response?.data.detail;

            if (status === 403) {
                title.value = "Tài khoản chưa được xác thực.";

                const encoded = email.value;
                const emailencode = btoa(encoded);

                setTimeout(() => {
                    router.push(`/verifyotp/${emailencode}`);
                    alertVisible.value = false;
                }, 2000);
            }

            setTimeout(() => {
                alertVisible.value = false;
            }, 2000);
        }
    } finally {
        loading.value = false;
    }
};

const loginSuccess = async (res) => {
    Cookies.set("customer", JSON.stringify(res), { expires: 1 });
    router.push("/");
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #e6e8e4;
}

.login-form {
    width: 400px;
    padding: 20px;
    background-color: var(--color-primary);
}

.login-form-title {
    text-align: center;
    font-size: 20px;
    margin-bottom: 20px;
    color: #fff;
}

.btn-primary {
    background-color: var(--color-second-text);
}

::placeholder {
    color: #c1c1c1;
    font-size: 14px;
}

input {
    font-size: 14px;
}

.remember_label {
    font-size: 14px;
}

.remember_label a {
    color: #ffffff;
}

.remember_label a:hover {
    color: #94ef91;
}

/* .remember_item {
    gap: 7px;
} */

.createAccount {
    color: #fff;
    padding-top: 5px;
    float: right;
    padding-top: 5px;
}

.createAccount:hover {
    color: #94ef91;
}

.remember_item input:hover {
    cursor: pointer;
}

.login_btn {
    border: 1px;
    transition: all 0.2s ease-in-out;
}

.login_btn:hover {
    transform: scale(1.05);
}
</style>
