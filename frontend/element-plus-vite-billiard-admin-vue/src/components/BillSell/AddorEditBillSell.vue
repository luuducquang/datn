<template>
    <el-card class="card_body">
        <el-form
            ref="ruleFormRef"
            :model="ruleForm"
            :rules="rules"
            label-width="auto"
            class="demo-ruleForm"
            :size="formSize"
            status-icon
        >
            <el-form-item label="Tên khách hàng" prop="name">
                <el-input v-model="ruleForm.name" />
            </el-form-item>

            <el-form-item label="Số điện thoại" prop="phone">
                <el-input v-model="ruleForm.phone" />
            </el-form-item>

            <el-form-item label="Email" prop="email">
                <el-input v-model="ruleForm.email" />
            </el-form-item>

            <el-form-item label="Địa chỉ giao hàng" prop="address_detail">
                <el-input v-model="ruleForm.address_detail" />
            </el-form-item>

            <el-form-item label="Tổng tiền" prop="total_price">
                <el-input
                    readonly
                    v-model="ruleForm.total_price"
                    type="number"
                />
            </el-form-item>

            <el-form-item
                v-if="route.params.id"
                label="Trạng thái"
                prop="status"
            >
                <el-select
                    v-model="ruleForm.status"
                    placeholder="Vui lòng chọn"
                    :disabled="ruleForm.status === 'Hoàn tất'"
                >
                    <el-option label="Đang xử lý" value="Đang xử lý" />
                    <el-option label="Đang giao hàng" value="Đang giao hàng" />
                    <el-option label="Đã giao hàng" value="Đã giao hàng" />
                    <el-option label="Đổi hàng" value="Đổi hàng" />
                    <el-option label="Trả hàng" value="Trả hàng" />
                    <el-option label="Hoàn tất" value="Hoàn tất" />
                    <el-option label="Huỷ đơn" value="Huỷ đơn" />
                </el-select>
            </el-form-item>

            <el-form-item label="Thanh toán" prop="is_paid">
                <template v-if="!route.params.id">
                    <el-select
                        v-model="ruleForm.is_paid"
                        placeholder="Chọn trạng thái thanh toán"
                    >
                        <el-option label="Chưa thanh toán" :value="false" />
                        <el-option label="Đã thanh toán" :value="true" />
                    </el-select>
                </template>
                <template v-else>
                    <el-tag
                        :type="ruleForm.is_paid ? 'success' : 'danger'"
                        effect="dark"
                    >
                        {{
                            ruleForm.is_paid
                                ? "Đã thanh toán"
                                : "Chưa thanh toán"
                        }}
                    </el-tag>
                </template>
            </el-form-item>
            <el-form-item v-if="route.params.id" label="Tuỳ chọn">
                <el-button type="warning" @click="invoiceDialogVisible = true"
                    >Xem hoá đơn</el-button
                >
            </el-form-item>

            <el-card>
                <el-form-item label="Tên sản phẩm" prop="item_id">
                    <el-select
                        v-model="ruleForm.item_id"
                        filterable
                        placeholder="Vui lòng chọn sản phẩm muốn mua"
                        @change="handleProductChange"
                    >
                        <el-option
                            v-for="item in optionsProduct"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>

                <el-form-item label="Số lượng" prop="quantity">
                    <el-input
                        v-model="ruleForm.quantity"
                        type="number"
                        @input="handleQuantityChange"
                    />
                </el-form-item>

                <el-form-item label="Đơn giá" prop="unit_price">
                    <el-input
                        readonly
                        v-model="ruleForm.unit_price"
                        type="number"
                    />
                </el-form-item>

                <el-form-item label="Tổng giá" prop="total_price">
                    <el-input
                        readonly
                        v-model="ruleForm.total_price_item"
                        type="number"
                    />
                </el-form-item>

                <el-form-item v-if="checkIsAdmin()">
                    <div class="list_btn">
                        <el-icon
                            @click="handlerAddDetail"
                            class="btn_add_detail"
                            ><Plus
                        /></el-icon>
                    </div>
                </el-form-item>

                <el-table :data="tableData" style="width: 100%">
                    <el-table-column
                        label="STT"
                        width="80"
                        align="center"
                        prop="stt"
                    >
                    </el-table-column>

                    <el-table-column
                        label="Hình ảnh"
                        align="center"
                        prop="hinhAnh"
                    >
                        <template #default="scope">
                            <img
                                :src="apiImage + scope.row.hinhAnh"
                                alt="Hình ảnh sản phẩm"
                                class="img_item"
                            /> </template
                    ></el-table-column>

                    <el-table-column
                        label="Số lượng"
                        align="center"
                        prop="soLuong"
                    >
                        <template #default="scope">
                            <el-input
                                class="amount_detail"
                                v-model="scope.row.soLuong"
                                type="number"
                                min="1"
                                @click="updateTotalPrice(scope.row)"
                            ></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column
                        label="Đơn giá"
                        align="center"
                        prop="donGia"
                    />

                    <el-table-column
                        label="Tổng tiền"
                        align="center"
                        prop="tongTien"
                    />

                    <el-table-column label="Tuỳ chọn" align="center">
                        <template #default="scope">
                            <!-- <el-button
                                v-if="route.params.id"
                                size="small"
                                @click="handleEdit(scope.$index, scope.row)"
                            >
                                Sửa
                            </el-button> -->
                            <el-popconfirm
                                v-if="checkIsAdmin()"
                                confirm-button-text="Yes"
                                cancel-button-text="No"
                                icon-color="#626AEF"
                                title="Bạn có muốn xoá không?"
                                @confirm="
                                    () => confirmEvent(scope.$index, scope.row)
                                "
                            >
                                <template #reference>
                                    <el-button
                                        size="small"
                                        type="danger"
                                        :disabled="
                                            ruleForm.status === 'Hoàn tất'
                                        "
                                    >
                                        Xoá
                                    </el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>

                <el-form-item class="btns_item">
                    <el-button
                        :disabled="ruleForm.status === 'Hoàn tất'"
                        type="primary"
                        @click="submitForm(ruleFormRef)"
                    >
                        {{ route.params.id ? "Chỉnh sửa" : "Thêm" }}
                    </el-button>
                    <el-button
                        @click="resetForm(ruleFormRef)"
                        :disabled="ruleForm.status === 'Hoàn tất'"
                        >Làm mới</el-button
                    >
                </el-form-item>
            </el-card>
        </el-form>
        <el-dialog
            v-model="invoiceDialogVisible"
            title="Hoá đơn đặt hàng"
            width="50%"
        >
            <template #default>
                <div id="print-section">
                    <div class="header">
                        <h1>Q-BILLIARDS CLUB</h1>
                        <p>Hưng Đạo - Tiên Lữ - Hưng Yên<br />0123.456.789</p>
                    </div>

                    <h3 style="text-align: center">HOÁ ĐƠN KHÁCH HÀNG</h3>
                    <p>Họ tên: {{ ruleForm.name }}</p>
                    <p>SĐT: {{ ruleForm.phone }}</p>
                    <p>Email: {{ ruleForm.email }}</p>
                    <p>Địa chỉ giao hàng: {{ ruleForm.address_detail }}</p>

                    <el-table :data="tableData" class="table-menu-item">
                        <el-table-column
                            label="Sản phẩm"
                            align="center"
                            prop="tenSanPham"
                        />
                        <el-table-column
                            label="Số lượng"
                            align="center"
                            prop="soLuong"
                        />
                        <el-table-column
                            label="Đơn giá"
                            align="center"
                            prop="donGia"
                        >
                            <template #default="scope">
                                {{ ConvertPrice(scope.row.donGia) }}
                            </template>
                        </el-table-column>
                        <el-table-column
                            label="Tổng tiền"
                            align="center"
                            prop="tongTien"
                        >
                            <template #default="scope">
                                {{ ConvertPrice(scope.row.tongTien) }}
                            </template>
                        </el-table-column>
                    </el-table>

                    <div class="summary">
                        <p class="total">
                            Tổng hoá đơn:
                            {{ ConvertPrice(ruleForm.total_price) }}
                        </p>
                    </div>

                    <div class="footer">
                        <p>In bởi qbillardclub.com.vn</p>
                        <p>Cảm ơn quý khách!</p>
                    </div>
                </div>
            </template>

            <template #footer>
                <el-button type="primary" @click="PrintInvoice"
                    >In hoá đơn</el-button
                >
                <el-button @click="invoiceDialogVisible = false"
                    >Đóng</el-button
                >
            </template>
        </el-dialog>
    </el-card>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed } from "vue";
