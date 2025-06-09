<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink
                :to="`/category/${productDetail?.categoryproduct?.category_name}`"
                >{{ productDetail?.categoryproduct?.category_name }}</NuxtLink
            >
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink :to="`/detail/${productDetail?._id}`">{{
                productDetail?.item_name
            }}</NuxtLink>
        </div>
    </div>
    <div class="container product-detail-container">
        <div class="row product-detail-content">
            <div class="col-lg-5 col-md-6 col-12 product-image-section">
                <img
                    :src="apiImage + productDetail?.image"
                    alt="ảnh sản phẩm"
                    class="img-fluid rounded"
                />
            </div>

            <div class="col-lg-4 col-md-6 col-12 product-info-section">
                <h2 class="product-title">{{ productDetail?.item_name }}</h2>
                <div class="product-pricing">
                    <span class="old-price" v-if="productDetail?.price"
                        >{{ productDetail?.price.toLocaleString("de-DE")
                        }}<sup>đ</sup></span
                    >
                    <span class="sale-price"
                        >{{
                            productDetail?.price_reduction?.toLocaleString(
                                "de-DE"
                            )
                        }}<sup>đ</sup></span
                    >
                    <span class="vat-note">(Đã bao gồm VAT)</span>
                </div>
                <p class="product-status">
                    Tình trạng:
                    <span
                        :class="{
                            'text-danger':
                                Number(productDetail?.quantity_available) <= 0,
                            'text-success':
                                Number(productDetail?.quantity_available) > 0,
                        }"
                    >
                        {{
                            Number(productDetail?.quantity_available) > 0
                                ? "Còn hàng"
                                : "Hết hàng"
                        }}
                    </span>
                </p>
                <p class="product-views">
                    Lượt xem: {{ productDetail?.view?.toLocaleString("de-DE") }}
                </p>
                <p class="product-sold" v-if="productDetail?.sales">
                    Đã bán: {{ productDetail.sales.toLocaleString("de-DE") }}
                </p>
                <p class="product-origin">
                    Xuất xứ: {{ productDetail?.origin }}
                </p>

                <div class="product-quantity">
                    <label>Số lượng:</label>
                    <div class="quantity-control d-flex align-items-center">
                        <span
                            class="btn btn-light"
                            @click="amountProduct > 1 && amountProduct--"
                            >-</span
                        >
                        <input
                            type="text"
                            class="form-control text-center mx-2"
                            v-model="amountProduct"
                            @input="validateAmount"
                            style="width: 60px"
                        />
                        <span class="btn btn-light" @click="amountProduct++"
                            >+</span
                        >
                    </div>
                </div>

                <div class="product-buttons mt-3">
                    <button class="btn btn-danger w-100 mb-2" @click="addCart">
                        THÊM VÀO GIỎ HÀNG
                    </button>
                    <button class="btn btn-warning w-100" @click="buyNow">
                        MUA NGAY
                    </button>
                </div>

                <div class="hotline mt-3">
                    <i class="fa-solid fa-phone-volume me-1"></i>
                    Hotline: <a href="tel:0123456789">012.3456.789</a>
                </div>
            </div>

            <div class="col-lg-3 col-12 mt-4 mt-lg-0 policy-section">
                <h5 class="fw-bold">CAM KẾT VỚI KHÁCH HÀNG</h5>
                <ul class="list-unstyled mt-3">
                    <li>
                        <i class="fa-solid fa-shield-halved me-2"></i> Hàng
                        chính hãng 100%
                    </li>
                    <li>
                        <i class="fa-solid fa-thumbs-up me-2"></i> Uy tín chất
                        lượng
                    </li>
                    <li>
                        <i class="fa-solid fa-gears me-2"></i> Hỗ trợ sau bán
                        hàng
                    </li>
                    <li>
                        <i class="fa-solid fa-rotate me-2"></i> Đổi trả rõ ràng
                    </li>
                </ul>
            </div>
        </div>

        <div
            class="product-description mt-5"
            v-html="productDetail?.description_detail"
        ></div>

        <div class="recommend-section mt-5">
            <h3 class="text-center mb-4">Sản phẩm cùng loại</h3>
            <div class="row">
                <div
                    class="col-lg-2 col-md-4 col-sm-6 col-6"
                    v-for="product in productRecomend"
                    :key="product._id"
                >
                    <item-product-recomend :product="product" :isSale="true" />
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useRoute, useRouter } from "vue-router";
import Cookies from "js-cookie";
import { ref, onMounted } from "vue";
import { type Products } from "~/constant/api";
import { getProductById, getProductRecomend } from "~/services/detail.service";
import { apiImage } from "~/constant/request";
import {
    createCart,
    getGioHangByIdTaiKhoan,
    updateCart,
    updateCartsFalse,
} from "~/services/cart.service";
import { useCartStore } from "~/store";
import { checkQuantityItems } from "~/services/home.service";
import axios from "axios";
import Swal from "sweetalert2";
import { useHead } from "@unhead/vue";

