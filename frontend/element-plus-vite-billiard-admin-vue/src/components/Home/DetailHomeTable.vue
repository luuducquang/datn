<template>
    <el-card class="card-container">
        <el-row :gutter="20">
            <el-col :span="8">
                <h1 class="m-0">Bàn số: {{ dataDetailTable?.table_number }}</h1>
                <p>Thời gian sử dụng: {{ formatTime(timeElapsed) }}</p>
                <p>
                    Giá 1h:
                    {{
                        ConvertPrice(
                            Number(dataDetailTable?.pricingrule?.rate_per_hour)
                        ) || "Chưa có dữ liệu"
                    }}
                </p>
                <p>Tạm tính: {{ ConvertPrice(Number(totalPrice)) }}</p>
                <p>Tiền dịch vụ: {{ ConvertPrice(Number(service_price)) }}</p>
                <h2>
                    Tổng tiền:
                    {{
                        ConvertPrice(Number(service_price) + Number(totalPrice))
                    }}
                </h2>

                <div class="button-container" style="margin-top: 20px">
                    <div v-if="dataDetailTable?.status === true">
                        <el-button
                            type="primary"
                            @click="StartAndPay"
                            style="
                                width: 100%;
                                padding: 12px;
                                background-color: #4caf50;
                                border-color: #4caf50;
                            "
                        >
                            Thanh Toán
                        </el-button>
                    </div>

                    <el-button
                        v-else
                        type="primary"
                        @click="toggleTimer"
                        style="
                            width: 100%;
                            padding: 12px;
                            background-color: #ffa500;
                            border-color: #ffa500;
                        "
                    >
                        Bắt đầu
                    </el-button>
                </div>
            </el-col>

            <el-col
                v-show="dataDetailTable?.status === true"
                :span="16"
                style="padding: 20px"
            >
                <div
                    class="button_add"
                    style="
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 20px;
                    "
                >
                    <el-button
                        type="success"
                        @click="
                            () => {
                                dialogFormMenuItemVisible = true;
                                resetForm(ruleFormRef);
                            }
                        "
                        style="
                            flex: 1;
                            padding: 12px;
                            margin-right: 10px;
                            background-color: #8bc34a;
                            border-color: #8bc34a;
                        "
                    >
                        Đồ ăn
                    </el-button>
                    <el-button
                        type="info"
                        @click="
                            () => {
                                dialogFormRentalItemVisible = true;
                                resetForm(ruleFormRef);
                            }
                        "
                        style="
                            flex: 1;
                            padding: 12px;
                            background-color: #2196f3;
                            border-color: #2196f3;
                        "
                    >
                        Thuê gậy
                    </el-button>
                </div>

                <el-table
                    :data="tableDataMenuItem"
                    class="table_content"
                    v-show="tableDataMenuItem.length > 0"
                    style="
                        margin-bottom: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    "
                >
                    <el-table-column
                        label="Sản phẩm"
                        align="center"
                        prop="menuitem.image"
                    >
                        <template #default="scope">
                            <img
                                :src="apiImage + scope.row.menuitem.image"
                                alt="Hình ảnh sản phẩm"
                                class="img_item"
                                style="
                                    width: 60px;
                                    height: 60px;
                                    object-fit: cover;
                                "
                            />
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
                                style="width: 100px"
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
                                    () => confirmEventMenuItem(scope.row._id)
                                "
                            >
                                <template #reference>
                                    <el-button size="small" type="danger">
                                        Delete
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>

                <el-table
                    :data="tableDataRentalItem"
                    class="table_content"
                    v-show="tableDataRentalItem.length > 0"
                    style="
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    "
                >
                    <el-table-column align="center" prop="rentalitem.image">
                        <template #default="scope">
                            <img
                                :src="apiImage + scope.row.rentalitem.image"
                                alt="Hình ảnh sản phẩm"
                                class="img_item"
                                style="
                                    width: 60px;
                                    height: 60px;
                                    object-fit: cover;
                                "
                            />
                        </template>
                    </el-table-column>
                    <el-table-column align="center" prop="start_time">
                        <template #default="scope">
                            <span>{{
                                formatTime(checkSeconds(scope.row.start_time))
                            }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column align="center" prop="unit_price">
                        <template #default="scope">
                            <span
                                >{{
                                    ConvertPrice(scope.row.unit_price)
                                }}/h</span
                            >
                        </template>
                    </el-table-column>
                    <el-table-column align="center">
                        <template #default="scope">
                            <span>
                                {{
                                    ConvertPrice(
                                        (scope.row.unit_price / 60 / 60) *
                                            checkSeconds(scope.row.start_time)
                                    )
                                }}
                            </span>
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
                                    () => confirmEventRentalItem(scope.row._id)
                                "
                            >
                                <template #reference>
                                    <el-button size="small" type="danger">
                                        Delete
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>
    </el-card>

    <el-dialog
        v-model="dialogFormMenuItemVisible"
        title="Thêm đồ ăn"
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
        v-model="dialogFormRentalItemVisible"
        title="Thuê gậy"
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
                    @change="handleRentalItemChange"
                >
                    <el-option
                        v-for="item in optionListRenTalItems"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>
            <el-form-item
                label="Giá thuê/1h"
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
                    <el-button @click="dialogFormRentalItemVisible = false"
                        >Cancel</el-button
                    >
                    <el-button
                        type="primary"
                        @click="submitFormRentalItem(ruleFormRef)"
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
            <p>Thời gian sử dụng: {{ formatTime(timeElapsed) }}</p>

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
                    <tr v-for="rental in tableDataRentalItem">
                        <td>{{ rental?.rentalitem?.item_name }}</td>
                        <td>
                            {{ formatTime(checkSeconds(rental?.start_time)) }}
                        </td>
                        <td>{{ ConvertPrice(rental?.unit_price) }}/h</td>
                        <td>
                            {{
                                ConvertPrice(
                                    (rental?.unit_price / 60 / 60) *
                                        checkSeconds(rental?.start_time)
                                )
                            }}
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="summary">
                <p>Tổng dịch vụ: {{ ConvertPrice(Number(service_price)) }}</p>
                <p>
                    Tổng tiền giờ chơi: {{ ConvertPrice(Number(totalPrice)) }}
                </p>
                <p class="total">
                    Thanh toán:
                    {{
                        ConvertPrice(Number(totalPrice) + Number(service_price))
                    }}
                </p>
                <p>
                    Giá giờ:
                    {{
                        ConvertPrice(
                            Number(dataDetailTable?.pricingrule?.rate_per_hour)
                        ) || "Chưa có dữ liệu"
                    }}
                </p>
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
import { nextTick, onMounted, onUnmounted } from "vue";
import { ref, computed, reactive } from "vue";
import { useRoute } from "vue-router";
import {
    OptionSelect,
    Rentals,
    TableMenuItems,
    TableRentalItems,
    Tables,
} from "~/constant/api";
import {
    createTableMenuItem,
    createTableRentalItem,
    deleteMenuItem,
    deleteMenuItembyTable,
    deleteRentalItem,
    getbyIdTable,
    getbyIdTableMenuItem,
    getbyIdTableRentalItem,
    updateTable,
    updateTableMenuItem,
} from "~/services/home.service";
import { getAllMenuItem } from "~/services/menuitem.service";
import ConvertPrice from "~/utils/convertprice";
import { apiImage } from "~/constant/request";
import { getAllRentalItem } from "~/services/rentalitem.service";
import { useUserStore } from "~/store";
import { createRental } from "~/services/rental.service";
import { createFoodOrder } from "~/services/foodorder.service";
import { createTimeSession } from "~/services/timesession.service";
import router from "~/router";

const route = useRoute();
const dataDetailTable = ref<Tables | null>(null);
const userStore = useUserStore();

const timeElapsed = ref(0);
const startTime = ref<string | null>(null);
let timer: NodeJS.Timeout | null = null;

const isPrepareBill = ref(true);

const ruleFormRef = ref<FormInstance>();

const optionListMenuItems = ref<OptionSelect[]>();
const optionListRenTalItems = ref<OptionSelect[]>();

const dialogFormMenuItemVisible = ref(false);
const dialogFormRentalItemVisible = ref(false);
const dialogVisiblePay = ref(false);
const formLabelWidth = "140px";

const tableDataMenuItem = ref<TableMenuItems[]>([]);
const tableDataRentalItem = ref<TableRentalItems[]>([]);

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

const PayAndPrintInvoice = async () => {
    const resIdTable = await getbyIdTable(String(route.params.id));
    if (resIdTable.status === true) {
        const listRentalItem = tableDataRentalItem.value.map(
            (value: TableRentalItems) => {
                return {
                    user_id: String(userStore?.user?._id),
                    item_id: String(value?.item_id),
                    rental_date: String(value?.start_time),
                    return_date: String(getLocalISOString()),
                    price: Number(
                        (
                            (value?.unit_price / 60 / 60) *
                            checkSeconds(value?.start_time)
                        ).toFixed(0)
                    ),
                    status: true,
                };
            }
        );

        const listIdRentalItem = tableDataRentalItem.value.map(
            (value: TableRentalItems) => {
                return value?._id;
            }
        );

        const listFoodOrderItem = tableDataMenuItem.value.map(
            (value: TableMenuItems) => {
                return {
                    user_id: String(userStore?.user?._id),
                    table_id: String(route.params.id),
                    item_id: value?.item_id,
                    pay_date: String(getLocalISOString()),
                    quantity: value.quantity,
                    unit_price: value.unit_price,
                    total_price: value.total_price,
                };
            }
        );

        await createTimeSession({
            table_id: String(route.params.id),
            start_time: String(dataDetailTable.value?.start_date),
            end_time: getLocalISOString(),
            price: Number(Number(totalPrice.value).toFixed(0)),
        });

        await updateTable({
            _id: String(route.params.id),
            table_number: Number(dataDetailTable.value?.table_number),
            table_type_id: String(dataDetailTable.value?.table_type_id),
            status: Boolean(!dataDetailTable.value?.status),
            start_date: String(startTime.value),
            end_date: String(startTime.value),
        });

        if (listRentalItem.length > 0) {
            await createRental(listRentalItem);
        }

        for (const idRental of listIdRentalItem) {
            if (idRental) {
                await deleteRentalItem(String(idRental));
            }
        }

        for (const item of listFoodOrderItem) {
            if (item) {
                await createFoodOrder(item);
            }
        }

        await fetchById(String(route.params.id));

        if (listFoodOrderItem.length > 0) {
            await deleteMenuItembyTable(String(route.params.id));
        }

        const printContent = document.getElementById("print-section");
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

const handleRentalItemChange = (value: string) => {
    if (optionListRenTalItems.value) {
        const selectedProduct = optionListRenTalItems.value.find(
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

const confirmEventRentalItem = async (Id: string) => {
    try {
        await deleteRentalItem(Id);
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
                dialogFormMenuItemVisible.value = false;
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

const submitFormRentalItem = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;

    try {
        const valid = await formEl.validate();
        if (valid) {
            try {
                await createTableRentalItem({
                    table_id: String(route.params.id),
                    item_id: form.item_id,
                    unit_price: form.unit_price,
                    start_time: getLocalISOString(),
                });
                Notification("Thêm thành công", "success");
                dialogFormRentalItemVisible.value = false;
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

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
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
            if (timer) {
                clearInterval(timer);
                timer = null;
                startTime.value = null;
            } else {
                startTime.value = getLocalISOString();
                timer = setInterval(updateElapsed, 1000);
            }

            await updateTable({
                _id: String(route.params.id),
                table_number: Number(dataDetailTable.value?.table_number),
                table_type_id: String(dataDetailTable.value?.table_type_id),
                status: !dataDetailTable.value?.status,
                start_date: String(startTime.value),
                end_date: String(getLocalISOString()),
            });

            await fetchById(String(route.params.id));
        } else {
            Notification("Bàn này đã được dùng", "warning");
        }
    } catch (error) {
        console.error("Error toggling timer:", error);
        Notification("Đã xảy ra lỗi khi cập nhật bàn", "error");
    }
}

function updateElapsed() {
    if (startTime.value) {
        const start = new Date(startTime.value).getTime();
        timeElapsed.value = Math.floor((Date.now() - start) / 1000);
    }
}

function checkSeconds(time: string | Date): number {
    let dateTime: Date;

    if (typeof time === "string") {
        dateTime = new Date(time);
    } else if (time instanceof Date) {
        dateTime = time;
    } else {
        throw new Error("Invalid input: time must be a string or Date object.");
    }

    if (isNaN(dateTime.getTime())) {
        throw new Error("Invalid input: time is not a valid date.");
    }

    return Math.floor((Date.now() - dateTime.getTime()) / 1000);
}

const formatTime = (s: number): string => {
    const hours = Math.floor(s / 3600);
    const minutes = Math.floor((s % 3600) / 60);
    const seconds = s % 60;

    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
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

    const resTableMenuItem = await getbyIdTableMenuItem(id);
    tableDataMenuItem.value = resTableMenuItem;

    if (dataDetailTable.value?.status === true) {
        startTime.value = String(dataDetailTable.value?.start_date);
        if (isPrepareBill.value) {
            timer = setInterval(async () => {
                updateElapsed();
                const resTableRentalItem = await getbyIdTableRentalItem(id);
                tableDataRentalItem.value = resTableRentalItem;
            }, 1000);
        } else {
            if (timer) {
                clearInterval(timer);
                timer = null;
            }
            updateElapsed();
            const resTableRentalItem = await getbyIdTableRentalItem(id);
            tableDataRentalItem.value = resTableRentalItem;
        }
    }
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

    const resListRentalItem = await getAllRentalItem();
    optionListRenTalItems.value = resListRentalItem
        ?.filter(function (item) {
            return item?.quantity_available > 0;
        })
        ?.map(function ({ _id, item_name, rental_price_hours }) {
            return {
                value: _id || 0,
                label: item_name || "",
                price: rental_price_hours || 0,
            };
        });
};

const totalPrice = computed(() => {
    const ratePerHour = dataDetailTable.value?.pricingrule?.rate_per_hour || 0;
    const timeInHours = timeElapsed.value / 3600;
    return (ratePerHour * timeInHours).toFixed(2);
});

const service_price = computed(() => {
    const menuItemTotal = tableDataMenuItem.value.reduce((total, item) => {
        return total + item.quantity * item.unit_price;
    }, 0);

    const rentalItemTotal = tableDataRentalItem.value.reduce((total, item) => {
        return (
            total + checkSeconds(item.start_time) * (item.unit_price / 60 / 60)
        );
    }, 0);

    return menuItemTotal + rentalItemTotal;
});

const StartAndPay = async () => {
    dialogVisiblePay.value = true;
};

onMounted(() => {
    if (route.params.id) {
        fetchById(String(route.params.id));
    }
});

onUnmounted(() => {
    if (timer) clearInterval(timer);
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
.ep-button {
    margin: 2px;
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
</style>
