<template>
    <div class="forgot-container">
        <div class="card shadow forgot-form">
            <div class="card-body">
                <h2 class="text-center mb-3">Quên mật khẩu</h2>

                <form @submit.prevent="handleSubmit">
                    <div class="mb-3">
                        <label for="email" class="form-label">Email:</label>
                        <input
                            v-model="email"
                            id="email"
                            type="email"
                            class="form-control"
                            placeholder="Nhập email của bạn"
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
                            loading ? "Đang gửi..." : "Gửi mã xác nhận"
                        }}</span>
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { sendForgotPasswordOtp } from "~/services/registry.service";
import axios from "axios";
import Swal from "sweetalert2";
import { useHead } from '@unhead/vue'

definePageMeta({
    layout: "onlychildren",
});

useHead({
  title: 'Quên mật khẩu'
})

const email = ref("");
const loading = ref(false);
const router = useRouter();

const handleSubmit = async () => {
    loading.value = true;
    try {
        await sendForgotPasswordOtp({ email: email.value });

        Swal.fire("Thành công", "Mã xác nhận đã được gửi tới email!", "success");

        const emailencode = btoa(email.value);

        setTimeout(() => {
            router.push(`/newpassword/${emailencode}`);
        }, 1000);
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
.forgot-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: var(--color-bg);
}

.forgot-form {
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
