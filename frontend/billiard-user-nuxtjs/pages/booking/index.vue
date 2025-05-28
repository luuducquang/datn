<template>
    <div class="container py-4">
        <div class="row g-3">
            <div class="col-12 col-lg-12 order-1 order-lg-1">
                <div class="row g-3">
                    <div
                        class="col-12 col-md-6 col-lg-4"
                        v-for="table in tableData"
                        :key="table._id"
                    >
                        <div
                            class="card text-center p-3 position-relative"
                            :class="table.status ? 'bg-danger' : 'bg-success'"
                        >
                            <h1 class="text-white">{{ table.table_number }}</h1>
                            <p class="m-0 text-white">
                                {{
                                    table.status ? "Đang sử dụng" : "Đang trống"
                                }}
                            </p>
                            <button
                                class="btn btn-primary btn-booking"
                                data-bs-toggle="modal"
                                data-bs-target="#exampleModal"
                                @click="
                                    openModal(String(table?._id), table?.status)
                                "
                                href="#exampleModalToggle"
                                role="button"
                            >
                                Đặt bàn
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div
        class="modal fade"
        id="exampleModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div
                class="modal-content shadow-lg border-0 rounded-4 overflow-hidden"
            >
                <div class="modal-header bg-primary text-white py-3 px-4">
                    <h5
                        class="modal-title fw-semibold mb-0"
                        id="exampleModalLabel"
                    >
                        Thông tin đặt bàn
                    </h5>
                    <button
                        type="button"
                        class="btn-close btn-close-white"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>

                <div class="modal-body p-0">
                    <div class="row g-0">
                        <div class="col-12 col-lg-8 border-end p-4">
                            <form
                                id="booking-form"
                                @submit.prevent="submitBooking"
                            >
                                <div class="row g-3 mb-3">
                                    <div class="col-md-6">
                                        <label class="form-label fw-bold"
                                            >Tên khách hàng</label
                                        >
                                        <input
                                            :disabled="idCreatedBooking != ''"
                                            type="text"
                                            class="form-control rounded-3"
                                            v-model="customerName"
                                            placeholder="Nhập tên khách hàng"
                                            required
                                        />
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-bold"
                                            >Số điện thoại</label
                                        >
                                        <input
                                            :disabled="idCreatedBooking != ''"
                                            type="tel"
                                            class="form-control rounded-3"
                                            v-model="customerPhone"
                                            placeholder="Nhập số điện thoại"
                                            required
                                        />
                                    </div>
                                </div>

                                <div v-if="isStatusTable" class="row g-3">
                                    <p class="fw-bold">
                                        Lưu ý: Bàn này có người đang chơi vui
                                        lòng chọn thời gian bắt đầu sau 4 tiếng
                                    </p>
                                </div>

                                <div class="row g-3 mb-3">
                                    <div class="col-md-6">
                                        <label class="form-label fw-bold"
                                            >Thời gian bắt đầu</label
                                        >
                                        <input
                                            :disabled="idCreatedBooking != ''"
                                            type="datetime-local"
                                            class="form-control rounded-3"
                                            v-model="startTime"
                                            required
                                        />
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label fw-bold"
                                            >Thời gian kết thúc</label
                                        >
                                        <input
                                            :disabled="idCreatedBooking != ''"
                                            type="datetime-local"
                                            class="form-control rounded-3"
                                            v-model="endTime"
                                            required
                                        />
                                    </div>
                                </div>

                                <div>
                                    <p class="form-label fw-bold mb-3">
                                        Thêm dịch vụ
                                    </p>
                                    <div
                                        class="row g-2 align-items-center mb-4"
                                    >
                                        <div class="col-md-6">
                                            <select
                                                :disabled="
                                                    idCreatedBooking != ''
                                                "
                                                class="form-select"
                                                v-model="selectedItem"
                                            >
                                                <option disabled value="">
                                                    Chọn dịch vụ
                                                </option>
                                                <option
                                                    v-for="item in optionListMenuItems"
                                                    :key="item.label"
                                                    :value="item"
                                                >
                                                    {{ item.label }} -
                                                    {{
                                                        item?.price
                                                            ? item?.price.toLocaleString()
                                                            : ""
                                                    }}đ
                                                </option>
                                            </select>
                                        </div>
                                        <div class="col-md-3">
                                            <input
                                                :disabled="
                                                    idCreatedBooking != ''
                                                "
                                                type="number"
                                                class="form-control"
                                                placeholder="Số lượng"
                                                v-model.number="
                                                    selectedQuantity
                                                "
                                                min="1"
                                            />
                                        </div>
                                        <div class="col-md-3">
                                            <button
                                                :disabled="
                                                    idCreatedBooking != ''
                                                "
                                                class="btn btn-primary w-100"
                                                type="button"
                                                @click="addService"
                                            >
                                                Thêm
                                            </button>
                                        </div>
                                    </div>

                                    <table
                                        class="table table-bordered mt-3 mb-4"
                                        v-if="addedServices.length"
                                    >
                                        <thead class="table-light">
                                            <tr>
                                                <th class="text-center">
                                                    Hình ảnh
                                                </th>
                                                <th class="text-center">
                                                    Tên dịch vụ
                                                </th>
                                                <th class="text-center">
                                                    Số lượng
                                                </th>
                                                <th class="text-center">
                                                    Đơn giá (đ)
                                                </th>
                                                <th class="text-center">
                                                    Thành tiền (đ)
                                                </th>
                                                <th class="text-center">
                                                    Hành động
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr
                                                v-for="(
                                                    item, index
                                                ) in addedServices"
                                                :key="index"
                                            >
                                                <td>
                                                    <img
                                                        :src="
                                                            item.image
                                                                ? apiImage +
                                                                  item.image
                                                                : ''
                                                        "
                                                        alt="image"
                                                        width="50"
                                                        height="50"
                                                    />
                                                </td>
                                                <td>
                                                    {{ item.name }}
                                                </td>
                                                <td class="text-center">
                                                    <div
                                                        class="d-flex justify-content-center align-items-center gap-2"
                                                    >
                                                        <button
                                                            type="button"
                                                            class="btn btn-sm btn-outline-secondary"
                                                            @click="
                                                                decreaseQuantity(
                                                                    index
                                                                )
                                                            "
                                                        >
                                                            -
                                                        </button>
                                                        <span
                                                            class="btn btn-sm"
                                                            >{{
                                                                item.quantity
                                                            }}</span
                                                        >
                                                        <button
                                                            type="button"
                                                            class="btn btn-sm btn-outline-secondary"
                                                            @click="
                                                                increaseQuantity(
                                                                    index
                                                                )
                                                            "
                                                        >
                                                            +
                                                        </button>
                                                    </div>
                                                </td>
                                                <td class="text-center">
                                                    {{
                                                        item.unit_price
                                                            ? item.unit_price.toLocaleString()
                                                            : ""
                                                    }}
                                                </td>
                                                <td class="text-center">
                                                    {{
                                                        item.unit_price
                                                            ? item.total_price.toLocaleString()
                                                            : ""
                                                    }}
                                                </td>
                                                <td class="text-center">
                                                    <button
                                                        type="button"
                                                        class="btn btn-sm btn-danger"
                                                        @click="
                                                            removeService(index)
                                                        "
                                                    >
                                                        Xoá
                                                    </button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <div class="row mb-3 g-2">
                                    <p class="form-label fw-bold">
                                        Mã giảm giá
                                    </p>
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
                                                    Number(voucher.quantity) >
                                                        0 && voucher.status
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
                                        Lưu ý: bạn phải nhấn "Áp dụng" thì
                                        voucher mới có hiệu lực
                                    </p>
                                </div>

                                <p v-if="voucherError" class="text-danger">
                                    {{ voucherError }}
                                </p>

                                <p
                                    class="form-label fw-bold mb-3"
                                    v-if="startTime && endTime"
                                >
                                    Thời gian chơi:
                                    {{ formatDuration(duration) }} ({{
                                        ConvertPrice(
                                            Number(
                                                dataDetailTable?.pricingrule
                                                    ?.rate_per_hour
                                            )
                                        ) || "Chưa có dữ liệu"
                                    }}/h) =
                                    {{
                                        ConvertPrice(
                                            Number(
                                                dataDetailTable?.pricingrule
                                                    ?.rate_per_hour
                                            ) * Number(duration / 3600)
                                        ) || "Chưa có dữ liệu"
                                    }}
                                </p>

                                <p class="form-label fw-bold mb-3">
                                    Phí dịch vụ:
                                    {{ ConvertPrice(getTotalAmount()) || "0" }}
                                </p>

                                <p class="form-label fw-bold mb-3">
                                    Giảm giá giờ chơi thành viên hạng
                                    {{
                                        getMembershipRank(
                                            dataCustomer?.loyalty_points
                                        ).rank
                                    }}:
                                    {{
                                        getMembershipRank(
                                            dataCustomer?.loyalty_points
                                        ).voucher
                                    }}
                                    % =
                                    {{
                                        ConvertPrice(
                                            Number(
                                                Number(
                                                    dataDetailTable?.pricingrule
                                                        ?.rate_per_hour
                                                ) * Number(duration / 3600)
                                            ) *
                                                (Number(
                                                    getMembershipRank(
                                                        dataCustomer?.loyalty_points
                                                    ).voucher
                                                ) /
                                                    100)
                                        )
                                    }}
                                </p>

                                <p
                                    v-if="discountAmount !== null"
                                    class="text-success"
                                >
                                    Đã áp dụng mã:
                                    <strong>{{ voucherCode }}</strong> – Giảm
                                    {{ discountAmount }}% giờ chơi =
                                    {{
                                        ConvertPrice(
                                            (Number(
                                                Number(
                                                    dataDetailTable?.pricingrule
                                                        ?.rate_per_hour
                                                ) * Number(duration / 3600)
                                            ) *
                                                Number(discountAmount)) /
                                                100
                                        )
                                    }}
                                </p>

                                <p class="form-label fw-bold mb-3">
                                    Tổng tiền :
                                    {{
                                        ConvertPrice(
                                            totalPricePaid + getTotalAmount()
                                        )
                                    }}
                                </p>

                                <h4 class="form-label fw-bold mb-3">
                                    Thanh toán trước :
                                    {{ ConvertPrice(totalPricePaid) }}
                                </h4>

                                <div class="text-center">
                                    <button
                                        v-show="!idCreatedBooking"
                                        type="submit"
                                        class="btn btn-success px-5"
                                    >
                                        Đặt bàn ngay
                                    </button>
                                    <PayPalButton
                                        v-show="idCreatedBooking"
                                        :amount="totalPricePaid"
                                        :onSuccess="handleSuccess"
                                    />
                                </div>
                            </form>
                        </div>

                        <div class="col-12 col-lg-4 p-4 bg-light">
                            <h5 class="fw-bold mb-3">Danh sách đặt bàn</h5>
                            <div
                                v-if="
                                    searchBookingData &&
                                    searchBookingData.length
                                "
                            >
                                <div
                                    v-for="(
                                        booking, index
                                    ) in searchBookingData"
                                    :key="index"
                                    class="mb-3 p-3 border rounded bg-white shadow-sm"
                                >
                                    <div>
                                        <strong>Bắt đầu:</strong>
                                        {{ formatTime(booking.start_time) }}
                                    </div>
                                    <div>
                                        <strong>Kết thúc:</strong>
                                        {{ formatTime(booking.end_time) }}
                                    </div>
                                    <div class="text-end text-muted small mt-1">
                                        {{
                                            getTimeDifference(
                                                booking.created_at
                                            )
                                        }}
                                    </div>
                                </div>
                            </div>
                            <div v-else class="text-muted">
                                <p>Không có dữ liệu đặt bàn.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { io } from "socket.io-client";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";
