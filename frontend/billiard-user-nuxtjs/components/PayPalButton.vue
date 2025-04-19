<template>
    <div id="paypal-button"></div>
</template>

<script setup>
import { onMounted } from "vue";
import { loadScript } from "@paypal/paypal-js";
import {
    capturePaypalOrder,
    createPaypalOrder,
} from "~/services/payment.service";

const props = defineProps({
    amount: {
        type: Number,
        required: true,
    },
    onSuccess: {
        type: Function,
        required: true,
    },
});

onMounted(async () => {
    const paypal = await loadScript({
        clientId:
            "AevnZPJJW8_kjKZW3V2nrryVCEreZzQJXFodD54xoNJaXLLEF8hh3863ld1FWjY3w1QJDUbx9UrobbHr",
    });

    if (paypal) {
        paypal
            .Buttons({
                createOrder: async () => {
                    const data = await createPaypalOrder(props.amount);
                    return data.id;
                },
                onApprove: async (data) => {
                    const result = await capturePaypalOrder(data.orderID);
                    props.onSuccess(result);
                },
            })
            .render("#paypal-button");
    }
});
</script>
