<template>
    <div class="container-registry">
        <div class="row justify-content-center">
            <div class="col-md-6 registry-form">
                <div class="card">
                    <div class="card-body">
                        <h2 class="card-title text-center">
                            Đăng ký tài khoản
                        </h2>
                        <form @submit.prevent="onFinish">
                            <div class="mb-3">
                                <label for="fullName" class="form-label"
                                    >Họ và tên</label
                                >
                                <input
                                    type="text"
                                    id="fullName"
                                    v-model="fullName"
                                    class="form-control"
                                    required
                                    placeholder="Họ và tên"
                                />
                            </div>
                            <!-- <div class="mb-3">
                                <label for="phone" class="form-label"
                                    >Nhập số điện thoại</label
                                >
                                <input
                                    type="text"
                                    id="phone"
                                    v-model="phone"
                                    class="form-control"
                                    required
                                    placeholder="Nhập số điện thoại"
                                />
                            </div> -->
                            <div class="mb-3">
                                <label for="email" class="form-label"
                                    >Email</label
                                >
                                <input
                                    type="email"
                                    id="email"
                                    v-model="email"
                                    class="form-control"
                                    required
                                    placeholder="Nhập địa chỉ email"
                                />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label"
                                    >Mật khẩu</label
                                >
                                <input
                                    type="password"
                                    id="password"
                                    v-model="password"
                                    class="form-control"
                                    required
                                    placeholder="Mật khẩu"
                                />
                            </div>
                            <div class="mb-3">
                                <label for="confirmPassword" class="form-label"
                                    >Nhập lại mật khẩu</label
                                >
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    v-model="confirmPassword"
                                    class="form-control"
                                    required
                                    placeholder="Nhập lại mật khẩu"
                                />
                            </div>
                            <div class="mb-3 form-check">
                                <input
                                    type="checkbox"
                                    id="terms"
                                    v-model="acceptTerms"
                                    class="form-check-input"
                                    required
                                />
                                <label for="terms" class="form-check-label check_conditon">
                                    Tôi đã đọc và đồng ý với
                                    <a href="#">điều khoản chung</a> và
                                    <a href="#"
                                        >chính sách bảo mật của Q-Billiard Club</a
                                    >
                                </label>
                            </div>
                            <button
                                type="submit"
                                class="btn btn-primary w-100 d-flex justify-content-center align-items-center"
                                :disabled="loading"
                            >
                                <span
                                    v-if="loading"
                                    class="spinner-border spinner-border-sm me-2"
                                    role="status"
                                    aria-hidden="true"
                                ></span>
                                <span>{{
                                    loading ? "Đang xử lý..." : "Đăng ký"
                                }}</span>
                            </button>
                            <div class="text-center mt-3">
                                <p>
                                    Tôi đã có tài khoản
                                    <NuxtLink class="goto_login" to="/login"
                                        >Đăng nhập</NuxtLink
                                    >
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <alert-toast :visible="alertVisible" :message="title" />
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { registryUser } from "~/services/registry.service";
import axios from "axios";

definePageMeta({
    layout: "onlychildren",
});

const fullName = ref("");
const phone = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const acceptTerms = ref(false);
const loading = ref(false);
const router = useRouter();
const alertVisible = ref(false);
const title = ref("");

const onFinish = async () => {
    loading.value = true;
    try {
        await registryUser({
            email: String(email.value),
            password: String(password.value),
            fullname: String(fullName.value),
            address: "",
            avatar: "/static/uploads/user.jpg",
            loyalty_points: 0,
            role_name: "USER",
        });
        alertVisible.value = true;
        title.value = "Đăng ký tài khoản thành công !";
        setTimeout(() => {
            router.push("/login");
            alertVisible.value = false;
        }, 1000);
    } catch (error) {
        if (axios.isAxiosError(error)) {
            alertVisible.value = true;
            title.value = error.response?.data.detail;
            setTimeout(() => {
                alertVisible.value = false;
            }, 2000);
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.container-registry {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #e6e8e4;
    padding: 20px;
    font-size: 14px;
}

.card {
    border-radius: 15px;
    background-color: var(--color-primary);
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
}

::placeholder {
    font-size: 14px;
}

.registry-form {
    width: 500px;
}

.card-body {
    padding: 30px;
}

.card-title {
    color: #fff;
    font-size: 1.5rem;
    margin-bottom: 20px;
}

.btn-primary {
    background-color: var(--color-second-text);
    border: none;
    padding: 10px;
    font-size: 1rem;
}

.btn-primary:hover {
    background-color: #fff;
    color: var(--color-primary);
}

.form-check-label a {
    color: #fff;
    text-decoration: underline;
}

.form-check-label a:hover {
    color: #ddd;
}

.text-center p {
    color: #fff;
    margin-top: 10px;
}

.form-label {
    color: #fff;
}

.form-control {
    background-color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px;
    font-size: 14px;
    /* border: 1px; */
}

.form-control:focus {
    box-shadow: none;
    /* border: 1px solid #20b2aa; */
}

.form-check-input {
    margin-top: 0.3em;
}

.mt-3 {
    margin-top: 1rem !important;
}

.mb-3 {
    margin-bottom: 1rem !important;
}

.text-center {
    text-align: center !important;
}

.goto_login {
    color: #fff;
}

.goto_login:hover {
    color: #68da5b;
}

.check_conditon{
    color: #fff;
}
</style>
