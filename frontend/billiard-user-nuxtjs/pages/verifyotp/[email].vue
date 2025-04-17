<template>
    <div class="verify-container">
        <div class="card verify-form">
            <div class="card-body">
                <h3>Xác thực OTP</h3>
                <form @submit.prevent="handleVerify">
                    <div class="mb-3">
                        <label for="otp">Mã OTP:</label>

                        <input
                            v-model="otp"
                            id="otp"
                            type="text"
                            class="form-control"
                            placeholder="Nhập mã OTP"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        class="btn btn-success w-100"
                        :disabled="loading"
                    >
                        <span
                            v-if="loading"
                            class="spinner-border spinner-border-sm me-2"
                        ></span>
                        <span>{{
                            loading ? "Đang xác thực..." : "Xác thực"
                        }}</span>
                    </button>
                </form>
                <alert-toast :visible="alertVisible" :message="message" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

definePageMeta({
    layout: "onlychildren",
});

const otp = ref("");
const route = useRoute();
const router = useRouter();
const email = ref("");
const loading = ref(false);
const alertVisible = ref(false);
const message = ref("");

onMounted(() => {
    if (route.query.e) {
        try {
            email.value = atob(route.query.e);
        } catch (e) {
            message.value = "Đường dẫn không hợp lệ!";
            alertVisible.value = true;
        }
    }
});

const handleVerify = async () => {
    loading.value = true;
    try {
        await verifyOtp({
            email: email.value,
            otp: otp.value,
        });
        message.value = "Xác thực thành công!";
        alertVisible.value = true;
        setTimeout(() => router.push("/login"), 1000);
    } catch (err) {
        if (axios.isAxiosError(err)) {
            message.value = err.response?.data.detail || "Lỗi xác thực";
            alertVisible.value = true;
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.verify-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
.verify-form {
    width: 400px;
}
</style>
