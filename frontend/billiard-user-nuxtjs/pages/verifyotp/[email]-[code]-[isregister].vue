<template>
    <div class="verify-container">
        <div class="card shadow verify-form">
            <div class="card-body">
                <h2 class="text-center mb-3">Xác thực mã OTP</h2>
                <p class="text-muted text-center">
                    Mã xác thực đã gửi tới: <strong>{{ maskedEmail }}</strong>
                </p>

                <form @submit.prevent="handleVerify">
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

                    <button
                        type="submit"
                        class="btn btn-success w-100 mb-2"
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

                <div class="text-center">
                    <button
                        class="btn btn-link p-0"
                        @click="handleResendOtp"
                        :disabled="countdown > 0 || resending"
                    >
                        <span
                            v-if="resending"
                            class="spinner-border spinner-border-sm me-1"
                        ></span>
                        <span>
                            {{
                                countdown > 0
                                    ? `Gửi lại mã sau ${countdown}s`
                                    : "Gửi lại mã OTP"
                            }}
                        </span>
                    </button>
                </div>

                <alert-toast :visible="alertVisible" :message="message" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Cookies from "js-cookie";
import { maskEmail } from "~/store/maskEmail";
import { sentOtp, verifyOtp } from "~/services/registry.service";
import { login } from "~/services/login.service";

definePageMeta({
    layout: "onlychildren",
});

const otp = ref("");
const resending = ref(false);
const route = useRoute();
const router = useRouter();
const loading = ref(false);
const alertVisible = ref(false);
const message = ref("");
const email = ref("");
const pass = ref("");

const countdown = ref(60);
let countdownInterval = null;

const maskedEmail = computed(() => {
    return email.value ? maskEmail(email.value) : "";
});

const startCountdown = () => {
    countdown.value = 60;
    countdownInterval = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            clearInterval(countdownInterval);
        }
    }, 1000);
};

onMounted(async () => {
    const emailParam = route.params.email;
    const passwordParam = route.params.code;

    email.value = atob(emailParam);
    pass.value = atob(passwordParam);

    const isRegister = route.params.isregister;
    if (isRegister === "false") {
        await sentOtp({ email: email.value });
    }

    startCountdown();
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

        setTimeout(async () => {
            const res = await login({
                email: email.value,
                password: pass.value,
            });

            await loginSuccess(res);
        }, 1000);
    } catch (err) {
        if (axios.isAxiosError(err)) {
            message.value = err.response?.data.detail || "Lỗi xác thực";
            alertVisible.value = true;
        }
    } finally {
        loading.value = false;
    }
};

const handleResendOtp = async () => {
    resending.value = true;
    try {
        await sentOtp({ email: email.value });
        message.value = "Mã OTP đã được gửi lại!";
        alertVisible.value = true;
        startCountdown();
        setTimeout(() => {
            alertVisible.value = false;
        }, 2000);
    } catch (err) {
        message.value = "Gửi lại OTP thất bại!";
        alertVisible.value = true;
    } finally {
        resending.value = false;
    }
};

const loginSuccess = async (res) => {
    Cookies.set("customer", JSON.stringify(res), { expires: 1 });
    router.push("/");
};
</script>

<style scoped>
.verify-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: var(--color-bg);
}

.verify-form {
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
    color: #fff;
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

button.btn-success {
    background-color: var(--color-primary);
    border: none;
    padding: 10px;
    font-size: 1rem;
    color: #fff;
    transition: all 0.3s ease;
}

button.btn-success:hover {
    background-color: #5cc84a;
    color: #fff;
}

button.btn-link {
    font-size: 14px;
    color: #343a40;
    text-decoration: underline;
}

button.btn-link:disabled {
    color: #343a40;
    text-decoration: none;
}
</style>