import {
    checkBooking,
    createBooking,
    getAllTable,
    getTableById,
    getBookingByID,
    getAllMenuItem,
    createBookingItem,
    updateStatusBooking,
} from "~/services/booking.service";
import {
    type OptionSelect,
    type Bookings,
    type Tables,
    type BookingItems,
    type Discounts,
} from "~/constant/api";
import Swal from "sweetalert2";
import axios from "axios";
import ConvertPrice from "~/store/convertprice";
import formatTime from "~/store/formatTime";
import { apiImage } from "~/constant/request";
import { getMembershipRank } from "~/store/getMemberShip";
import {
    getAllDiscount,
    getDiscountByCode,
    getDiscountUseCode,
} from "~/services/discount.service";

import { useHead } from "@unhead/vue";
import {
    getInformation,
    updateInformationWalletPoint,
} from "~/services/information.service";
import { login } from "~/services/login.service";

useHead({
    title: "Đặt bàn",
});

const getDefaultDateTime = () => {
    const now = new Date();
    const vietnamTime = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    return vietnamTime.toISOString().slice(0, 16);
};

const dataDetailTable = ref<Tables | null>(null);
const duration = ref<number>(0);
const selectedItem = ref<any>("");
const selectedQuantity = ref(1);
const addedServices = ref<BookingItems[]>([]);
const optionListMenuItems = ref<OptionSelect[]>();
const tableData = ref<Tables[]>([]);
const isStatusTable = ref(false);
const searchBookingData = ref<Bookings[]>([]);
const loading = ref(true);
const customerName = ref("");
const customerPhone = ref("");
const startTime = ref(getDefaultDateTime());
const endTime = ref(getDefaultDateTime());
const selectedTableId = ref("");
const isModalOpen = ref(false);
const idCreatedBooking = ref("");
const dataCustomer = ref();
const dataVoucher = ref<Discounts[]>([]);
const voucherCode = ref("");
const discountAmount = ref<number | null>(null);
const voucherError = ref("");

