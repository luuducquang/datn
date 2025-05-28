<template>
    <div class="container">
        <div class="type">
            <NuxtLink to="/">TRANG CHỦ</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/cart">Giỏ Hàng</NuxtLink>
            <i class="fa-solid fa-arrow-right"></i>
            <NuxtLink to="/order">Đặt Hàng</NuxtLink>
        </div>

        <item-cart
            :dataCart="dataCart"
            :fetch="fetchDataCart"
            :totalPrice="totalPrice"
            :order="true"
        />

        <div class="row">
            <div class="col-lg-4">
                <div class="total-order bg-white p-3 shadow-sm rounded">
                    <form action="#">
                        <table class="table">
                            <tbody>
                                <tr>
                                    <td>Phí tạm tính:</td>
                                    <td>
                                        <span class="totalPriceCart">{{
                                            totalPrice.toLocaleString("DE-de")
                                        }}</span>
                                        <sup>đ</sup>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Phụ phí:</td>
                                    <td>
                                        <span>0</span>
                                        <sup>đ</sup>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Phí vận chuyển:</td>
                                    <td>
                                        <span class="transport_order"
                                            >30.000</span
                                        >
                                        <sup>đ</sup>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Giảm giá:</td>
                                    <td>
                                        <span
                                            >-{{
                                                (
                                                    (totalPrice *
                                                        Number(
                                                            getMembershipRank(
                                                                dataCustomer?.loyalty_points
                                                            ).voucher
                                                        )) /
                                                    100
                                                ).toLocaleString("DE-de")
                                            }}</span
                                        >
                                        <sup>đ</sup>
                                        <span
                                            >({{
                                                Number(
                                                    getMembershipRank(
                                                        dataCustomer?.loyalty_points
                                                    ).voucher
                                                )
                                            }}% hạng thành viên)</span
                                        >
                                    </td>
                                </tr>
                                <tr v-if="discountAmount">
                                    <td></td>
                                    <td>
                                        <span
                                            >-{{
                                                (
                                                    (totalPrice *
                                                        Number(
                                                            discountAmount
                                                        )) /
                                                    100
                                                ).toLocaleString("DE-de")
                                            }}</span
                                        >
                                        <sup>đ</sup>
                                        <span
                                            >({{ Number(discountAmount) }}%
                                            voucher)</span
                                        >
                                    </td>
                                </tr>
                                <tr>
                                    <td class="border-top">Tổng thanh toán:</td>
                                    <td class="total_order border-top">
                                        <span
                                            class="total_all"
                                            style="
                                                font-family: Arial, Helvetica,
                                                    sans-serif;
                                                font-size: 20px;
                                            "
                                        >
                                            {{
                                                totalPricePaid.toLocaleString(
                                                    "DE-de"
                                                )
                                            }}
                                        </span>
                                        <sup>đ</sup>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </form>
                </div>
            </div>
            <div class="col-lg-8">
                <div class="container">
                    <form @submit.prevent="handleSubmit">
                        <div class="row mb-3 g-2">
                            <p class="form-label">Mã giảm giá</p>
                            <div class="col-md-4">
                                <input
                                    v-model="voucherCode"
                                    type="text"
                                    class="form-control"
                                    placeholder="Nhập mã giảm giá"
                                    @input="handleVoucherChange"
                                />
                            </div>
                            <div class="col-md-4">
                                <select
                                    v-model="voucherCode"
                                    class="form-select"
                                    @change="handleVoucherChange"
                                >
                                    <option value="" disabled>
                                        -- Chọn mã giảm giá --
                                    </option>
                                    <option
                                        v-for="voucher in dataVoucher"
                                        :key="voucher._id"
                                        :value="voucher.code"
                                    >
                                        Giảm
                                        {{ voucher.discount_value }}% -
                                        {{
                                            Number(voucher.quantity) > 0 &&
                                            voucher.status
                                                ? "Đang hoạt động"
                                                : "Đã hết hạn"
                                        }}
                                    </option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <button
                                    type="button"
                                    class="btn btn-primary w-80"
                                    @click="applyVoucher"
                                >
                                    Áp dụng
                                </button>
                            </div>
                            <p class="mb-0">
                                Lưu ý: bạn phải nhấn "Áp dụng" thì voucher mới
                                có hiệu lực
                            </p>
                        </div>
                        <div class="mb-3">
                            <label for="hoTen" class="form-label">Họ tên</label>
                            <input
                                type="text"
                                class="form-control"
                                id="hoTen"
                                v-model="formData.hoTen"
                                :class="{ 'is-invalid': formErrors.hoTen }"
                                required
                            />
                            <div
                                v-if="formErrors.hoTen"
                                class="invalid-feedback"
                            >
                                Vui lòng nhập họ tên!
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="soDienThoai" class="form-label"
                                >Điện thoại</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="soDienThoai"
                                v-model="formData.soDienThoai"
                                :class="{
                                    'is-invalid': formErrors.soDienThoai,
                                }"
                                maxlength="11"
                                required
                            />
                            <div
                                v-if="formErrors.soDienThoai"
                                class="invalid-feedback"
                            >
                                {{ formErrors.soDienThoai }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input
                                type="email"
                                class="form-control"
                                id="email"
                                v-model="formData.email"
                                :class="{ 'is-invalid': formErrors.email }"
                                required
                            />
                            <div
                                v-if="formErrors.email"
                                class="invalid-feedback"
                            >
                                {{ formErrors.email }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="province" class="form-label"
                                >Tỉnh/TP</label
                            >
                            <select
                                class="form-select"
                                id="province"
                                v-model="formData.province"
                                @change="handlerClickCountry"
                                required
                            >
                                <option value="" disabled>Vui lòng chọn</option>
                                <option
                                    v-for="(value, index) in country"
                                    :key="index"
                                    :value="value.code"
                                >
                                    {{ value.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="district" class="form-label"
                                >Quận/Huyện</label
                            >
                            <select
                                class="form-select"
                                id="district"
                                v-model="formData.district"
                                @change="handlerClickDistrict"
                                required
                                :disabled="district.length === 0"
                            >
                                <option value="" disabled>Vui lòng chọn</option>
                                <option
                                    v-for="(value, index) in district"
                                    :key="index"
                                    :value="value.code"
                                >
                                    {{ value.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="ward" class="form-label"
                                >Phường/Xã</label
                            >
                            <select
                                class="form-select"
                                id="ward"
                                v-model="formData.ward"
                                required
                                :disabled="ward.length === 0"
                            >
                                <option value="" disabled>Vui lòng chọn</option>
                                <option
                                    v-for="(value, index) in ward"
                                    :key="index"
                                    :value="value.code"
                                >
                                    {{ value.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="diaChi" class="form-label"
                                >Địa chỉ</label
                            >
                            <input
                                type="text"
                                class="form-control"
                                id="diaChi"
                                v-model="formData.diaChi"
                                :class="{ 'is-invalid': formErrors.diaChi }"
                                required
                            />
                            <div
                                v-if="formErrors.diaChi"
                                class="invalid-feedback"
                            >
                                Vui lòng nhập địa chỉ!
                            </div>
                        </div>
                        <!-- <div class="d-flex justify-content-center">
                            <button
                                type="submit"
                                class="btn btn-primary btn-order"
                            >
                                Đặt hàng
                            </button>
                            <div>
                                <PayPalButton
                                    :amount="totalPrice + 30000"
                                    :onSuccess="handleSuccess"
                                />
                            </div>
                        </div> -->
                        <div class="mb-3">
                            <label class="form-label"
                                >Chọn phương thức thanh toán:</label
                            >
                            <div class="form-check">
                                <input
                                    class="form-check-input"
                                    type="radio"
                                    value="cod"
                                    v-model="paymentMethod"
                                    @click="ChangeMethod"
                                />
                                <label class="form-check-label" for="cod">
                                    Thanh toán khi nhận hàng
                                </label>
                            </div>
                            <div class="form-check">
                                <input
                                    class="form-check-input"
                                    type="radio"
                                    value="wallet"
                                    v-model="paymentMethod"
                                    @click="ChangeMethod"
                                />
                                <label class="form-check-label" for="wallet">
                                    Thanh toán bằng ví (Số dư:
                                    {{ ConvertPrice(dataCustomer?.wallet) }})
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
                            <div
                                v-if="
                                    paymentMethod === 'paypal' &&
                                    formData.hoTen != '' &&
                                    formData.soDienThoai != '' &&
                                    formData.email != '' &&
                                    formData.diaChi != '' &&
                                    formData.province != '' &&
                                    formData.district != '' &&
                                    formData.ward != '' &&
                                    isPaypal
                                "
                                class="mt-3 mb-3 d-flex justify-content-center"
                            >
                                <PayPalButton
                                    :amount="Number(totalPricePaid)"
                                    :onSuccess="handleSuccess"
                                />
                            </div>
                            <div
                                v-if="!isPaypal"
                                class="d-flex justify-content-center"
                            >
                                <button
                                    type="submit"
                                    class="btn btn-primary btn-order me-2"
                                    :disabled="!paymentMethod"
                                >
                                    Đặt hàng
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import axios from "axios";
import Cookies from "js-cookie";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";
import { type Discounts, type Cart } from "~/constant/api";
import {
    getCountry,
    getDistrict,
    getWard,
} from "~/services/apicountry.service";
import {
    deleteManyCarts,
    getGioHangByIdTaiKhoan,
} from "~/services/cart.service";
import {
    getAllDiscount,
    getDiscountByCode,
    getDiscountUseCode,
} from "~/services/discount.service";
import {
    checkAndUpdateQuantityItems,
    checkQuantityItems,
} from "~/services/home.service";
import {
    getInformation,
    updateInformation,
    updateInformationWalletPoint,
} from "~/services/information.service";
import { login } from "~/services/login.service";
import { sendOrder } from "~/services/order.service";
import { getMembershipRank } from "~/store/getMemberShip";
import { useHead } from "@unhead/vue";
import ConvertPrice from "~/store/convertprice";

useHead({
    title: "Đặt hàng",
});

const router = useRouter();

const dataCart = ref<Cart[]>([]);
const totalPrice = ref(0);

const isPaypal = ref(false);
const paymentMethod = ref("cod");

const dataCustomer = ref();

const dataVoucher = ref<Discounts[]>([]);
const voucherCode = ref("");
const discountAmount = ref<number | null>(null);
const voucherError = ref("");

const formData = ref<Record<string, string>>({
    hoTen: "",
    soDienThoai: "",
    email: "",
    province: "",
    district: "",
    ward: "",
    diaChi: "",
});

const formErrors = ref<{
    hoTen: boolean | string;
    soDienThoai: boolean | string;
    email: boolean | string;
    province: boolean | string;
    district: boolean | string;
    ward: boolean | string;
    diaChi: boolean | string;
}>({
    hoTen: false,
    soDienThoai: false,
    email: false,
    province: false,
    district: false,
    ward: false,
    diaChi: false,
});

const country = ref<Record<string, string>[]>([]);

const district = ref<Record<string, string>[]>([]);

const ward = ref<Record<string, string>[]>([]);

const handlerClickCountry = async (event: Event) => {
    const target = event.target as HTMLSelectElement;
    const selectedProvinceId = target.value;
    await getDistrict(Number(selectedProvinceId))
        .then((districtData) => {
            district.value = districtData?.districts;
            return districtData;
        })
        .catch((error) => {
            console.error("Error fetching country data:", error);
            return "";
        });
};

const handlerClickDistrict = async (event: Event) => {
    const target = event.target as HTMLSelectElement;
    const selectedDistrictId = target.value;
    await getWard(Number(selectedDistrictId))
        .then((wardData) => {
            ward.value = wardData?.wards;
            return wardData;
        })
        .catch((error) => {
            console.error("Error fetching country data:", error);
            return "";
        });
};

const totalPricePaid = computed(() => {
    const membershipVoucher =
        Number(
            getMembershipRank(dataCustomer.value?.loyalty_points)?.voucher
        ) || 0;
    const discount = Number(discountAmount.value) || 0;
    const totalDiscountPercent = membershipVoucher + discount;
    const discountedPrice = totalPrice.value * (1 - totalDiscountPercent / 100);
    const shippingFee = 30000;

    return discountedPrice + shippingFee;
});

const getDefaultDateTime = () => {
    const now = new Date();
    const vietnamTime = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    return vietnamTime.toISOString().slice(0, 16);
};

const handleVoucherChange = () => {
    discountAmount.value = null;
};

async function applyVoucher() {
    voucherError.value = "";
    discountAmount.value = null;

    if (!voucherCode.value) {
        voucherError.value = "Vui lòng nhập mã giảm giá.";
        return;
    }

    try {
        const valueDiscount = await getDiscountByCode(voucherCode.value);
        discountAmount.value = valueDiscount;
    } catch (error) {
        voucherError.value = "Mã giảm giá không tồn tại hoặc đã hết hiệu lực.";
    }
}

const ChangeMethod = () => {
    isPaypal.value = false;
};

const handleSuccess = async (result: any) => {
    console.log("Thanh toán thành công:", result);

    const listitems = dataCart.value.reduce(
        (acc: { ids: string[]; quantities: number[] }, value: Cart) => {
            acc.ids.push(value.item_id);
            acc.quantities.push(value.quantity);
            return acc;
        },
        { ids: [], quantities: [] }
    );

    const listIdDel: Array<string> = dataCart.value.map((item) =>
        String(item._id)
    );

    const countryName = country.value.find(
        (item) => item.code === formData.value.province
    );
    const districtName = district.value.find(
        (item) => item.code === formData.value.district
    );
    const wardName = ward.value.find(
        (item) => item.code === formData.value.ward
    );

    const listJsonBuy = dataCart.value.map(function (value: Cart) {
        return {
            item_id: value.item_id,
            quantity: value.quantity,
            unit_price: value.product?.price_reduction || 0,
            total_price:
                (Number(value.product?.price_reduction) || 0) *
                Number(value.quantity),
        };
    });

    const customer = JSON.parse(customerData ?? "{}");

    if (countryName && districtName && wardName) {
        await checkAndUpdateQuantityItems(listitems);
        await sendOrder({
            status: "Đang xử lý",
            sell_date: getDefaultDateTime(),
            total_price:
                Number(totalPrice.value) *
                    (1 -
                        (getMembershipRank(dataCustomer.value?.loyalty_points)
                            .voucher +
                            Number(discountAmount.value)) /
                            100) +
                30000,
            name: formData.value.hoTen,
            address: `${countryName.name}-${districtName.name}-${wardName.name}`,
            email: formData.value.email,
            phone: formData.value.soDienThoai,
            address_detail: formData.value.diaChi,
            user_id: customer._id,
            sell_items: listJsonBuy,
            is_paid: true,
        });
        await deleteManyCarts(listIdDel);
        Swal.fire("Thành công", "Đặt hàng thành công!", "success");

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
            loyalty_points:
                dataUser.loyalty_points +
                (Number(totalPrice.value) *
                    (1 -
                        getMembershipRank(dataCustomer.value?.loyalty_points)
                            .voucher /
                            100) +
                    30000) *
                    0.2,
            wallet: Number(dataUser.wallet),
            role_name: customer.role_name,
        });

        const res = await login({
            email: String(dataUser.email),
            password: String(customer.password),
        });
        Cookies.set("customer", JSON.stringify(res), { expires: 1 });

        setTimeout(() => {
            router.replace("/");
        }, 1500);
    }
};

const handleSubmit = async () => {
    formErrors.value = {
        hoTen: !formData.value.hoTen,
        soDienThoai: !formData.value.soDienThoai.match(/^[0-9]+$/)
            ? "Số điện thoại không hợp lệ!"
            : !formData.value.soDienThoai,
        email: !formData.value.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
            ? "Email không hợp lệ!"
            : !formData.value.email,
        province: !formData.value.province,
        district: !formData.value.district,
        ward: !formData.value.ward,
        diaChi: !formData.value.diaChi,
    };

    if (Object.values(formErrors.value).every((field) => field === false)) {
        const countryName = country.value.find(
            (item) => item.code === formData.value.province
        );
        const districtName = district.value.find(
            (item) => item.code === formData.value.district
        );
        const wardName = ward.value.find(
            (item) => item.code === formData.value.ward
        );
        const listIdDel: Array<string> = dataCart.value.map((item) =>
            String(item._id)
        );
        const customer = JSON.parse(customerData ?? "{}");

        const listJsonBuy = dataCart.value.map(function (value: Cart) {
            return {
                item_id: value.item_id,
                quantity: value.quantity,
                unit_price: value.product?.price_reduction || 0,
                total_price:
                    (Number(value.product?.price_reduction) || 0) *
                    Number(value.quantity),
            };
        });

        if (countryName && districtName && wardName) {
            try {
                if (dataCart.value) {
                    const listitems = dataCart.value.reduce(
                        (
                            acc: { ids: string[]; quantities: number[] },
                            value: Cart
                        ) => {
                            acc.ids.push(value.item_id);
                            acc.quantities.push(value.quantity);
                            return acc;
                        },
                        { ids: [], quantities: [] }
                    );

                    const checkQuantity = await checkQuantityItems(listitems);

                    if (checkQuantity) {
                        try {
                            if (Number(discountAmount.value) > 0) {
                                await getDiscountUseCode(voucherCode.value);
                            }
                            if (paymentMethod.value === "cod") {
                                await checkAndUpdateQuantityItems(listitems);
                                await sendOrder({
                                    status: "Đang xử lý",
                                    sell_date: getDefaultDateTime(),
                                    total_price:
                                        Number(totalPrice.value) *
                                            (1 -
                                                (getMembershipRank(
                                                    dataCustomer.value
                                                        ?.loyalty_points
                                                ).voucher +
                                                    Number(
                                                        discountAmount.value
                                                    )) /
                                                    100) +
                                        30000,
                                    name: formData.value.hoTen,
                                    address: `${countryName.name}-${districtName.name}-${wardName.name}`,
                                    email: formData.value.email,
                                    phone: formData.value.soDienThoai,
                                    address_detail: formData.value.diaChi,
                                    user_id: customer._id,
                                    sell_items: listJsonBuy,
                                    is_paid: false,
                                });
                                await deleteManyCarts(listIdDel);

                                Swal.fire(
                                    "Thành công",
                                    "Đặt hàng thành công!",
                                    "success"
                                );

                                setTimeout(() => {
                                    router.replace("/");
                                }, 1500);
                            } else if (paymentMethod.value === "paypal") {
                                isPaypal.value = true;

                                Swal.fire(
                                    "Thông báo",
                                    "Vui lòng thanh toán qua PayPal, sau khi thanh toán đơn hàng sẽ được xử lý.",
                                    "info"
                                );
                            } else if (paymentMethod.value === "wallet") {
                                const dataUser = await getInformation(
                                    dataCustomer?.value?._id
                                );

                                const customer = JSON.parse(
                                    customerData ?? "{}"
                                );
                                if (
                                    dataUser.wallet >=
                                    Number(totalPrice.value) *
                                        (1 -
                                            (getMembershipRank(
                                                dataCustomer.value
                                                    ?.loyalty_points
                                            ).voucher +
                                                Number(discountAmount.value)) /
                                                100) +
                                        30000
                                ) {
                                    await checkAndUpdateQuantityItems(
                                        listitems
                                    );
                                    await sendOrder({
                                        status: "Đang xử lý",
                                        sell_date: getDefaultDateTime(),
                                        total_price:
                                            Number(totalPrice.value) *
                                                (1 -
                                                    (getMembershipRank(
                                                        dataCustomer.value
                                                            ?.loyalty_points
                                                    ).voucher +
                                                        Number(
                                                            discountAmount.value
                                                        )) /
                                                        100) +
                                            30000,
                                        name: formData.value.hoTen,
                                        address: `${countryName.name}-${districtName.name}-${wardName.name}`,
                                        email: formData.value.email,
                                        phone: formData.value.soDienThoai,
                                        address_detail: formData.value.diaChi,
                                        user_id: customer._id,
                                        sell_items: listJsonBuy,
                                        is_paid: true,
                                    });
                                    await deleteManyCarts(listIdDel);
                                    Swal.fire(
                                        "Thành công",
                                        "Đặt hàng thành công!",
                                        "success"
                                    );

                                    await updateInformationWalletPoint({
                                        _id: customer?._id,
                                        username: customer?.username,
                                        password: customer?.password,
                                        fullname: customer?.fullname,
                                        email: customer?.email,
                                        phone: customer?.phone,
                                        address: customer?.address,
                                        avatar: customer?.avatar,
                                        loyalty_points: Number(
                                            dataUser.loyalty_points +
                                                (Number(totalPrice.value) *
                                                    (1 -
                                                        getMembershipRank(
                                                            customer?.loyalty_points
                                                        ).voucher /
                                                            100) +
                                                    30000) *
                                                    0.2
                                        ),
                                        wallet: Number(
                                            Number(dataUser.wallet) -
                                                Number(totalPricePaid.value)
                                        ),
                                        role_name: customer.role_name,
                                    });

                                    const res = await login({
                                        email: String(dataUser.email),
                                        password: String(customer.password),
                                    });
                                    Cookies.set(
                                        "customer",
                                        JSON.stringify(res),
                                        { expires: 1 }
                                    );

                                    setTimeout(() => {
                                        router.replace("/");
                                    }, 1500);
                                } else {
                                    Swal.fire(
                                        "Thông báo",
                                        "Số dư của bạn không đủ, không thể thanh toán.",
                                        "info"
                                    );
                                }
                            }
                        } catch (error) {
                            if (axios.isAxiosError(error)) {
                                Swal.fire(
                                    "Lỗi",
                                    error.response?.data.detail,
                                    "error"
                                );
                                voucherCode.value = "";
                                discountAmount.value = null;
                            }
                        }
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
        } else {
            console.error("Error api country");
            console.log(countryName, districtName, wardName);
        }
    } else {
        console.log("Form is invalid!", formErrors.value);
    }
};

const customerData = Cookies.get("customer");
const fetchDataCart = async () => {
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            dataCustomer.value = customer;
            const dataTemp = await getGioHangByIdTaiKhoan(customer._id);
            const dataBuy = dataTemp.filter((value) => value.status === true);
            dataCart.value = dataBuy;
            const totalPriceBuy = dataBuy.reduce((total, item) => {
                return (
                    total +
                    Number(item?.product?.price_reduction) * item?.quantity
                );
            }, 0);
            totalPrice.value = totalPriceBuy;

            await getCountry()
                .then((countryData) => {
                    country.value = countryData;
                    return countryData;
                })
                .catch((error) => {
                    console.error("Error fetching country data:", error);
                    return "";
                });

            const listVoucher = await getAllDiscount();
            dataVoucher.value = listVoucher;
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

.form-control,
.form-select {
    font-size: 0.9rem;
}

.btn-order {
    background-color: var(--color-primary);
    border: none;
    margin-bottom: 20px;
}
</style>