import type {
    ComponentSize,
    FormInstance,
    FormRules,
    Table,
} from "element-plus";
import { Plus, Check } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import router from "~/router";
import { useRoute } from "vue-router";
import { useUserStore } from "~/store";
import { OptionSelect, TableBillSell } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    createBillSell,
    createSellItem,
    deleteSellItem,
    getDetailBillById,
    getDetailSellItemById,
    updateBillSell,
    updateSellItem,
} from "~/services/billsell.service";
import { watch } from "vue";
import { getAllProduct } from "~/services/product.service";
import { getCurrentDateTime } from "~/utils/getTimeCurrent";
import axios from "axios";
import { checkIsAdmin } from "~/utils/checkRole";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const route = useRoute();
const store = useUserStore();

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const invoiceDialogVisible = ref(false);

const ConvertPrice = (val: any) => {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
    }).format(val);
};

const ruleForm = reactive<any>({
    name: "",
    phone: "",
    email: "",
    address_detail: "",
    total_price: 0,
    status: "",
    item_id: "",
    quantity: 1,
    unit_price: 0,
    total_price_item: 0,
    is_paid: false,
});

const rules = reactive<FormRules>({
    name: [
        {
            required: true,
            message: "Vui lòng nhập tên khách hàng",
            trigger: "blur",
        },
    ],
    phone: [
        {
            required: true,
            message: "Vui lòng nhập số điện thoại",
            trigger: "blur",
        },
    ],
    email: [
        {
            required: true,
            message: "Vui lòng nhập email",
            trigger: "blur",
        },
    ],
    address_detail: [
        {
            required: true,
            message: "Vui lòng nhập địa chỉ giao hàng",
            trigger: "blur",
        },
    ],
    total_price: [
        {
            required: true,
            message: "Vui lòng nhập tổng giá",
            trigger: "blur",
        },
    ],
    status: [
        {
            required: true,
            message: "Vui lòng nhập trạng thái",
            trigger: "blur",
        },
    ],
    item_id: [
        {
            required: true,
            message: "Vui lòng chọn sản phẩm",
            trigger: "blur",
        },
    ],
    quantity: [
        {
            required: true,
            message: "Vui lòng nhập số lượng",
            trigger: "blur",
        },
    ],
    unit_price: [
        {
            required: true,
            message: "Vui lòng nhập đơn giá",
            trigger: "blur",
        },
    ],
    total_price_item: [
        {
            required: true,
            message: "Vui lòng nhập tổng giá",
            trigger: "blur",
        },
    ],
});

