<template>
    <div>
        <div class="container">
            <div
                v-for="(value, index) in dataCart"
                :key="index"
                :class="`item${index}`"
                class="row pt-3 pb-3 border-top"
            >
                <div v-if="order === false" class="col-1 align-content-center">
                    <input
                        type="checkbox"
                        :checked="value.status"
                        class="form-check-input checkbox_btn"
                        @click="handlerChecked(value)"
                    />
                </div>
                <div
                    :class="[
                        { 'col-5': order === false },
                        { 'col-7': order === true },
                    ]"
                    class="align-content-center"
                >
                    <div class="info_item_cart">
                        <img
                            :src="apiImage + value.rentalitem?.image"
                            class="img-thumbnail"
                        />
                        <span class="item">
                            <NuxtLink
                                :to="`/detail/${value.rentalitem?._id}`"
                                class="text-decoration-none text-dark nameItem"
                            >
                                {{ value.rentalitem?.item_name }}
                            </NuxtLink>
                        </span>
                    </div>
                </div>
                <div class="col-2 align-content-center">
                    <div
                        class="d-flex flex-column justify-content-center align-items-center price_cart"
                    >
                        <p>
                            <span
                                class="text-muted text-decoration-line-through"
                            >
                                {{
                                    Number(value?.rentalitem?.price) > 0
                                        ? Number(
                                              value?.rentalitem?.price
                                          ).toLocaleString("DE-de")
                                        : 0
                                }}
                            </span>
                            <sup class="text-muted">đ</sup>
                        </p>
                        <p>
                            <span class="text-dark">{{
                                Number(value?.rentalitem?.price_reduction) > 0
                                    ? Number(
                                          value?.rentalitem?.price_reduction
                                      ).toLocaleString("DE-de")
                                    : 0
                            }}</span>
                            <sup>đ</sup>
                        </p>
                    </div>
                </div>
                <div class="col-3 align-content-center">
                    <div class="d-flex justify-content-center list_btn_amount">
                        <i class="fa-solid fa-minus" @click="minus(value)" />
                        <input
                            type="text"
                            class="form-control text-center input_amount"
                            :value="value.quantity"
                            min="1"
                            max="99"
                            @input="validateInput($event, value)"
                        />
                        <i class="fa-solid fa-plus" @click="plus(value)" />
                    </div>
                </div>
                <div v-if="order === false" class="col-1 align-content-center">
                    <p class="del_btn" @click="deleteCart(value)">Xoá</p>
                </div>
            </div>
        </div>
        <div v-if="order === false" class="pay">
            <div class="price-total-cart">
                <p>Tiền tạm tính:</p>
                <span class="totalPriceCart">{{
                    totalPrice > 0 ? totalPrice.toLocaleString("DE-de") : 0
                }}</span>
                <sup>đ</sup>
            </div>
            <NuxtLink v-show="totalPrice > 0" @click="buyNow" class="goOrder"
                >Tiến hành đặt hàng</NuxtLink
            >
        </div>
    </div>

    <alert-toast :visible="alertVisible" :message="titleAddItem" />
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";
import { useCartStore } from "~/store";
import { type Cart } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    deleteCarts,
    getGioHangByIdTaiKhoan,
    updateCart,
} from "~/services/cart.service";
import axios from "axios";
import { checkQuantityItems } from "~/services/home.service";

const alertVisible = ref(false);
const titleAddItem = ref("");

const router = useRouter();
const props = defineProps<{
    dataCart: Cart[];
    totalPrice: number;
    fetch: Function;
    order: boolean;
}>();

const store = useCartStore();

const buyNow = async () => {
    try {
        if (props.dataCart.length > 0) {
            const listitems = props.dataCart.reduce(
                (acc: { ids: string[]; quantities: number[] }, value: Cart) => {
                    acc.ids.push(value.item_id);
                    acc.quantities.push(value.quantity);
                    return acc;
                },
                { ids: [], quantities: [] }
            );

            const checkQuantity = await checkQuantityItems(listitems);
            if (checkQuantity) {
                router.push("/order");
            }
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            titleAddItem.value = `${error.response?.data?.detail?.insufficient_items.item_name} không đủ số lượng, trong kho chỉ còn ${error.response?.data?.detail?.insufficient_items?.quantity_available} sản phẩm`;
            alertVisible.value = true;
            setTimeout(() => {
                alertVisible.value = false;
            }, 3000);
        }
    }
};

