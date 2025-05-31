<template>
    <div class="topup-page d-flex justify-content-center align-items-center">
        <div class="topup-card card p-4 shadow-lg">
            <h2 class="text-center mb-3">Nạp tiền</h2>

            <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                    <label class="form-label mb-2">Chọn mệnh giá</label>
                    <div class="d-flex flex-wrap gap-2 mb-2">
                        <button
                            v-for="value in fixedAmounts"
                            :key="value"
                            type="button"
                            class="btn btn-outline-light btn-sm"
                            @click="selectAmount(value)"
                        >
                            {{ formatCurrency(value) }}
                        </button>
                    </div>
                    <input
                        type="text"
                        class="form-control"
                        placeholder="Hoặc nhập số tiền khác"
                        :value="displayAmount"
                        @input="onInput"
                        required
                    />
                </div>

                <div class="mb-3">
                    <label for="paymentMethod" class="form-label"
                        >Phương thức thanh toán</label
                    >
                    <div class="form-check">
                        <input
                            class="form-check-input"
                            type="radio"
                            value="momo"
                            v-model="paymentMethod"
                            @click="ChangeMethod"
                        />
                        <label class="form-check-label" for="momo">
                            Thanh toán bằng MoMo
                        </label>
                    </div>
                    <div class="form-check">
                        <input
                            class="form-check-input"
                            type="radio"
                            value="paypal"
                            v-model="paymentMethod"
                            @click="ChangeMethod"
                        />
                        <label class="form-check-label" for="paypal">
                            Thanh toán bằng PayPal
                        </label>
                    </div>
                </div>

                <div v-if="momoPayUrl" class="text-center mt-3">
                    <p class="mb-3">Quét mã QR bên dưới để thanh toán:</p>
                    <img
                        :src="`https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(
                            momoPayUrl
                        )}`"
                        alt="QR MoMo"
                    />
                </div>

                <div
                    v-if="isPaypal"
                    class="mt-3 mb-3 d-flex justify-content-center"
                >
                    <PayPalButton
                        :amount="Number(amount)"
                        :onSuccess="handleSuccess"
                    />
                </div>

                <button
                    v-if="!isPaypal && !momoPayUrl"
                    type="submit"
                    class="btn btn-light w-100 fw-bold"
                >
                    Nạp tiền
                </button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";
import {
    getInformation,
    updateInformationWalletPoint,
} from "~/services/information.service";
import { captureMomoOrder, createMomoOrder } from "~/services/momo.service";
import { login } from "~/services/login.service";
import Swal from "sweetalert2";

const amount = ref("");
const paymentMethod = ref("momo");
const fixedAmounts = [10000, 20000, 50000, 100000, 500000];
const displayAmount = ref("");
const isPaypal = ref(false);
const momoPayUrl = ref("");
const orderId = ref("");
const router = useRouter();

const selectAmount = (value: any) => {
    amount.value = value;
};

const formatCurrency = (val: any) => {
    if (!val) return "";
    const numberVal = val.toString().replace(/\D/g, "");
    if (!numberVal) return "";
    return Number(numberVal).toLocaleString("vi-VN");
};

watch(amount, (newVal) => {
    displayAmount.value = formatCurrency(newVal);
});

const onInput = (e: any) => {
    const rawValue = e.target.value;
    const numericValue = rawValue.replace(/\D/g, "");
    amount.value = numericValue;
    displayAmount.value = formatCurrency(numericValue);
};

const ChangeMethod = () => {
    momoPayUrl.value = "";
    isPaypal.value = false;
};

const handleSuccess = async () => {
    const customer = JSON.parse(customerData ?? "{}");
    const dataUser = await getInformation(customer._id);
    await updateInformationWalletPoint({
        _id: customer._id,
        username: customer.username,
        password: customer.password,
        fullname: customer.fullname,
        email: customer.email,
        phone: customer.phone,
        address: customer.address,
        avatar: customer.avatar,
        loyalty_points: dataUser.loyalty_points,
        wallet: Number(dataUser.wallet) + Number(amount.value),
        role_name: customer.role_name,
    });

    const res = await login({
        email: String(dataUser.email),
        password: String(customer.password),
    });
    Cookies.set("customer", JSON.stringify(res), { expires: 1 });

    Swal.fire(
        "Thành công",
        `Nạp tiền thành công mệnh giá ${displayAmount.value} VND`,
        "success"
    );
    ChangeMethod();
};

async function createMoMoPayment() {
    try {
        const res = await createMomoOrder(Number(amount.value));
        if (res && res.payUrl && res.orderId) {
            momoPayUrl.value = res.payUrl;
            orderId.value = res.orderId;

            const checkStatusInterval = setInterval(async () => {
                const status = await captureMomoOrder(orderId.value);
                if (status.resultCode === 0) {
                    clearInterval(checkStatusInterval);
                    handleSuccess();
                    console.log("a");
                }
            }, 5000);
        } else {
            alert("Không lấy được link MoMo!");
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Swal.fire("Lỗi", `${error}`, "error");
            console.log(error);
        }
    }
}

const handleSubmit = () => {
    if (paymentMethod.value === "momo") {
        createMoMoPayment();
    } else if (paymentMethod.value === "paypal") {
        isPaypal.value = true;
    }
};

const customerData = Cookies.get("customer");
const fetchDataCart = async () => {
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
            router.push("/login");
        }
    } else {
        router.push("/login");
    }
};

onMounted(async () => {
    fetchDataCart();
});
</script>

<style scoped>
.topup-page {
    background-color: #f5faff;
    padding: 3rem;
}

.topup-card {
    background-color: #ffffff;
    max-width: 600px;
    width: 100%;
    border-radius: 1rem;
    padding: 3rem 4rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.topup-card h2 {
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--color-primary);
}

.topup-card p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #444;
}

.form-label {
    font-size: 1.1rem;
    color: var(--color-primary);
    font-weight: 600;
}

input.form-control,
select.form-select {
    font-size: 1.1rem;
    padding: 0.6rem 1rem;
    border-radius: 0.5rem;
    border: 1px solid #ced4da;
}

input.form-control:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn {
    font-size: 1.1rem;
    padding: 0.6rem 1.2rem;
    border-radius: 0.5rem;
}

.d-flex.flex-wrap.gap-2.mb-2 button.btn-outline-light {
    border: 1px solid var(--color-primary);
    color: var(--color-primary);
    background-color: #fff;
    transition: all 0.2s ease;
}

.d-flex.flex-wrap.gap-2.mb-2 button.btn-outline-light:hover {
    background-color: var(--color-primary);
    color: #fff;
}

button.btn-light.w-100.fw-bold {
    background-color: var(--color-primary);
    color: #fff;
    font-weight: 600;
    padding: 0.75rem 1rem;
    font-size: 1.2rem;
    transition: background-color 0.3s ease;
    border: none;
}

button.btn-light.w-100.fw-bold:hover {
    background-color: #0056b3;
}

.form-check-input:checked {
    background-color: var(--color-primary);
    border-color: var(--color-primary);
}
</style>
