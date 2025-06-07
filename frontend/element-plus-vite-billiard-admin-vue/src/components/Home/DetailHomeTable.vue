<template>
    <el-card class="card-container modern-layout" shadow="always">
        <el-row :gutter="30">
            <el-col :span="10">
                <el-card shadow="hover" class="table-info-card modern-card">
                    <el-descriptions
                        :column="1"
                        border
                        size="large"
                        class="mb-3"
                    >
                        <template #title>
                            <div
                                class="d-flex justify-between items-center w-full"
                            >
                                <span>Thông tin khách và bàn</span>
                                <el-button
                                    v-if="dataDetailTable?.status"
                                    type="primary"
                                    size="small"
                                    class="ml-5"
                                    @click="dialogTransferTable = true"
                                >
                                    Chuyển bàn
                                </el-button>
                            </div>
                            <AlertTransferTable
                                v-model="dialogTransferTable"
                                :current-table-id="String(route.params.id)"
                                @transfer-success="fetchById"
                            />
                        </template>
                        <el-descriptions-item label="Tên khách hàng">
                            <el-input
                                v-model="customerForm.fullname"
                                placeholder="Nhập tên khách hàng"
                                size="large"
                                @blur="onChangeForm"
                            />
                        </el-descriptions-item>
                        <el-descriptions-item label="Số điện thoại">
                            <el-input
                                v-model="customerForm.phone"
                                placeholder="Nhập số điện thoại"
                                size="large"
                                @input="onPhoneInput"
                            />
                        </el-descriptions-item>

                        <el-descriptions-item label="Bàn số">
                            <span class="fw-bold">{{
                                dataDetailTable?.table_number || "--"
                            }}</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="Thời gian sử dụng">
                            {{
                                dataPriceTable?.total_seconds
                                    ? formatTime(
                                          Number(dataPriceTable?.total_seconds)
                                      )
                                    : "0p"
                            }}
                        </el-descriptions-item>
                        <el-descriptions-item
                            v-for="(
                                rule, index
                            ) in dataDetailTable?.pricingrule"
                            :key="index"
                            :label="index === 0 ? 'Giá theo giờ' : ''"
                        >
                            {{ rule.start_hour }}h - {{ rule.end_hour }}h:
                            {{ ConvertPrice(Number(rule.rate_per_hour)) }}
                        </el-descriptions-item>
                        <el-descriptions-item label="Tiền giờ chơi">
                            {{
                                dataPriceTable?.total_price
                                    ? ConvertPriceToK(
                                          Number(dataPriceTable?.total_price)
                                      )
                                    : ConvertPriceToK(0)
                            }}
                        </el-descriptions-item>
                        <el-descriptions-item label="Tiền dịch vụ">
                            {{ ConvertPrice(Number(service_price)) }}
                        </el-descriptions-item>
                        <el-descriptions-item
                            v-if="voucherCode && Number(discountAmount) > 0"
                            label="Giảm giá"
                        >
                            -{{ ConvertPriceToK(Number(discountPrice)) }}({{
                                discountAmount
                            }}%)
                        </el-descriptions-item>

                        <el-descriptions-item
                            v-if="
                                discountLoyalCustomer &&
                                Number(discountLoyalCustomer) > 0
                            "
                            label="Giảm giá hội viên thân thiết"
                        >
                            -{{
                                ConvertPriceToK(
                                    Number(discountPriceLoyalCustomer)
                                )
                            }}
                            ({{ discountLoyalCustomer }}%)
                        </el-descriptions-item>

                        <el-descriptions-item
                            v-if="moneyPaid > 0"
                            label="Tiền đặt bàn"
                        >
                            -{{ ConvertPriceToK(Number(moneyPaid)) }}
                        </el-descriptions-item>

                        <el-descriptions-item
                            label="Cần thanh toán"
                            label-class-name="total-label"
                            content-class-name="total-value"
                        >
                            <h3>
                                {{
                                    ConvertPriceToK(
                                        Number(service_price) +
                                            Number(totalPrice) -
                                            Number(discountPrice) -
                                            Number(discountPriceLoyalCustomer) -
                                            Number(moneyPaid)
                                    )
                                }}
                            </h3>
                        </el-descriptions-item>
                    </el-descriptions>

                    <el-button
                        v-if="dataDetailTable?.status === true"
                        type="success"
                        @click="StartAndPay"
                        size="large"
                        plain
                        class="full-width mt-3"
                    >
                        Thanh Toán
                    </el-button>

                    <el-button
                        v-else
                        type="warning"
                        @click="toggleTimer"
                        size="large"
                        plain
                        class="full-width mt-3"
                    >
                        Bắt đầu
                    </el-button>
                </el-card>
            </el-col>

            <el-col :span="14">
                <el-card>
                    <el-row class="voucher-row" :gutter="10">
                        <el-col :span="17">
                            <el-select
                                v-model="voucherCode"
                                placeholder="-- Chọn mã giảm giá --"
                                @change="handleVoucherChange"
                                size="large"
                                class="full-width"
                            >
                                <el-option
                                    :key="'none'"
                                    label="-- Không chọn voucher --"
                                    :value="''"
                                />
                                <el-option
                                    v-for="voucher in dataVoucher"
                                    :key="voucher._id"
                                    :label="`Giảm ${voucher.discount_value}% - ${Number(voucher.quantity) > 0 && voucher.status ? 'Đang hoạt động' : 'Hết hạn'}`"
                                    :value="voucher.code"
                                />
                            </el-select>
                        </el-col>
                        <el-col :span="7">
                            <el-button
                                type="primary"
                                @click="applyVoucher"
                                size="large"
                                class="full-width"
                            >
                                Áp dụng
                            </el-button>
                        </el-col>
                    </el-row>

                    <el-alert
                        v-if="voucherError"
                        type="error"
                        :closable="false"
                        show-icon
                        class="mb-2"
                    >
                        {{ voucherError }}
                    </el-alert>

                    <el-alert
                        v-if="discountAmount !== null"
                        type="success"
                        :closable="false"
                        show-icon
                        class="mb-2"
                    >
                        Đã áp dụng mã: <strong>{{ voucherCode }}</strong> – Giảm
                        {{ discountAmount }}%
                    </el-alert>

                    <el-row class="booking-row mt-3 mb-2" :gutter="10">
                        <el-col :span="24">
                            <el-select
                                v-model="selectedBookingId"
                                placeholder="-- Chọn bàn đã đặt --"
                                @change="handleBookingChange"
                                size="large"
                                class="full-width"
                                :disabled="shouldDisableBookingSelect"
                                :title="bookingTitleTooltip"
                            >
                                <el-option
                                    :key="'none'"
                                    label="-- Không chọn bàn đã đặt --"
                                    :value="''"
                                />
                                <el-option
                                    v-for="booking in dataBookings"
                                    :key="booking._id"
                                    :label="`${formatDate(booking.start_time)} - ${formatDate(booking.end_time)} - ${booking.name} (${booking.phone}) - ${ConvertPrice(Number(booking?.money_paid))} `"
                                    :value="String(booking._id)"
                                />
                            </el-select>
                        </el-col>
                    </el-row>

                    <div class="mb-3 text-right">
                        <el-button
                            type="success"
                            @click="
                                () => {
                                    dialogFormMenuItemVisible = true;
                                }
                            "
                        >
                            Thêm dịch vụ
                        </el-button>
                    </div>

                    <el-table
                        :data="tableDataMenuItem"
                        v-show="tableDataMenuItem.length > 0"
                        class="table-menu-item"
                    >
                        <el-table-column
                            label="Hình ảnh"
                            align="center"
                            prop="menuitem.image"
                        >
                            <template #default="scope">
                                <img
                                    :src="apiImage + scope.row?.menuitem?.image"
                                    alt="Hình ảnh sản phẩm"
                                    class="img-item"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="Sản phẩm"
                            align="center"
                            prop="unit_price"
                        >
                            <template #default="scope">
                                <span>{{ scope.row?.menuitem?.name }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="Số lượng"
                            align="center"
                            prop="quantity"
                        >
                            <template #default="scope">
                                <el-input-number
                                    v-model="scope.row.quantity"
                                    :min="1"
                                    :max="100"
                                    @change="
                                        (value) =>
                                            handleQuantityMenuItemChangeApi(
                                                value,
                                                scope.row
                                            )
                                    "
                                    class="quantity-input"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="Giá"
                            align="center"
                            prop="unit_price"
                        >
                            <template #default="scope">
                                <span>{{
                                    ConvertPrice(scope.row.unit_price)
                                }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="Tổng giá"
                            align="center"
                            prop="total_price"
                        >
                            <template #default="scope">
                                <span>{{
                                    ConvertPrice(scope.row.total_price)
                                }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column align="right">
                            <template #default="scope">
                                <el-popconfirm
                                    confirm-button-text="Yes"
                                    cancel-button-text="No"
                                    icon-color="#626AEF"
                                    title="Bạn có muốn xoá không?"
                                    @confirm="
                                        () =>
                                            confirmEventMenuItem(scope.row._id)
                                    "
                                >
                                    <template #reference>
                                        <el-button size="small" type="danger"
                                            >Xoá</el-button
                                        >
                                    </template>
                                </el-popconfirm>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </el-card>

    <el-dialog
        v-model="dialogFormMenuItemVisible"
        title="Thêm dịch vụ"
        width="500"
    >
        <el-form :model="form" :rules="rules" ref="ruleFormRef">
            <el-form-item
                label="Sản phẩm"
                :label-width="formLabelWidth"
                prop="item_id"
            >
                <el-select
                    v-model="form.item_id"
                    filterable
                    placeholder="Vui lòng chọn"
                    @change="handleMenuItemChange"
                >
                    <el-option
                        v-for="item in optionListMenuItems"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item
                label="Số lượng"
                :label-width="formLabelWidth"
                prop="quantity"
            >
                <el-input-number
                    v-model="form.quantity"
                    :min="1"
                    :max="100"
                    @change="handleChangeQuantityMenuItem"
                />
            </el-form-item>
            <el-form-item
                label="Giá bán"
                :label-width="formLabelWidth"
                prop="unit_price"
            >
                <el-input
                    v-model="form.unit_price"
                    autocomplete="off"
                    disabled
                />
            </el-form-item>
            <el-form-item
                label="Tổng giá"
                :label-width="formLabelWidth"
                prop="total_price"
            >
                <el-input
                    v-model="form.total_price"
                    autocomplete="off"
                    disabled
                />
            </el-form-item>
            <el-form-item>
                <div class="button_item">
                    <el-button @click="dialogFormMenuItemVisible = false"
                        >Cancel</el-button
                    >
                    <el-button
                        type="primary"
                        @click="submitFormMenuItem(ruleFormRef)"
                    >
                        Thêm
                    </el-button>
                </div>
            </el-form-item>
        </el-form>
    </el-dialog>
    <el-dialog
        v-model="dialogVisiblePay"
        title="Hoá đơn thanh toán"
        width="500"
    >
        <el-card id="print-section">
            <div class="header">
                <h1>Q-BILLIARDS CLUB</h1>
                <p>Hưng Đạo - Tiên Lữ - Hưng Yên<br />0123.456.789</p>
            </div>

            <h3 style="text-align: center">
                HÓA ĐƠN BÀN {{ dataDetailTable?.table_number }}
            </h3>
            <p>Giờ bắt đầu: {{ convertDate(dataDetailTable?.start_date) }}</p>
            <p>Giờ kết thúc: {{ convertDate(getLocalISOString()) }}</p>
            <p>
                Thời gian sử dụng:
                {{ formatTime(Number(dataPriceTable?.total_seconds)) }}
            </p>
            <p>
                {{
                    customerForm.fullname
                        ? "Khách hàng: " + customerForm.fullname
                        : "Khách lẻ"
                }}
            </p>
            <p v-if="customerForm.phone">
                Số điện thoại: {{ customerForm.phone }}
            </p>

            <table>
                <thead>
                    <tr>
                        <th>Tên</th>
                        <th>SL</th>
                        <th>Giá</th>
                        <th>Tổng</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="menu in tableDataMenuItem">
                        <td>{{ menu?.menuitem?.name }}</td>
                        <td>
                            {{ menu?.quantity }}
                        </td>
                        <td>{{ ConvertPrice(menu?.unit_price) }}/sp</td>
                        <td>
                            {{
                                ConvertPrice(
                                    Number(menu?.unit_price) *
                                        Number(menu?.quantity)
                                )
                            }}
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="summary">
                <p>Tổng dịch vụ: {{ ConvertPrice(Number(service_price)) }}</p>
                <p>
                    Tổng tiền giờ chơi:
                    {{ ConvertPriceToK(Number(totalPrice)) }}
                </p>
                <p v-if="voucherCode && Number(discountAmount) > 0">
                    Giảm giá {{ discountAmount }}%:
                    {{ ConvertPriceToK(Number(discountPrice)) }}
                </p>
                <p
                    v-if="
                        discountLoyalCustomer &&
                        Number(discountLoyalCustomer) > 0
                    "
                >
                    Hội viên thân thiết giảm {{ discountLoyalCustomer }}%:
                    {{ ConvertPriceToK(Number(discountPriceLoyalCustomer)) }}
                </p>
                <p v-if="moneyPaid > 0">
                    Đã thanh toán khi đặt bàn: {{ ConvertPriceToK(moneyPaid) }}
                </p>
                <p class="total">
                    Cần thanh toán:
                    {{
                        ConvertPriceToK(
                            Number(totalPrice) +
                                Number(service_price) -
                                Number(discountPrice) -
                                Number(discountPriceLoyalCustomer) -
                                Number(moneyPaid)
                        )
                    }}
                </p>
                <div v-if="dataDetailTable?.pricingrule?.length">
                    <p
                        v-for="(rule, index) in dataDetailTable.pricingrule"
                        :key="index"
                    >
                        Giá giờ {{ rule.start_hour }}h - {{ rule.end_hour }}h:
                        {{ ConvertPrice(Number(rule.rate_per_hour)) }}
                    </p>
                </div>
                <p v-else>Chưa có dữ liệu</p>
                <p>Nhân viên: {{ userStore?.user?.fullname }}</p>
            </div>

            <div class="footer">
                <p>In bởi qbillardclub.com.vn</p>
                <p>
                    Quý khách vui lòng kiểm tra lại hóa đơn trước khi thanh toán
                </p>
                <p>Xin chân thành cảm ơn quý khách</p>
                <p>Hẹn gặp lại quý khách lần sau</p>
            </div>
        </el-card>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisiblePay = false">Cancel</el-button>
                <el-button type="primary" @click="PayAndPrintInvoice">
                    Thanh toán và in hoá đơn
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ElMessage, FormInstance, FormRules } from "element-plus";
import { nextTick, onMounted, onUnmounted, watch } from "vue";
import { ref, computed, reactive } from "vue";
import { useRoute } from "vue-router";
import {
    Bookings,
    Discounts,
    OptionSelect,
    StockUpdateItem,
    TableMenuItems,
    TablePrice,
    Tables,
} from "~/constant/api";
import {
    createTableMenuItem,
    deleteMenuItem,
    deleteMenuItembyTable,
    getbyIdTable,
    getbyIdTableMenuItem,
    updateTable,
    updateTableMenuItem,
} from "~/services/home.service";
import {
    getAllMenuItem,
    increaseQuantityItem,
} from "~/services/menuitem.service";
import ConvertPriceToK from "~/utils/convertpricetoK";
import ConvertPrice from "~/utils/convertprice";
import { apiImage } from "~/constant/request";
import { useUserStore } from "~/store";
import { createOrderItem } from "~/services/orderitem.service";
import {
    createTimeSession,
    getCountByPhone,
} from "~/services/timesession.service";
import router from "~/router";
import {
    getAllDiscount,
    getDiscountByCode,
    getDiscountUseCode,
} from "~/services/discount.service";
import {
    getBookingByIDBooking,
    getBookingByIDTable,
} from "~/services/booking.service";
import { getBookingItemByIDBooking } from "~/services/bookingitem.service";
import { getTablePrice } from "~/services/table.service";
import { DiscountLoyalCustomer } from "~/utils/loyalcustomer";
import { debounce } from "lodash-es";

const route = useRoute();
const dataDetailTable = ref<Tables | null>(null);
const userStore = useUserStore();
let intervalId: ReturnType<typeof setInterval> | undefined;

const startTime = ref<string | null>(null);

const ruleFormRef = ref<FormInstance>();

const optionListMenuItems = ref<OptionSelect[]>();

const dialogFormMenuItemVisible = ref(false);
const dialogVisiblePay = ref(false);
const formLabelWidth = "140px";

const dialogTransferTable = ref(false);

const tableDataMenuItem = ref<TableMenuItems[]>([]);
const dataPriceTable = ref<TablePrice>();

const customerForm = reactive({
    fullname: "",
    phone: "",
});

const dataVoucher = ref<Discounts[]>([]);
const voucherCode = ref("");
const discountAmount = ref<number | null>(null);
const discountLoyalCustomer = ref<number | null>(null);
const voucherError = ref("");

const dataBookings = ref<Bookings[]>([]);
const selectedBookingId = ref("");
const moneyPaid = ref(0);

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const form = reactive({
    item_id: "",
    quantity: 1,
    unit_price: 0,
    total_price: 0,
});

const rules = reactive<FormRules>({
    item_id: [
        {
            required: true,
            message: "Vui lòng chọn sản phẩm",
            trigger: "change",
        },
    ],
    quantity: [
        {
            required: true,
            message: "Vui lòng chọn số lượng",
            trigger: "change",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "change",
        },
    ],
    unit_price: [
        {
            required: true,
            message: "Vui lòng nhập giá bán",
            trigger: "change",
        },
    ],
    total_price: [
        {
            required: true,
            message: "Vui lòng nhập tổng giá",
            trigger: "change",
        },
    ],
});

const onChangeForm = async () => {};

function onPhoneInput(value: string) {
    customerForm.phone = value.replace(/\D/g, "");
}

const debouncedUpdate = debounce(async (fullname: string, phone: string) => {
    await updateTable({
        _id: String(route.params.id),
        table_number: Number(dataDetailTable.value?.table_number),
        table_type_id: String(dataDetailTable.value?.table_type_id),
        status: Boolean(dataDetailTable.value?.status),
        start_date: String(dataDetailTable?.value?.start_date),
        end_date: String(dataDetailTable.value?.start_date),
        description: String(dataDetailTable?.value?.description),
        booking_id: String(dataDetailTable?.value?.booking_id),
        name: fullname,
        phone: phone,
    });

    try {
        const resCountPhone = await getCountByPhone(String(phone));
        discountLoyalCustomer.value = DiscountLoyalCustomer(
            Number(resCountPhone)
        );
    } catch (error) {
        discountLoyalCustomer.value = 0;
    }
}, 1000);

watch(
    () => [customerForm.fullname, customerForm.phone],
    ([newFullname, newPhone]) => {
        debouncedUpdate(newFullname, newPhone);
    }
);

const bookingTitleTooltip = computed(() => {
    if (!selectedBookingId.value) return "";

    const booking = dataBookings.value.find(
        (b) => String(b._id) === selectedBookingId.value
    );
    if (!booking) return "";

    const now = new Date();
    const bookingEnd = new Date(booking.end_time);

    if (now < bookingEnd) {
        const formattedDate = `${bookingEnd.getHours().toString().padStart(2, "0")}:${bookingEnd.getMinutes().toString().padStart(2, "0")}:${bookingEnd.getSeconds().toString().padStart(2, "0")} ${bookingEnd.getDate().toString().padStart(2, "0")}/${(bookingEnd.getMonth() + 1).toString().padStart(2, "0")}/${bookingEnd.getFullYear()}`;

        return `Bàn đã đặt này sẽ được mở sau ${formattedDate}`;
    }

    return "";
});

const shouldDisableBookingSelect = computed(() => {
    if (!selectedBookingId.value) return false;

    const booking = dataBookings.value.find(
        (b) => String(b._id) === selectedBookingId.value
    );
    if (!booking) return false;

    const now = new Date();
    const bookingEnd = new Date(booking.end_time);
    return now < bookingEnd;
});

const handleBookingChange = async (id: string) => {
    const selected = dataBookings.value.find((b) => b._id === id);
    await updateTable({
        _id: String(route.params.id),
        table_number: Number(dataDetailTable.value?.table_number),
        table_type_id: String(dataDetailTable.value?.table_type_id),
        status: Boolean(dataDetailTable.value?.status),
        start_date: String(dataDetailTable?.value?.start_date),
        end_date: String(dataDetailTable.value?.start_date),
        description: String(dataDetailTable?.value?.description),
        name: String(selected?.name),
        phone: String(selected?.phone),
        booking_id: selected?._id ? String(selected._id) : "",
    });
    if (selectedBookingId.value === "") {
        moneyPaid.value = 0;
    } else {
        try {
            const resBookingItem = await getBookingItemByIDBooking(
                String(selected?._id)
            );
            if (Array.isArray(resBookingItem) && resBookingItem.length > 0) {
                for (const item of resBookingItem) {
                    await createTableMenuItem({
                        table_id: String(route.params.id),
                        item_id: item.item_id,
                        quantity: item.quantity,
                        unit_price: item.unit_price,
                        total_price: item.quantity * item.unit_price,
                    });
                }
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                Notification(error.response?.data.detail, "warning");
                fetchById(String(route.params.id));
            }
        }
    }
    fetchById(String(route.params.id));
};

const formatDate = (date: Date | string): string => {
    const d = new Date(date);
    return d.toLocaleString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
    });
};