const optionsProduct = ref<OptionSelect[]>();

async function fetchProduct() {
    const resListProduct = await getAllProduct();
    const res = resListProduct?.filter(function (item) {
        return item?.quantity_available > 0;
    });
    ruleForm.item_id = String(res[0]?._id);
    ruleForm.unit_price = Number(res[0]?.price_reduction);
    ruleForm.total_price_item = Number(res[0]?.price_reduction);
    optionsProduct.value = res.map(function (value: any) {
        return {
            value: value._id,
            label: `${value.item_name} (${value.quantity_available})`,
            gia: value.price_reduction,
            hinhAnh: value.image,
        };
    });
}
onMounted(() => {
    fetchProduct();
});

const PrintInvoice = async () => {
    const printContent: any = document.getElementById("print-section");
    const originalContent = document.body.innerHTML;

    document.body.innerHTML = printContent.outerHTML;

    await window.print();

    document.body.innerHTML = originalContent;

    router
        .push(`/billsell/edit/${route.params.id}`)
        .then(() => window.location.reload());
};

const handleProductChange = (value: any) => {
    const filteredProduct = optionsProduct.value?.find(
        (product) => product.value === value
    );
    if (filteredProduct) {
        ruleForm.unit_price = filteredProduct.gia;
        ruleForm.total_price_item =
            Number(ruleForm.unit_price) * Number(ruleForm.quantity);
    } else {
        ruleForm.unit_price = 0;
    }
};
const handleQuantityChange = (value: any) => {
    ruleForm.total_price_item = Number(ruleForm.unit_price) * Number(value);
};

