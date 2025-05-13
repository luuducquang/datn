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
    <div class="container">
        <div class="row gy-3">
            <div class="col-lg-5 col-md-6 col-sm-6">
                <span class="product-item-img"
                    ><img
                        :src="apiImage + productDetail?.image"
                        alt="anh san pham"
                /></span>
                <div class="miror"></div>
                <!-- <div class="but">
                    <span>
                        <i class="fa-solid fa-angle-left"></i>
                    </span>
                    <span>
                        <i class="fa-solid fa-angle-right"></i>
                    </span>
                </div> -->
                <div class="img-slider">
                    <!-- <img class="activeImg opacity1" src="./assets/img/Cleanser/cerave/3.jpg" alt=""> -->
                    <!-- <img ng-repeat="x in listImgDetail" src={{x.linkAnh}} alt=""> -->
                    <!-- <img src="./assets/img/Cleanser/cerave/2.jpg" alt="">
                    <img src="./assets/img/Cleanser/cerave/1.webp" alt="">
                    <img src="./assets/img/Cleanser/cerave/5.webp" alt=""> -->
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-6">
                <table>
                    <tr>
                        <td>
                            <div class="product-item-name">
                                {{ productDetail?.item_name }}
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <div class="product-item_price">
                                <span class="product-item_price_old">{{
                                    Number(productDetail?.price) > 0
                                        ? productDetail?.price.toLocaleString(
                                              "de-DE"
                                          )
                                        : ""
                                }}</span
                                ><sup>đ</sup>
                                <span class="product-item_price_current">{{
                                    Number(productDetail?.price_reduction) > 0
                                        ? productDetail?.price_reduction.toLocaleString(
                                              "de-DE"
                                          )
                                        : ""
                                }}</span
                                ><sup>đ</sup>
                                <span class="VAT">(Đã bao gồm VAT)</span>
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <div class="status">
                                Tình trạng :
                                <span
                                    :style="{
                                        color:
                                            Number(
                                                productDetail?.quantity_available
                                            ) < 5
                                                ? '#FF3300'
                                                : '#33CC00',
                                    }"
                                    >{{
                                        Number(
                                            productDetail?.quantity_available
                                        ) > 0
                                            ? Number(
                                                  productDetail?.quantity_available
                                              ) < 5
                                                ? "Hết hàng"
                                                : "Còn hàng"
                                            : "Hết hàng"
                                    }}</span
                                >
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            Lượt xem :
                            {{
                                Number(productDetail?.view) > 0
                                    ? Number(
                                          productDetail?.view
                                      ).toLocaleString("de-DE")
                                    : ""
                            }}
                        </td>
                    </tr>

                    <!-- <tr>
                        <td>
                            Đã bán :
                            {{
                                productDetail?.luotBan > 0
                                    ? productDetail?.luotBan.toLocaleString(
                                          "de-DE"
                                      )
                                    : ""
                            }}
                        </td>
                    </tr> -->

                    <tr>
                        <td>
                            <span class="origin">Xuất xứ : </span>
                            <span class="country-origin">{{
                                productDetail?.origin
                            }}</span>
                        </td>
                    </tr>

                    <!-- <tr>
                        <td>
                            <div class="product-item-capacity">
                                <span class="capacity-name">Dung tích : </span>
                                <span class="size">{{
                                    productDetail?.trongLuong
                                }}</span>
                                <div class="capacity-volume">
                                    <input type="radio" id="1" name="capacity" class="size-mini">235ml</input>
                                    <input type="radio" id="1" name="capacity" class="size-big">473ml</input>
                                </div>
                            </div>
                        </td>
                    </tr> -->

                    <tr>
                        <td>
                            <div class="product-amount-item">Số lượng :</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="buy-amount-product d-flex">
                                <span
                                    class="fa-solid fa-minus minus_btn"
                                    @click="
                                        () => {
                                            if (amountProduct > 1) {
                                                amountProduct--;
                                            }
                                        }
                                    "
                                ></span>
                                <input
                                    type="text"
                                    min="1"
                                    class="amount"
                                    v-model="amountProduct"
                                    @input="validateAmount"
                                />
                                <span
                                    @click="amountProduct++"
                                    class="fa-solid fa-plus plus_btn"
                                ></span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <button class="add-item" @click="addCart">
                                THÊM VÀO GIỎ HÀNG
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <button @click="buyNow" class="buy-now">
                                MUA NGAY
                            </button>
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <div class="call">
                                <div class="fa-solid fa-phone-volume"></div>
                                <span class="Hotline"
                                    >Hotline :
                                    <a
                                        href="tel:012.3456.789"
                                        title="tel:012.3456.789"
                                    >
                                        <span>012.3456.789</span>
                                    </a>
                                </span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="about_policy col-lg-3">
                <table>
                    <tr>
                        <th>CAM KẾT VỚI KHÁCH HÀNG</th>
                    </tr>
                    <tr>
                        <td>
                            <i class="font15 fa-solid fa-shield-halved"></i>Hàng
                            chính hãng 100%
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <i class="font15 fa-solid fa-thumbs-up"></i>Uy tín
                            chất lượng
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <i class="font15 fa-solid fa-gears"></i>Hỗ trợ liên
                            tục trong quá trình sử dụng sản phẩm
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <i class="font15 fa-sharp fa-solid fa-rotate"></i
                            >Chính sách đổi trả rõ ràng
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="bind_html" v-html="productDetail?.description_detail"></div>
        <div class="recomend">
            <h1>Sản phẩm cùng loại</h1>
            <div class="list_item_recomend">
                <div class="row justify-content-center">
                    <div
                        class="col-lg-2 col-md-4 col-sm-6 col-6"
                        v-for="product in productRecomend"
                        :key="product._id"
                    >
                        <item-product-recomend
                            :product="product"
                            :isSale="true"
                        />
                    </div>
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