const handlerChecked = async (item: Cart) => {
    await updateCart({
        _id: String(item._id),
        item_id: item.item_id,
        user_id: "",
        quantity: item.quantity,
        status: !item.status,
    });
    props.fetch();
};

const minus = async (item: Cart) => {
    if (item.quantity > 1) {
        await updateCart({
            _id: String(item._id),
            item_id: item.item_id,
            user_id: "",
            quantity: item.quantity - 1,
            status: item.status,
        });
        props.fetch();
    }
};

const validateInput = (event: Event, item: Cart) => {
    const target = event.target as HTMLInputElement;
    let value = target.value.replace(/[^0-9]/g, "");

    if (value === "" || parseInt(value) === 0) {
        value = "1";
    }

    target.value = value;

    setTimeout(async () => {
        await updateCart({
            _id: String(item._id),
            item_id: item.item_id,
            user_id: "",
            quantity: value,
            status: item.status,
        });
        props.fetch();
    }, 1000);
};

// const updateInput = async (item: Cart, event: Event) => {
//     const target = event.target as HTMLInputElement;
//     let value = parseInt(target.value, 10);

//     if (isNaN(value) || value < 1) {
//         value = 1;
//     } else if (value > 99) {
//         value = 99;
//     }

//     target.value = value.toString();
//     console.log(value);

// };

const plus = async (item: Cart) => {
    await updateCart({
        _id: String(item._id),
        item_id: item.item_id,
        user_id: "",
        quantity: item.quantity + 1,
        status: item.status,
    });
    props.fetch();
};

const deleteCart = async (item: Cart) => {
    await deleteCarts(String(item._id));
    props.fetch();
    const customerData = Cookies.get("customer");
    if (customerData) {
        const customer = JSON.parse(customerData);
        const cartOld = await getGioHangByIdTaiKhoan(customer._id);
        store.setCart(cartOld);
    }
};
</script>

<style scoped>
.nameItem {
    display: -webkit-box;
    font-size: 0.8rem;
    max-height: 3.2rem;
    -webkit-box-orient: vertical;
    overflow: hidden;
    -webkit-line-clamp: 2;
    line-height: 1.7rem;
}

.nameItem:hover {
    color: var(--color-primary-two) !important;
}

.info_item_cart {
    display: flex;
    gap: 5px;
}

.img-thumbnail {
    width: 60px;
    height: 60px;
}

.price_cart {
    font-size: 0.8rem;
}

.fa-minus,
.fa-plus,
.input_amount {
    height: 30px;
    width: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #333;
    border-radius: 5px;
    transition: all 0.3s ease-in-out;
    padding: 0 5px;
}

.input_amount {
    font-size: 0.8rem;
}

.fa-minus:hover,
.fa-plus:hover {
    color: #fff;
    background-color: #333;
    cursor: pointer;
}

.checkbox_btn {
    cursor: pointer;
}

.del_btn {
    font-size: 0.9rem;
    margin: 0;
}

p {
    margin: 0;
}

.del_btn:hover {
    cursor: pointer;
    color: var(--color-primary-two) !important;
}

.list_btn_amount {
    gap: 2px;
}

.pay {
    display: flex;
    justify-content: end;
    padding: 10px;
    position: sticky;
    bottom: 0;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}

.pay .price-total-cart {
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 3px;
}

.totalPriceCart {
    color: var(--color-primary-two);
}
.pay a {
    text-decoration: none;
    background-color: var(--color-primary-two);
    padding: 5px 10px;
    text-transform: uppercase;
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    cursor: pointer;
}

.pay a:hover {
    opacity: 0.8;
}
</style>