const fetchById = async (id: string) => {
    try {
        const resSellItem = await getDetailSellItemById(id);
        const resBillSell = await getDetailBillById(id);
        (ruleForm.name = resBillSell[0]?.name),
            (ruleForm.phone = resBillSell[0]?.phone),
            (ruleForm.email = resBillSell[0]?.email),
            (ruleForm.address_detail = resBillSell[0]?.address_detail),
            (ruleForm.total_price = resBillSell[0]?.total_price),
            (ruleForm.is_paid = resBillSell[0]?.is_paid),
            (ruleForm.status = resBillSell[0]?.status);
        const dataTempTable = resSellItem.map((value: any, index: number) => {
            return {
                stt: index + 1,
                maChiTietHoaDon: value._id,
                maSanPham: String(value.item_id),
                hinhAnh: String(value.product.image),
                soLuong: Number(value.quantity),
                donGia: Number(value.unit_price),
                tongTien: Number(value.unit_price) * Number(value.quantity),
                tenSanPham: value.product.item_name,
            };
        });
        tableData.value = dataTempTable;
    } catch (error) {
        router.push("/billsell");
        Notification("Hoá đơn không có sản phẩm", "success");
        const listitemDeleted = tableData.value.map((value: TableBillSell) => {
            return value.maChiTietHoaDon;
        });
        await updateBillSell({
            _id: String(route.params.id),
            user_id: String(store?.user?._id),
            sell_date: String(getCurrentDateTime()),
            name: ruleForm.name,
            email: ruleForm.email,
            phone: ruleForm.phone,
            address: String(ruleForm.address_detail),
            address_detail: String(ruleForm.address_detail),
            total_price: ruleForm.total_price,
            status: "Huỷ đơn",
            is_paid: ruleForm.is_paid,
        });
        for (const item of listitemDeleted) {
            if (item) {
                await deleteSellItem(item);
            }
        }
    }
};

onMounted(() => {
    if (route.params.id) {
        fetchById(String(route.params.id));
    }
});

const handleEdit = (index: number, row: TableBillSell) => {
    console.log(index, row);
};

const confirmEvent = async (index: number, row: TableBillSell) => {
    try {
        if (route.params.id) {
            await deleteSellItem(String(row.maChiTietHoaDon));
            fetchById(String(route.params.id));
            Notification("Xoá thành công", "success");
        } else {
            tableData.value.splice(index, 1);
        }
    } catch (error) {
        console.error("Error deleting =:", error);
        Notification("Lỗi khi xoá =", "error");
    }
};

const tableData = ref<TableBillSell[]>([]);

const handlerAddDetail = async () => {
    const filteredProduct = optionsProduct.value?.find(
        (product) => product.value === ruleForm.item_id
    );

    const existingProduct = tableData.value.find(
        (product) => product.maSanPham === ruleForm.item_id
    );

    if (route.params.id) {
        if (existingProduct) {
            Notification("Sản phẩm đã có, vui lòng tăng số lượng", "warning");
        } else {
            try {
                await createSellItem({
                    sell_id: String(route.params.id),
                    item_id: ruleForm.item_id,
                    quantity: ruleForm.quantity,
                    unit_price: ruleForm.unit_price,
                    total_price: ruleForm.total_price_item,
                });
                const resSellItem = await getDetailSellItemById(
                    String(route.params.id)
                );

                const totalTongTien = resSellItem.reduce(
                    (acc, item) => acc + item.total_price,
                    0
                );

                await updateBillSell({
                    _id: String(route.params.id),
                    user_id: String(store?.user?._id),
                    sell_date: String(getCurrentDateTime()),
                    name: ruleForm.name,
                    email: ruleForm.email,
                    phone: ruleForm.phone,
                    address: String(ruleForm.address_detail),
                    address_detail: String(ruleForm.address_detail),
                    total_price: totalTongTien,
                    status: ruleForm.status,
                    is_paid: ruleForm.is_paid,
                });

                fetchById(String(route.params.id));
                Notification("Thêm thành công", "success");
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    Notification(error.response?.data.detail, "warning");
                }
            }
        }
        fetchById(String(route.params.id));
    } else {
        if (existingProduct) {
            existingProduct.soLuong =
                Number(existingProduct.soLuong) + Number(ruleForm.quantity);
            existingProduct.tongTien =
                Number(existingProduct.soLuong) * existingProduct.donGia;
        } else {
            tableData.value.push({
                stt: Number(tableData.value.length + 1),
                maChiTietHoaDon: "",
                maSanPham: ruleForm.item_id,
                hinhAnh: String(filteredProduct?.hinhAnh),
                soLuong: Number(ruleForm.quantity),
                donGia: Number(ruleForm.unit_price),
                tongTien: Number(ruleForm.total_price_item),
            });
        }
    }
};

