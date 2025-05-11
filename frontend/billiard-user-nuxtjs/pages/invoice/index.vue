<template>
    <div class="container mb-3">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/invoice">Lịch sử đơn hàng</NuxtLink>
        </div>
        <div class="mt-3"><item-invoice :billsell="dataInvoice" /></div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import { useRouter } from "vue-router";
import { type BillSells } from "~/constant/api";
import { getInvoiceAll } from "~/services/invoice.service";

const router = useRouter();

const dataInvoice = ref<BillSells[]>([]);

const fetchData = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            const dataFetch = await getInvoiceAll(customer._id);
            dataInvoice.value = dataFetch.reverse();
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
    fetchData();
});
</script>

<style lang="css" scoped>
.type {
    background: linear-gradient(
        90deg,
        var(--color-primary),
        var(--color-linear-gradient)
    );
    padding: 12px 20px;
    color: var(--color-text);
    margin-top: 10px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    font-size: 13px;
}

.type a {
    text-decoration: none;
    color: var(--color-text);
    font-size: 13px;
    text-transform: uppercase;
    font-weight: 600;
    transition: color 0.3s;
}

.type a:hover {
    color: #eaffd0;
}

.type i {
    color: var(--color-text);
    font-size: 12px;
    margin: 0 8px;
}
</style>