const handleVoucherChange = () => {
    discountAmount.value = null;
};

async function applyVoucher() {
    voucherError.value = "";
    discountAmount.value = null;

    if (!voucherCode.value) {
        voucherError.value = "Vui lòng chọn mã giảm giá.";
        return;
    }

    try {
        const valueDiscount = await getDiscountByCode(voucherCode.value);
        discountAmount.value = valueDiscount;
    } catch (error) {
        voucherError.value = "Mã giảm giá không tồn tại hoặc đã hết hiệu lực.";
    }
}

const PayAndPrintInvoice = async () => {
    const resIdTable = await getbyIdTable(String(route.params.id));
    if (resIdTable.status === true) {
        const listOrderMenuItem = tableDataMenuItem.value.map(
            (value: TableMenuItems) => {
                return {
                    item_id: value?.item_id,
                    quantity: value.quantity,
                    unit_price: value.unit_price,
                    total_price: value.total_price,
                };
            }
        );

        const getRentalItemIds: StockUpdateItem[] = tableDataMenuItem.value
            .filter((item) => item?.menuitem?.is_rental)
            .map((item) => ({
                item_id: String(item.item_id),
                quantity: Number(item.quantity),
            }));

        await increaseQuantityItem(getRentalItemIds);

        const idTimesession = await createTimeSession({
            table_id: String(route.params.id),
            start_time: String(dataDetailTable.value?.start_date),
            end_time: getLocalISOString(),
            price: Number(Number(totalPrice.value).toFixed(0)),
            price_paid: Number(
                Number(
                    Number(totalPrice.value) +
                        Number(service_price.value) -
                        Number(discountPrice.value) -
                        Number(discountPriceLoyalCustomer.value) -
                        Number(moneyPaid.value)
                ).toFixed(0)
            ),
            name: customerForm.fullname,
            phone: customerForm.phone,
        });

        await createOrderItem({
            user_id: String(userStore?.user?._id),
            table_id: String(route.params.id),
            timesession_id: String(idTimesession),
            total_price: Number(service_price.value),
            menu_items: listOrderMenuItem,
        });

        await updateTable({
            _id: String(route.params.id),
            table_number: Number(dataDetailTable.value?.table_number),
            table_type_id: String(dataDetailTable.value?.table_type_id),
            status: Boolean(!dataDetailTable.value?.status),
            start_date: String(dataPriceTable?.value?.start_time),
            end_date: String(dataPriceTable?.value?.end_time),
            description: String(dataDetailTable?.value?.description),
            name: "",
            phone: "",
            booking_id: "",
        });

        if (voucherCode.value) {
            await getDiscountUseCode(voucherCode.value);
        }

        await fetchById(String(route.params.id));

        if (listOrderMenuItem.length > 0) {
            await deleteMenuItembyTable(String(route.params.id));
        }

        const printContent: any = document.getElementById("print-section");
        const originalContent = document.body.innerHTML;

        document.body.innerHTML = printContent.outerHTML;

        await window.print();

        document.body.innerHTML = originalContent;

        router.push("/").then(() => window.location.reload());
    } else {
        Notification("Bàn này đã được thanh toán", "warning");
    }
};