const updateTotalPrice = async (row: TableBillSell) => {
    if (row.soLuong === "0") {
        row.soLuong = 1;
    }
    row.tongTien = Number(row.soLuong) * row.donGia;

    if (route.params.id) {
        try {
            await updateSellItem({
                _id: String(row.maChiTietHoaDon),
                sell_id: String(route.params.id),
                item_id: String(row.maSanPham),
                quantity: Number(row.soLuong),
                unit_price: Number(row.donGia),
                total_price: Number(row.donGia) * Number(row.soLuong),
            });
            const resSellItem = await getDetailSellItemById(
                String(route.params.id)
            );

            const totalTongTien = resSellItem.reduce(
                (acc, item) => acc + item.total_price,
                0
            );

            await updateBillSell({
                _id: String(route.params.id),
                user_id: String(store?.user?._id),
                sell_date: String(getCurrentDateTime()),
                name: ruleForm.name,
                email: ruleForm.email,
                phone: ruleForm.phone,
                address: String(ruleForm.address_detail),
                address_detail: String(ruleForm.address_detail),
                total_price: totalTongTien,
                status: ruleForm.status,
                is_paid: ruleForm.is_paid,
            });

            fetchById(String(route.params.id));
            Notification("Điều chỉnh số lượng thành công", "success");
        } catch (error) {
            if (axios.isAxiosError(error)) {
                Notification(error.response?.data.detail, "warning");
                fetchById(String(route.params.id));
            }
        }
    }
};

watch(
    tableData.value,
    (newTableData) => {
        const totalAmount = newTableData.reduce(
            (acc: any, item: any) => acc + item.tongTien,
            0
        );
        ruleForm.total_price = totalAmount;
    },
    { deep: true }
);

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    try {
        const valid = await formEl.validate();
        if (valid) {
            if (route.params.id) {
                if (ruleForm.status === "Huỷ đơn") {
                    const listitemDeleted = tableData.value.map(
                        (value: TableBillSell) => {
                            return value.maChiTietHoaDon;
                        }
                    );
                    await updateBillSell({
                        _id: String(route.params.id),
                        user_id: String(store?.user?._id),
                        sell_date: String(getCurrentDateTime()),
                        name: ruleForm.name,
                        email: ruleForm.email,
                        phone: ruleForm.phone,
                        address: String(ruleForm.address_detail),
                        address_detail: String(ruleForm.address_detail),
                        total_price: ruleForm.total_price,
                        status: "Huỷ đơn",
                        is_paid: ruleForm.is_paid,
                    });
                    for (const item of listitemDeleted) {
                        if (item) {
                            await deleteSellItem(item);
                        }
                    }
                    Notification("Huỷ đơn thành công", "success");
                } else {
                    await updateBillSell({
                        _id: String(route.params.id),
                        user_id: String(store?.user?._id),
                        sell_date: String(getCurrentDateTime()),
                        name: ruleForm.name,
                        email: ruleForm.email,
                        phone: ruleForm.phone,
                        address: String(ruleForm.address_detail),
                        address_detail: String(ruleForm.address_detail),
                        total_price: ruleForm.total_price,
                        status: ruleForm.status,
                        is_paid: ruleForm.is_paid,
                    });
                    Notification("Cập nhật thành công", "success");
                }
                router.push("/billsell");
            } else {
                const listDataProduct = tableData.value.map((value: any) => {
                    return {
                        item_id: value.maSanPham,
                        quantity: Number(value.soLuong),
                        unit_price: Number(value.donGia),
                        total_price: Number(value.tongTien),
                    };
                });
                if (listDataProduct.length <= 0) {
                    Notification("Bạn chưa thêm sản phẩm", "warning");
                } else {
                    try {
                        await createBillSell({
                            user_id: String(store?.user?._id),
                            sell_date: String(getCurrentDateTime()),
                            name: ruleForm.name,
                            email: ruleForm.email,
                            phone: ruleForm.phone,
                            address: String(ruleForm.address_detail),
                            address_detail: String(ruleForm.address_detail),
                            total_price: ruleForm.total_price,
                            status: "Đang xử lý",
                            sell_items: listDataProduct,
                            is_paid: ruleForm.is_paid,
                        });
                        Notification("Thêm thành công", "success");
                        router.push("/billsell");
                    } catch (error) {
                        if (axios.isAxiosError(error)) {
                            Notification(
                                error.response?.data.detail,
                                "warning"
                            );
                        }
                    }
                }
            }
        } else {
            Notification("Bạn cần điền đủ thông tin", "warning");
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Notification(error.response?.data.detail, "warning");
        }
    }
};

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
};
</script>

<style scoped>
.line_item {
    height: 1px;
    background-color: #333;
}

.img_item {
    width: 70px;
    height: 70px;
    object-fit: cover;
}

.list_btn {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
.btn_add_detail {
    background-color: #3eeb27;
    color: aliceblue;
    font-size: 23px;
    cursor: pointer;
}

.btn_check_detail {
    background-color: #3eeb27;
    color: aliceblue;
    font-size: 23px;
    cursor: pointer;
}

.amount_detail {
    width: 60px;
}

.btns_item {
    margin-top: 10px;
}
</style>
