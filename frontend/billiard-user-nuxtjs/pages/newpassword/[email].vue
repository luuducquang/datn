<template>
    <div class="reset-container">
        <div class="card shadow reset-form">
            <div class="card-body">
                <h2 class="text-center mb-3">Đặt lại mật khẩu</h2>

                <form @submit.prevent="handleResetPassword">
                    <div class="mb-3">
                        <label for="otp" class="form-label">Mã OTP:</label>
                        <input
                            v-model="otp"
                            id="otp"
                            type="text"
                            class="form-control"
                            placeholder="Nhập mã OTP"
                            required
                        />
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label"
                            >Mật khẩu mới:</label
                        >
                        <input
                            v-model="password"
                            id="password"
                            type="password"
                            class="form-control"
                            placeholder="Nhập mật khẩu mới"
                            required
                        />
                    </div>

                    <div class="mb-3">
                        <label for="confirmPassword" class="form-label"
                            >Xác nhận mật khẩu:</label
                        >
                        <input
                            v-model="confirmPassword"
                            id="confirmPassword"
                            type="password"
                            class="form-control"
                            placeholder="Nhập lại mật khẩu"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        class="btn btn-primary w-100 mb-2"
                        :disabled="loading"
                    >
                        <span
                            v-if="loading"
                            class="spinner-border spinner-border-sm me-2"
                        ></span>
                        <span>{{
                            loading ? "Đang cập nhật..." : "Cập nhật mật khẩu"
                        }}</span>
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { resetPasswordWithOtp } from "~/services/registry.service";
import axios from "axios";
import Swal from "sweetalert2";
import { useHead } from '@unhead/vue'

useHead({
  title: 'Quên mật khẩu'
})

definePageMeta({
    layout: "onlychildren",
});

const otp = ref("");
const password = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const route = useRoute();
const router = useRouter();

const email = ref("");

const handleResetPassword = async () => {
    if (password.value !== confirmPassword.value) {
        Swal.fire("Thông báo", "Mật khẩu xác nhận không khớp!", "warning");
        return;
    }

    loading.value = true;
    const emailParam = route.params.email;
    email.value = atob(emailParam);
    try {
        await resetPasswordWithOtp({
            email: email.value,
            otp: otp.value,
            new_password: password.value,
        });

        Swal.fire(
            "Thành công",
            "Mật khẩu đã được cập nhật thành công!",
            "success"
        );

        setTimeout(() => {
            router.push("/login");
        }, 1500);
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Swal.fire("Lỗi", error.response?.data.detail, "error");
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.reset-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: var(--color-bg);
}

.reset-form {
    width: 400px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 12px;
}

.card-body h2 {
    color: #343a40;
    font-size: 1.75rem;
    font-weight: 600;
}

.card-body p {
    font-size: 14px;
    margin: 0;
}

.form-label {
    color: #343a40;
    font-size: 14px;
}

input.form-control {
    border: 1px solid #ced4da;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

input.form-control:focus {
    border-color: var(--color-primary);
    box-shadow: none;
    background-color: #fff;
}

button.btn-primary {
    background-color: var(--color-primary);
    border: none;
    padding: 10px;
    font-size: 1rem;
    color: #fff;
    transition: all 0.3s ease;
}

button.btn-primary:hover {
    background-color: #5cc84a;
    color: #fff;
}
</style>
