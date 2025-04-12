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
                                        <span>0</span>
                                        <sup>đ</sup>
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
                                                (
                                                    totalPrice + 30000
                                                ).toLocaleString("DE-de")
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
                                    :value="value.province_id"
                                >
                                    {{ value.province_name }}
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
                                    :value="value.district_id"
                                >
                                    {{ value.district_name }}
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
                                    :value="value.ward_id"
                                >
                                    {{ value.ward_name }}
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
                        <div class="d-flex justify-content-center">
                            <button type="submit" class="btn btn-primary">
                                Đặt hàng
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <alert-toast :visible="alertVisible" :message="TitleToast" />
</template>

<script setup lang="ts">
import axios from "axios";
import Cookies from "js-cookie";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { type Product, type Cart } from "~/constant/api";
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
    checkAndUpdateQuantityItems,
    checkQuantityItems,
} from "~/services/home.service";
import { sendOrder } from "~/services/order.service";

const router = useRouter();

const dataCart = ref<Cart[]>([]);
const totalPrice = ref(0);

const alertVisible = ref(false);
const TitleToast = ref("");

const formData = ref<Record<string, string>>({
    hoTen: "",
    soDienThoai: "",
    email: "",
    province: "",
    district: "",
    ward: "",
    diaChi: "",
});

const formErrors = ref({
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
            district.value = districtData?.results;
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
            ward.value = wardData?.results;
            return wardData;
        })
        .catch((error) => {
            console.error("Error fetching country data:", error);
            return "";
        });
};

const getDefaultDateTime = () => {
    const now = new Date();
    const vietnamTime = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    return vietnamTime.toISOString().slice(0, 16);
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
            (item) => item.province_id === formData.value.province
        );
        const districtName = district.value.find(
            (item) => item.district_id === formData.value.district
        );
        const wardName = ward.value.find(
            (item) => item.ward_id === formData.value.ward
        );
        const listIdDel: Array<string> = dataCart.value.map((item) =>
            String(item._id)
        );
        const customer = JSON.parse(customerData);

        const listJsonBuy = dataCart.value.map(function (value: Cart) {
            return {
                item_id: value.item_id,
                quantity: value.quantity,
                unit_price: value.rentalitem?.price_reduction || 0,
                total_price:
                    (Number(value.rentalitem?.price_reduction) || 0) *
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
                        await checkAndUpdateQuantityItems(listitems);
                        await sendOrder({
                            status: "Đang xử lý",
                            sell_date: getDefaultDateTime(),
                            total_price: Number(totalPrice.value) + 30000,
                            name: formData.value.hoTen,
                            address: `${countryName.province_name}-${districtName.district_name}-${wardName.ward_name}`,
                            email: formData.value.email,
                            phone: formData.value.soDienThoai,
                            address_detail: formData.value.diaChi,
                            user_id: customer._id,
                            sell_items: listJsonBuy,
                        });
                        await deleteManyCarts(listIdDel);
                        TitleToast.value = "Đặt hàng thành công!";
                        alertVisible.value = true;

                        setTimeout(() => {
                            router.replace("/");
                        }, 1000);
                        setTimeout(() => {
                            alertVisible.value = false;
                        }, 3000);
                    }
                }
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    TitleToast.value = `${error.response?.data?.detail?.insufficient_items.item_name} không đủ số lượng, trong kho chỉ còn ${error.response?.data?.detail?.insufficient_items?.quantity_available} sản phẩm`;
                    alertVisible.value = true;
                    setTimeout(() => {
                        alertVisible.value = false;
                    }, 3000);
                }
            }
        } else {
            console.error("Error api country");
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
            const dataTemp = await getGioHangByIdTaiKhoan(customer._id);
            const dataBuy = dataTemp.filter((value) => value.status === true);
            dataCart.value = dataBuy;
            const totalPriceBuy = dataBuy.reduce((total, item) => {
                return (
                    total +
                    Number(item?.rentalitem?.price_reduction) * item?.quantity
                );
            }, 0);
            totalPrice.value = totalPriceBuy;

            await getCountry()
                .then((countryData) => {
                    country.value = countryData?.results;
                    return countryData;
                })
                .catch((error) => {
                    console.error("Error fetching country data:", error);
                    return "";
                });
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

.form-control,
.form-select {
    font-size: 0.9rem;
}
</style>
