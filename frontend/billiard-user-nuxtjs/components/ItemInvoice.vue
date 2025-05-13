<template>
    <div v-show="billsell.length === 0">
        <h4 class="text-center m-0 pt-3">Bạn chưa có đơn hàng nào</h4>
        <div class="text-center mt-2">
            <NuxtLink v-if="billsell.length === 0" to="/"
                >Quay Lại trang chủ</NuxtLink
            >
        </div>
    </div>
    <div class="accordion" id="accordionExample">
        <div
            class="accordion-item"
            v-for="(value, index) in billsell"
            :key="index"
        >
            <h2 class="accordion-header" :id="`heading${value?._id}`">
                <button
                    class="accordion-button collapsed"
                    type="button"
                    data-bs-toggle="collapse"
                    :data-bs-target="`#collapse${value?._id}`"
                    aria-expanded="false"
                    :aria-controls="`collapse${value?._id}`"
                >
                    {{
                        `${value?.name} | ${
                            value?.total_price > 0
                                ? value?.total_price.toLocaleString("DE-de")
                                : 0
                        }đ | ${value?.address_detail} | ${value?.status} | ${
                            value?.is_paid
                                ? "Đã thanh toán"
                                : "Thanh toán khi nhận hàng"
                        }`
                    }}
                </button>
            </h2>
            <div
                :id="`collapse${value?._id}`"
                class="accordion-collapse collapse"
                :aria-labelledby="`heading${value?._id}`"
                data-bs-parent="#accordionExample"
                style=""
            >
                <div
                    class=""
                    v-for="(item, index) in detailBillSells"
                    :key="index"
                >
                    <div
                        v-if="item.sell_id === value?._id"
                        class="d-flex accordion-body"
                    >
                        <img
                            :src="
                                item.product
                                    ? apiImage + item.product.image
                                    : ''
                            "
                            alt="image"
                            width="200"
                            height="200"
                        />
                        <div class="p-3">
                            <h5>
                                {{ item.product ? item.product.item_name : "" }}
                            </h5>
                            <div>
                                Số lượng:
                                {{ item.quantity }}
                            </div>
                            <div>
                                Đơn giá:
                                {{
                                    item.unit_price > 0
                                        ? item.unit_price.toLocaleString(
                                              "De-de"
                                          )
                                        : 0
                                }}đ
                            </div>
                            <div>
                                Tổng giá:
                                {{
                                    (
                                        Number(item.quantity) *
                                        Number(item.unit_price)
                                    ).toLocaleString("De-de")
                                }}đ
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <div
                    v-if="value.trangThai === 'Đang xử lý'"
                    class="text-center"
                >
                    <button
                        @click="cancelOrder(Number(value.maHoaDon))"
                        class="btn btn_cancel"
                    >
                        Huỷ đơn
                    </button>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick } from "vue";
import type { BillSells, SellItems } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { getInvoiceById } from "~/services/invoice.service";

const props = defineProps<{
    billsell: BillSells[];
}>();

const detailBillSells = ref<SellItems[]>([]);

// onMounted(async () => {
//     await nextTick();
//     console.log(props.billsell);
// });

const fetchData = () => {
    setTimeout(async () => {
        const listDetail = await Promise.all(
            props.billsell.map(async (value) => {
                const dataDetail = await getInvoiceById(String(value._id));
                return dataDetail;
            })
        );
        detailBillSells.value = listDetail.flat();
    }, 1000);
};

onMounted(() => {
    fetchData();
});

const cancelOrder = (id: number) => {
    console.log(id);
};
</script>

<style lang="css" scoped>
.btn_cancel {
    border: none;
    padding: 7px 10px;
    background-color: #ff0033;
    outline: none;
    color: #fff;
    margin-bottom: 10px;
}

.btn_cancel:hover {
    opacity: 0.8;
}
</style>