const router = useRouter();

const socket = io("http://127.0.0.1:8000/", {
    transports: ["websocket"],
});

socket.on("connect", () => {
    console.log("Connected to WebSocket server!");
});

socket.on("connect_error", (error) => {
    console.error("Connection failed:", error);
});

socket.on("table_status_updated", (data) => {
    const table = tableData.value.find((t) => t._id === data._id);
    if (table) {
        table.status = data.status;
    }
});

const openModal = async (id: string, status: boolean) => {
    selectedTableId.value = id;
    isModalOpen.value = true;

    const resBooking = await getBookingByID(id);
    searchBookingData.value = resBooking;

    const resIdTable = await getTableById(id);
    dataDetailTable.value = resIdTable;
    isStatusTable.value = status;

    const now = new Date();
    const vietnamTime = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    if (status) {
        const startTimeAfter4Hours = new Date(
            vietnamTime.getTime() + 5 * 60 * 60 * 1000
        );
        const formattedStartTime = startTimeAfter4Hours
            .toISOString()
            .slice(0, 16);
        startTime.value = formattedStartTime;

        const endTimeAfter1Hour = new Date(
            startTimeAfter4Hours.getTime() + 1 * 60 * 60 * 1000
        );
        const formattedEndTime = endTimeAfter1Hour.toISOString().slice(0, 16);
        endTime.value = formattedEndTime;

        Swal.fire(
            "Lưu ý",
            "Bàn này đang có người chơi. Thời gian bắt đầu đặt bàn được đặt sau thời điểm hiện tại 4 tiếng.",
            "info"
        );
    } else {
        const startTimeAfter1Hour = new Date(
            vietnamTime.getTime() + 1 * 60 * 60 * 1000
        );
        const formattedStartTime = startTimeAfter1Hour
            .toISOString()
            .slice(0, 16);
        startTime.value = formattedStartTime;

        const endTimeAfter2Hours = new Date(
            vietnamTime.getTime() + 2 * 60 * 60 * 1000
        );
        const formattedEndTime = endTimeAfter2Hours.toISOString().slice(0, 16);
        endTime.value = formattedEndTime;
    }
};