.product-item-img {
    overflow: hidden;
}

.product-item-img img {
    width: 100%;
    object-fit: cover;
    background-size: cover;
    transition: all 0.2s linear;
    padding: 7px 0;
}

.product-item-name {
    font-size: 20px;
    font-weight: 600;
    color: #6d4137;
}

.product-item_price_old,
.product-item_price_current {
    font-size: 20px;
    color: var(--color-sale);
    font-weight: 600;
}

.product-item_price sup {
    color: var(--color-sale);
}

.product-item_price .product-item_price_old {
    text-decoration: line-through;
}

/* .capacity-name,
.product-amount-item {
    font-weight: 600;
    color: var(--font-color);
} */

.minus_btn {
    height: 30px;
    width: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    outline: none;
    background-color: #ddd;
    border: none;
    cursor: pointer;
}

.plus_btn {
    height: 30px;
    width: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    outline: none;
    background-color: #ddd;
    border: none;
    cursor: pointer;
}

.amount {
    width: 30px;
    height: 30px;
    text-align: center;
    border: none;
}

.add-item {
    width: 100%;
    min-height: 50px;
    display: block;
    background-color: transparent;
    border-radius: 10px;
    color: #fff;
    overflow: hidden;
    cursor: pointer;
    font-size: 20px;
    border: none;
    margin: 5px 0;
    position: relative;
    z-index: 1;
    outline: none;
}

.add-item::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: -2;
    background-color: red;
    outline: none;
    border: none;
}

.add-item::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0;
    z-index: -1;
    /* background-color:#FF9900; */
    background-color: #fff;
    color: black;
    transition: width 0.5s ease;
    outline: none;
    border: none;
}

.add-item:hover::before {
    width: 100%;
    outline: none;
    border: none;
}

.add-item:hover {
    color: red;
    border: solid 1px red;
}

.buy-now {
    width: 80%;
    min-height: 50px;
    display: block;
    background: #f78608;
    background-color: transparent;
    border-radius: 10px;
    color: white;
    overflow: hidden;
    cursor: pointer;
    font-size: 20px;
    border: none;
    margin: 5px 0;
    z-index: 1;
    position: relative;
}

.buy-now::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: #f78608;
    z-index: -2;
    transition: width 0.5s linear;
}

.buy-now::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0;
    /* background-color: #BB0000; */
    background-color: #fff;
    z-index: -1;
    transition: width 0.5s ease;
}

.buy-now:hover::before {
    width: 100%;
}
.buy-now:hover {
    color: #f78608;
    border: solid 1px #f78608;
}
.about_policy tr td i {
    font-size: 15px;
    padding-right: 10px;
    color: #009a82;
}

.bind_html {
    overflow: hidden;
    margin-top: 20px;
}

.recomend > h1 {
    font-size: 30px;
    text-align: center;
    text-transform: uppercase;
    margin: 0;
    padding-bottom: 10px;
    color: var(--color-primary);
}

.alert-success {
    position: fixed;
    right: 20px;
    top: 70px;
    z-index: 999;
    transition: all 0.3s ease-in-out;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.5s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
}
</style>
