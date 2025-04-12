<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/invoice">Đơn hàng của bạn</NuxtLink>
        </div>
        <item-invoice :billsell="dataInvoice" />
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import Cookies from "js-cookie";
import { useRouter } from "vue-router";
import { type BillSells } from "~/constant/api";
import { getInvoiceAll } from "~/services/invoice.servie";

const router = useRouter();

const dataInvoice = ref<BillSells[]>([]);

const fetchData = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            const dataFetch = await getInvoiceAll(customer._id);
            dataInvoice.value = dataFetch;
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
    background: linear-gradient(90deg, var(--color-primary) 0%, #001815 100%) 0%
        0% no-repeat;
    padding: 10px;
    color: #fff;
    margin-top: 10px;
}

.type a {
    text-decoration: none;
    color: #ddd;
    font-size: 14px;
    text-transform: uppercase;
}

.type i {
    color: #fff;
    font-size: 10px;
    padding: 0 10px;
}
</style>