const closeModal = async () => {
    const resBooking = await getBookingByID(String(dataDetailTable.value?._id));
    searchBookingData.value = resBooking;
    isModalOpen.value = false;
    customerName.value = "";
    customerPhone.value = "";
    startTime.value = getDefaultDateTime();
    endTime.value = getDefaultDateTime();
    addedServices.value = [];
    idCreatedBooking.value = "";
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

const totalPricePaid = computed(() => {
    const tableRate = Number(
        dataDetailTable?.value?.pricingrule?.rate_per_hour || 0
    );
    const timeCost = tableRate * (duration.value / 3600);
    const discountPercent =
        (Number(
            getMembershipRank(dataCustomer.value?.loyalty_points).voucher || 0
        ) +
            Number(discountAmount.value || 0)) /
        100;
    return timeCost * (1 - discountPercent);
});

const addService = () => {
    if (!selectedItem.value || selectedQuantity.value <= 0) {
        Swal.fire("Lỗi", "Vui lòng chọn dịch vụ và số lượng hợp lệ!", "error");
        return;
    }
    const existingIndex = addedServices.value.findIndex(
        (item) => item.name === selectedItem.value.label
    );

    if (existingIndex !== -1) {
        addedServices.value[existingIndex].quantity += Number(
            selectedQuantity.value
        );
        addedServices.value[existingIndex].total_price =
            addedServices.value[existingIndex].quantity *
            addedServices.value[existingIndex].unit_price;
    } else {
        addedServices.value.push({
            booking_id: "",
            image: String(selectedItem?.value?.hinhAnh),
            item_id: String(selectedItem?.value?.value),
            quantity: Number(selectedQuantity.value),
            unit_price: Number(selectedItem.value.price),
            total_price:
                Number(selectedItem.value.price) * selectedQuantity.value,
            name: String(selectedItem?.value?.label),
        });
    }

    selectedQuantity.value = 1;
};

const increaseQuantity = (index: number) => {
    addedServices.value[index].quantity += 1;
    addedServices.value[index].total_price =
        addedServices.value[index].quantity *
        addedServices.value[index].unit_price;
};

const decreaseQuantity = (index: number) => {
    if (addedServices.value[index].quantity > 1) {
        addedServices.value[index].quantity -= 1;
        addedServices.value[index].total_price =
            addedServices.value[index].quantity *
            addedServices.value[index].unit_price;
    }
};

const removeService = (index: number) => {
    addedServices.value.splice(index, 1);
};

const getTotalAmount = (): number => {
    return addedServices.value.reduce((sum, item) => {
        return sum + (item.total_price || 0);
    }, 0);
};

watch([startTime, endTime], () => {
    if (!startTime.value || !endTime.value) {
        duration.value = 0;
        return;
    }

    const start = new Date(startTime.value);
    const end = new Date(endTime.value);
    const diff = Math.floor((end.getTime() - start.getTime()) / 1000);
    duration.value = diff > 0 ? diff : 0;
});

const formatDuration = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    return `${hrs} giờ ${mins} phút `;
};

