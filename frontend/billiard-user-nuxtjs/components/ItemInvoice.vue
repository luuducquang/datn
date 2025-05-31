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
                        ` ${value?.address_detail} | ${value?.status} 
                        `
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
                <div class="mx-3 mb-3 mt-3">
                    <strong class="text-primary">Tên người đặt:</strong>
                    {{ value?.name }}
                </div>
                <div class="mx-3 mb-3 mt-3">
                    <strong class="text-primary">Tổng thanh toán:</strong>
                    {{
                        value?.total_price > 0
                            ? value?.total_price.toLocaleString("DE-de")
                            : 0
                    }}
                </div>
                <div class="mx-3 mb-3">
                    <strong class="text-primary">Trạng thái: </strong>
                    <span
                        :class="value?.status ? 'text-success' : 'text-danger'"
                    >
                        {{ value?.status ? "Đã thanh toán" : "Đã huỷ" }}
                    </span>
                </div>
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
                        <div class="px-3">
                            <NuxtLink :to="`/detail/${item?.product?._id}`">
                                {{ item.product ? item.product.item_name : "" }}
                            </NuxtLink>
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
                <div class="text-center">
                    <button
                        v-if="
                            value.status != 'Huỷ đơn' &&
                            value.status === 'Đang xử lý'
                        "
                        class="btn btn-danger mb-3"
                        @click="
                            handleCancelBooking(
                                value,
                                Number(value?.total_price),
                                Boolean(value?.is_paid)
                            )
                        "
                    >
                        Huỷ đơn hàng
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Cookies from "js-cookie";
import Swal from "sweetalert2";
import { onMounted, ref, nextTick } from "vue";
import type { BillSells, SellItems } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    getInformation,
    updateInformationWalletPoint,
} from "~/services/information.service";
import { getInvoiceById, updateOrder } from "~/services/invoice.service";
import { login } from "~/services/login.service";

const props = defineProps<{
    billsell: BillSells[];
}>();

const emit = defineEmits(["refresh"]);

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

async function handleCancelBooking(
    item: BillSells,
    money_paid: number,
    is_paid: boolean
) {
    Swal.fire({
        title: "Bạn có chắc muốn huỷ đơn hàng?",
        text: is_paid
            ? `Số tiền đã thanh toán: ${money_paid.toLocaleString(
                  "de-DE"
              )}đ sẽ được chuyển vào ví của bạn`
            : `Đơn hàng sẽ bị huỷ`,

        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Có, huỷ ngay",
        cancelButtonText: "Không",
    }).then(async (result) => {
        if (result.isConfirmed) {
            const customerData = Cookies.get("customer");
            if (customerData) {
                const customer = JSON.parse(customerData);
                const dataUser = await getInformation(customer._id);

                await updateOrder({
                    _id: item._id,
                    status: "Huỷ đơn",
                    sell_date: item.sell_date,
                    total_price: item.total_price,
                    name: item.name,
                    address: item.address,
                    email: item.email,
                    phone: item.phone,
                    address_detail: item.address_detail,
                    user_id: item.user_id,
                    is_paid: item.is_paid,
                });

                if (is_paid === true) {
                    await updateInformationWalletPoint({
                        _id: customer._id,
                        username: customer.username,
                        password: customer.password,
                        fullname: customer.fullname,
                        email: customer.email,
                        phone: customer.phone,
                        address: customer.address,
                        avatar: dataUser.avatar,
                        loyalty_points:
                            Number(dataUser.loyalty_points) -
                            Number(money_paid) * 0.2,
                        wallet: Number(dataUser.wallet) + Number(money_paid),
                        role_name: customer.role_name,
                    });
                    const res = await login({
                        email: String(dataUser.email),
                        password: String(customer.password),
                    });
                    Cookies.set("customer", JSON.stringify(res), {
                        expires: 1,
                    });
                }

                emit("refresh");

                Swal.fire(
                    "Đã huỷ!",
                    "Đơn hàng đã được huỷ thành công.",
                    "success"
                );
            }
        }
    });
}
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

a {
    font-size: 20px;
    color: var(--color-primary);
}
</style>