const handleMenuItemChange = (value: string) => {
    if (optionListMenuItems.value) {
        const selectedProduct = optionListMenuItems.value.find(
            (item: OptionSelect) => item.value === value
        );

        if (selectedProduct) {
            form.unit_price = Number(selectedProduct.price);
        }
        if (form.item_id !== "") {
            form.total_price = Number(form.quantity) * Number(form.unit_price);
        }
    }
};

const handleChangeQuantityMenuItem = (
    cur: number | undefined,
    prev: number | undefined
) => {
    if (form.item_id !== "") {
        form.total_price = Number(cur) * Number(form.unit_price);
    }
};

const handleQuantityMenuItemChangeApi = async (
    value: number | undefined,
    item: TableMenuItems
) => {
    try {
        await updateTableMenuItem({
            _id: String(item._id),
            table_id: String(item.table_id),
            item_id: String(item.item_id),
            quantity: Number(value),
            unit_price: String(item.unit_price),
            total_price: Number(value) * Number(item.unit_price),
        });
        fetchById(String(route.params.id));
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Notification(error.response?.data.detail, "warning");
            fetchById(String(route.params.id));
        }
    }
};

const confirmEventMenuItem = async (Id: string) => {
    try {
        await deleteMenuItem(Id);
        Notification("Xoá thành công", "success");
        fetchById(String(route.params.id));
    } catch (error) {
        console.error("Error deleting =:", error);
        Notification("Lỗi khi xoá =", "error");
    }
};