const handleSuccess = async (result: any) => {
    console.log("Thanh toán thành công:", result);
    await updateStatusBooking(idCreatedBooking.value);
    const customerData = Cookies.get("customer");
    if (customerData) {
        const customer = JSON.parse(customerData);
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
                dataUser.loyalty_points + totalPricePaid.value * 0.2,
            wallet: Number(dataUser.wallet) - totalPricePaid.value,
            role_name: customer.role_name,
        });

        const res = await login({
            email: String(dataUser.email),
            password: String(customer.password),
        });
        Cookies.set("customer", JSON.stringify(res), { expires: 1 });
    }
    closeModal();
    Swal.fire("Thông Báo", "Đặt bàn thành công !", "success");
};

const submitBooking = async () => {
    if (!customerName.value.trim()) {
        Swal.fire("Lỗi", "Vui lòng nhập tên khách hàng!", "error");
        return;
    }
    if (!customerPhone.value.trim()) {
        Swal.fire("Lỗi", "Vui lòng nhập số điện thoại!", "error");
        return;
    }
    if (!startTime.value) {
        Swal.fire("Lỗi", "Vui lòng chọn thời gian bắt đầu!", "error");
        return;
    }
    if (!endTime.value) {
        Swal.fire("Lỗi", "Vui lòng chọn thời gian kết thúc!", "error");
        return;
    }

    const now = new Date();
    const start = new Date(startTime.value);
    const fourHoursLater = new Date(now.getTime() + 4 * 60 * 60 * 1000);

    if (isStatusTable.value && start <= fourHoursLater) {
        Swal.fire(
            "Lỗi",
            "Thời gian bắt đầu phải sau thời điểm hiện tại ít nhất 4 giờ!",
            "error"
        );
        return;
    }

    try {
        const bookingData = {
            table_id: selectedTableId.value,
            user_id: dataCustomer?.value?._id,
            name: customerName.value,
            phone: customerPhone.value,
            start_time: startTime.value,
            end_time: endTime.value,
            money_paid: Number(
                Number(
                    getTotalAmount() +
                        Number(
                            dataDetailTable.value?.pricingrule?.rate_per_hour
                        ) *
                            Number(duration.value / 3600) *
                            (1 -
                                (Number(discountAmount.value) +
                                    Number(
                                        getMembershipRank(
                                            dataCustomer?.value?.loyalty_points
                                        ).voucher
                                    )) /
                                    100)
                )
            ),
            status: false,
        };

        const ischeckBooking = await checkBooking({
            table_id: selectedTableId.value,
            start_time: startTime.value,
            end_time: endTime.value,
        });
        if (ischeckBooking) {
            try {
                if (Number(discountAmount.value) > 0) {
                    await getDiscountUseCode(voucherCode.value);
                }
                const rescreateBooking = await createBooking(bookingData);

                idCreatedBooking.value = String(rescreateBooking?._id);

                const listBookingItem = addedServices.value.map((service) => ({
                    booking_id: idCreatedBooking.value,
                    item_id: String(service.item_id),
                    image: String(service.image),
                    quantity: Number(service.quantity),
                    unit_price: Number(service.unit_price),
                    total_price:
                        Number(service.unit_price) * Number(service.quantity),
                    name: String(service.name),
                }));

                for (const element of listBookingItem) {
                    await createBookingItem(element);
                }

                Swal.fire(
                    "Thông Báo",
                    "Vui lòng thanh toán để hoàn tất !",
                    "info"
                );
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    Swal.fire("Lỗi", error.response?.data.detail, "error");
                    voucherCode.value = "";
                    discountAmount.value = null;
                }
            }
        } else {
            Swal.fire("Thất bại", "Thời gian này đã có khách đặt!", "warning");
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Swal.fire("Lỗi", error.response?.data.detail, "error");
        }
    }
};

