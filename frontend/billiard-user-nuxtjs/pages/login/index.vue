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

                    <div class="d-flex justify-content-between">
                        <NuxtLink class="createAccount" to="/forgotpass"
                            >Quên mật khẩu</NuxtLink
                        >

                        <NuxtLink class="createAccount" to="/registry"
                            >Tạo tài khoản</NuxtLink
                        >
                    </div>
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
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "~/services/login.service";
import Cookies from "js-cookie";
import axios from "axios";
import Swal from "sweetalert2";
import { useHead } from '@unhead/vue'

useHead({
  title: 'Đăng nhập'
})

definePageMeta({
    layout: "onlychildren",
});

const email = ref("");
const password = ref("");
const remember = ref(false);
const loading = ref(false);
const router = useRouter();

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
            const status = error.response?.status;
            title.value = error.response?.data.detail;

            if (status === 403) {
                Swal.fire(
                    "Thông báo",
                    "Tài khoản chưa được xác thực.",
                    "warning"
                );

                const encoded = email.value;
                const emailencode = btoa(encoded);

                const passwordencode = btoa(password.value);

                setTimeout(() => {
                    router.push(
                        `/verifyotp/${emailencode}-${passwordencode}-false`
                    );
                }, 2000);
            }
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
    min-height: 100vh;
    background-color: var(--color-bg);
    padding: 20px;
    font-size: 14px;
}

.login-form {
    width: 100%;
    max-width: 480px;
    border-radius: 16px;
    background-color: #ffffff;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    border: none;
}

.card-body {
    padding: 2rem;
}

.login-form-title {
    color: #343a40;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
    text-align: center;
}

.form-group input {
    border: 1px solid #ced4da;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

.form-group input:focus {
    border-color: var(--color-primary);
    box-shadow: none;
    background-color: #fff;
}

.btn-primary {
    background-color: var(--color-primary);
    border: none;
    padding: 10px;
    font-size: 1rem;
    color: #fff;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background-color: #5cc84a;
    color: #fff;
}

.createAccount {
    color: var(--color-primary);
    padding-top: 10px;
    float: right;
    font-size: 14px;
    text-decoration: underline;
}

.createAccount:hover {
    color: #145c32;
    text-decoration: underline;
}

.login_btn {
    transition: all 0.2s ease-in-out;
}

.login_btn:hover {
    transform: scale(1.05);
}

::placeholder {
    color: #c1c1c1;
    font-size: 14px;
}
</style>