const submitFormMenuItem = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;

    try {
        const valid = await formEl.validate();
        if (valid) {
            try {
                await createTableMenuItem({
                    table_id: String(route.params.id),
                    item_id: form.item_id,
                    quantity: form.quantity,
                    unit_price: form.unit_price,
                    total_price:
                        Number(form.quantity) * Number(form.unit_price),
                });
                Notification("Thêm thành công", "success");
                fetchById(String(route.params.id));
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    Notification(error.response?.data.detail, "warning");
                }
            }
        } else {
            Notification("Bạn cần điền đủ thông tin", "warning");
            console.log("error submit!");
        }
    } catch (fields) {
        Notification("Bạn cần điền đủ thông tin", "warning");
        console.log("error submit!", fields);
    }
};

function getLocalISOString() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

async function toggleTimer() {
    try {
        const tableDetail = await getbyIdTable(String(route.params.id));

        if (!tableDetail.status) {
            startTime.value = getLocalISOString();
            await updateTable({
                _id: String(route.params.id),
                table_number: Number(dataDetailTable.value?.table_number),
                table_type_id: String(dataDetailTable.value?.table_type_id),
                status: !dataDetailTable.value?.status,
                start_date: String(startTime.value),
                end_date: String(getLocalISOString()),
                description: String(dataDetailTable?.value?.description),
                name: String(customerForm.fullname),
                phone: String(customerForm.phone),
                booking_id: "",
            });
            const resPriceTable = await getTablePrice(String(route.params.id));
            dataPriceTable.value = resPriceTable;
            await fetchById(String(route.params.id));
        } else {
            Notification("Bàn này đã được dùng", "warning");
        }
    } catch (error) {
        console.error("Error toggling timer:", error);
        Notification("Đã xảy ra lỗi khi cập nhật bàn", "error");
    }
}