const route = useRoute();
const router = useRouter();
const store = useCartStore();
const id = route.params.id;

const productDetail = ref<Products | null>(null);
const productRecomend = ref<Products[]>([]);
const amountProduct = ref(1);

const fetchProductDetail = async () => {
    try {
        const res = await getProductById(String(id));
        productDetail.value = res;

        useHead({
            title: `${
                productDetail?.value ? productDetail?.value?.item_name : ""
            }`,
        });
    } catch (error) {
        console.error("Error while fetching product detail:", error);
    }
};

const fetchProductRecomend = async () => {
    try {
        const res = await getProductRecomend({
            page: 1,
            pageSize: 6,
            category_name: String(
                productDetail.value?.categoryproduct?.category_name
            ),
        });
        productRecomend.value = res?.data ?? [];
    } catch (error) {
        console.error("Error while fetching recommended products:", error);
    }
};

onMounted(async () => {
    await fetchProductDetail();
    if (productDetail.value) {
        await fetchProductRecomend();
    }
});

const validateAmount = (event: Event): void => {
    const target = event.target as HTMLInputElement;
    let value = target.value;
    value = value.replace(/\D/g, "");
    if (value === "") {
        value = "1";
    }
    amountProduct.value = Number(value);
};

const addCart = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            const cart = await getGioHangByIdTaiKhoan(customer._id);

            try {
                const checkQuantity = await checkQuantityItems({
                    ids: [String(id)],
                    quantities: [Number(amountProduct.value)],
                });

                if (checkQuantity) {
                    const isEmptyProduct = cart.find(
                        (value) => String(value.item_id) === String(id)
                    );

                    if (isEmptyProduct) {
                        await updateCart({
                            _id: String(isEmptyProduct._id),
                            item_id: String(isEmptyProduct.item_id),
                            user_id: "",
                            quantity:
                                amountProduct.value +
                                Number(isEmptyProduct.quantity),
                            status: isEmptyProduct.status,
                        });

                        Swal.fire(
                            "Thông báo",
                            "Sản phẩm tồn tại, đã tăng số lượng trong giỏ hàng!",
                            "warning"
                        );
                    } else {
                        await createCart({
                            item_id: String(id),
                            user_id: customer._id,
                            quantity: amountProduct.value,
                            status: false,
                        });

                        Swal.fire(
                            "Thành công",
                            "Sản phẩm đã được thêm vào giỏ hàng!",
                            "success"
                        );
                        const cartOld = await getGioHangByIdTaiKhoan(
                            customer._id
                        );
                        store.setCart(cartOld);
                    }
                }
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    Swal.fire(
                        "Lỗi",
                        `${error.response?.data?.detail?.insufficient_items.item_name} không đủ số lượng, trong kho chỉ còn ${error.response?.data?.detail?.insufficient_items?.quantity_available} sản phẩm`,
                        "error"
                    );
                }
            }
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
        }
    } else {
        router.push("/login");
    }
};

const buyNow = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);

            try {
                const checkQuantity = await checkQuantityItems({
                    ids: [String(id)],
                    quantities: [Number(amountProduct.value)],
                });

                if (checkQuantity) {
                    await updateCartsFalse(customer._id);

                    const cart = await getGioHangByIdTaiKhoan(customer._id);

                    const isEmptyProduct = cart.find(
                        (value) => String(value.item_id) === String(id)
                    );

                    if (isEmptyProduct) {
                        await updateCart({
                            _id: String(isEmptyProduct._id),
                            item_id: String(isEmptyProduct.item_id),
                            user_id: "",
                            quantity: amountProduct.value,
                            status: true,
                        });
                    } else {
                        await createCart({
                            item_id: String(id),
                            user_id: customer._id,
                            quantity: amountProduct.value,
                            status: true,
                        });
                        const cartOld = await getGioHangByIdTaiKhoan(
                            customer._id
                        );
                        store.setCart(cartOld);
                    }

                    router.push("/order");
                }
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    Swal.fire(
                        "Lỗi",
                        `${error.response?.data?.detail?.insufficient_items.item_name} không đủ số lượng, trong kho chỉ còn ${error.response?.data?.detail?.insufficient_items?.quantity_available} sản phẩm`,
                        "error"
                    );
                }
            }
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
        }
    } else {
        router.push("/login");
    }
};
</script>

<style scoped lang="css">
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

.product-title {
    font-size: 24px;
    font-weight: bold;
    color: #6d4137;
}

.product-pricing .old-price {
    text-decoration: line-through;
    color: gray;
    font-size: 18px;
    margin-right: 10px;
}

.product-pricing .sale-price {
    color: var(--color-sale);
    font-size: 22px;
    font-weight: bold;
}

.product-pricing .vat-note {
    font-size: 13px;
    display: block;
    color: #888;
}

.product-quantity label {
    font-weight: 600;
    margin-bottom: 5px;
}

.policy-section ul li {
    margin-bottom: 10px;
    color: #333;
}

.hotline {
    font-weight: 600;
    color: #d33;
}

.product-detail-container {
    padding-top: 20px;
}
</style>
