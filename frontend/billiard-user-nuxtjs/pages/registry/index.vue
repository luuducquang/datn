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
                                <label
                                    for="terms"
                                    class="form-check-label check_conditon"
                                >
                                    Tôi đã đọc và đồng ý với
                                    <a href="#">điều khoản chung</a> và
                                    <a href="#"
                                        >chính sách bảo mật của Q-Billiard
                                        Club</a
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
            const emailencode = btoa(email.value);
            const passwordencode = btoa(password.value);
            router.push(`/verifyotp/${emailencode}-${passwordencode}-true`);
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
    background-color: var(--color-bg);
    padding: 20px;
    font-size: 14px;
}

.registry-form {
    width: 100%;
    max-width: 480px;
}

.card {
    border-radius: 16px;
    background-color: #ffffff;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    border: none;
}

.card-body {
    padding: 2rem;
}

.card-title {
    color: #343a40;
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}

.form-label {
    font-weight: 500;
    color: #343a40;
}

.form-control {
    border: 1px solid #ced4da;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

.form-control:focus {
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

.form-check-label {
    color: #495057;
    font-size: 13px;
}

.form-check-label a {
    color: var(--color-primary);
    text-decoration: underline;
}

.goto_login {
    color: var(--color-primary);
    font-weight: 500;
}

.goto_login:hover {
    color: #145c32;
    text-decoration: underline;
}
</style>