const getTimeDifference = (createdAt: Date) => {
    const createdDate: any = new Date(createdAt);
    const currentDate: any = new Date();
    const differenceMs = currentDate - createdDate;
    const differenceMinutes = Math.floor(differenceMs / (1000 * 60));
    if (differenceMinutes < 60) {
        return `${differenceMinutes} phút trước`;
    } else if (differenceMinutes < 1440) {
        const hours = Math.floor(differenceMinutes / 60);
        return `${hours} giờ trước`;
    } else {
        const days = Math.floor(differenceMinutes / 1440);
        return `${days} ngày trước`;
    }
};

const fetchData = async () => {
    try {
        const res = await getAllTable();
        tableData.value = res;

        const resListMenuItem = await getAllMenuItem();
        optionListMenuItems.value = resListMenuItem
            ?.filter(function (item) {
                return item?.stock_quantity > 10;
            })
            ?.map(function ({ _id, name, price, image }) {
                return {
                    value: _id || 0,
                    label: name || "",
                    price: price || 0,
                    hinhAnh: image || "",
                };
            })
            ?.sort(function (a, b) {
                return a.label.localeCompare(b.label);
            });
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        const customer = JSON.parse(customerData);
        dataCustomer.value = customer;
        await fetchData();
        const modalElement = document.getElementById("exampleModal");
        if (modalElement) {
            modalElement.addEventListener("hidden.bs.modal", () => {
                closeModal();
            });
        }
        const listVoucher = await getAllDiscount();
        dataVoucher.value = listVoucher;
    } else {
        router.push("/login");
    }
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
.card {
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
    position: relative;
    overflow: hidden;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card:hover h1,
.card:hover p {
    opacity: 0.1;
    transition: opacity 0.2s ease;
}

.btn-booking {
    position: absolute;
    left: 50%;
    transform: translate(-50%, 50%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    background: #fff;
    color: #4d4d4d;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    cursor: pointer;
}

.btn-booking:hover {
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
    transform: translate(-50%, 60%) scale(1.05);
}

.card:hover .btn-booking {
    opacity: 1;
    visibility: visible;
}

.card h1 {
    font-size: 3rem;
    font-weight: bold;
    transition: opacity 0.2s ease;
}

.card p {
    font-size: 1.2rem;
    transition: opacity 0.2s ease;
}

.bg-danger {
    background-color: #e74c3c !important;
}

.bg-success {
    background-color: #2ecc71 !important;
}

.btn-success {
    background-color: var(--color-primary) !important;
    border: none;
}

.modal-content {
    border-radius: 10px;
    overflow: hidden;
}

.modal-header {
    background: linear-gradient(90deg, var(--color-primary), #0056b3);
}

.btn-close-white {
    filter: brightness(0) invert(1);
}

.modal-body {
    background-color: #f8f9fa;
}

.modal-footer {
    border-top: none;
}

.form-control {
    background-color: #fff;
    border: 1px solid #ced4da;
    box-shadow: none;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.form-control:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    border-color: var(--color-primary);
}

.voucher-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.voucher-input {
    width: 160px;
    padding: 6px 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.apply-button {
    padding: 6px 14px;
    font-size: 14px;
}
</style>