const formatTime = (s: number): string => {
    if (s < 60) {
        return "1p";
    }

    const hours = Math.floor(s / 3600);
    const minutes = Math.floor((s % 3600) / 60);

    if (hours === 0) {
        return `${minutes}p`;
    }

    if (minutes === 0) {
        return `${hours}h`;
    }

    return `${hours}h${minutes}p`;
};

function convertDate(inputDate: string | Date | any) {
    const date = new Date(inputDate);

    if (isNaN(date.getTime())) {
        throw new Error("Invalid date format");
    }

    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();

    return `${hours}:${minutes} ${day}/${month}/${year}`;
}

const fetchById = async (id: string) => {
    const resIdTable = await getbyIdTable(id);
    dataDetailTable.value = resIdTable;
    customerForm.fullname =
        String(dataDetailTable?.value?.name) != "null"
            ? String(dataDetailTable?.value?.name)
            : "";
    customerForm.phone =
        String(dataDetailTable?.value?.phone) != "null"
            ? String(dataDetailTable?.value?.phone)
            : "";

    selectedBookingId.value = String(dataDetailTable?.value?.booking_id);

    if (customerForm.phone != "") {
        const resCountPhone = await getCountByPhone(String(customerForm.phone));
        discountLoyalCustomer.value = DiscountLoyalCustomer(
            Number(resCountPhone)
        );
    }

    if (
        dataDetailTable.value?.booking_id != "" &&
        dataDetailTable.value?.booking_id != null
    ) {
        const dataBooking = await getBookingByIDBooking(
            String(dataDetailTable.value?.booking_id)
        );
        moneyPaid.value = Number(dataBooking?.money_paid);
    }

    const listVoucher = await getAllDiscount();
    dataVoucher.value = listVoucher.filter(
        (voucher: Discounts) =>
            voucher.status === true && Number(voucher.quantity) > 0
    );

    const resTableMenuItem = await getbyIdTableMenuItem(id);
    tableDataMenuItem.value = resTableMenuItem;

    dataBookings.value = await getBookingByIDTable(id);

    const resListMenuItem = await getAllMenuItem();
    optionListMenuItems.value = resListMenuItem
        ?.filter(function (item) {
            return item?.stock_quantity > 0;
        })
        ?.map(function ({ _id, name, price }) {
            return {
                value: _id || 0,
                label: name || "",
                price: price || 0,
            };
        });
};

const fetchPrice = async () => {
    if (dataDetailTable.value?.status === true) {
        const resPriceTable = await getTablePrice(String(route.params.id));
        dataPriceTable.value = resPriceTable;
    }
};

const totalPrice = computed(() => {
    return dataPriceTable?.value?.total_price || 0;
});

const service_price = computed(() => {
    const menuItemTotal = tableDataMenuItem.value.reduce((total, item) => {
        return total + item.quantity * item.unit_price;
    }, 0);

    return menuItemTotal;
});

const discountPrice = computed(() => {
    const price =
        Number(service_price.value || 0) + Number(totalPrice.value || 0);
    return price * (Number(discountAmount.value || 0) / 100);
});

const discountPriceLoyalCustomer = computed(() => {
    const price =
        Number(service_price.value || 0) + Number(totalPrice.value || 0);
    return price * (Number(discountLoyalCustomer.value || 0) / 100);
});

const StartAndPay = async () => {
    fetchPrice();
    dialogVisiblePay.value = true;
};

onMounted(async () => {
    if (route.params.id) {
        await fetchById(String(route.params.id));
        await fetchPrice();
        intervalId = setInterval(() => {
            fetchPrice();
        }, 60000);
    }
});

onUnmounted(() => {
    if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.img_item {
    width: 70px;
    height: 70px;
    object-fit: cover;
}
.button_item {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.button_add {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
.card-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.content {
    flex: 1;
    overflow-y: auto;
}

.button-container {
    display: flex;
    justify-content: center;
}
.custom-input-number {
    width: 100px;
}

.ep-table th.ep-table__cell.is-leaf,
.ep-table td.ep-table__cell {
    border-bottom: 0px solid #000 !important;
}

.ep-button + .ep-button {
    margin-left: 0px;
}

/* Billllllllllllllllllllllllllllll */
h1,
h2 {
    text-align: center;
    margin: 5px 0;
}

.header,
.footer {
    text-align: center;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}

table th,
table td {
    border: 1px solid #000;
    text-align: center;
    padding: 5px;
}

table th {
    background-color: #f0f0f0;
}

.summary {
    margin-top: 10px;
    text-align: right;
}

.summary p {
    margin: 2px 0;
}

.total {
    font-size: 1.2em;
    font-weight: bold;
}

.card-container {
    padding: 30px;
    border-radius: 12px;
    background-color: #f9f9f9;
}

.modern-card {
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 20px;
}

.full-width {
    width: 100%;
}

.img-item {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 8px;
}

.table-menu-item {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.quantity-input {
    width: 100px;
}

.text-right {
    text-align: right;
}

.total-label {
    font-weight: bold;
    color: #409eff;
}

.total-value {
    font-size: 18px;
    font-weight: bold;
    color: #e74c3c;
}
.full-width {
    width: 100%;
}

.voucher-row {
    margin-bottom: 12px;
    align-items: center;
}
</style>
