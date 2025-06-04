<template>
    <el-dialog
        v-model="isVisible"
        title="Chuyển bàn"
        width="600px"
        @close="handleClose"
    >
        <div v-if="tableData.length">
            <el-table :data="tableData" style="width: 100%" height="300">
                <el-table-column
                    prop="table_number"
                    label="Bàn số"
                    width="100"
                />
                <el-table-column prop="status" label="Trạng thái">
                    <template #default="{ row }">
                        <el-tag :type="row.status ? 'success' : 'info'">
                            {{ row.status ? "Đang sử dụng" : "Trống" }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="Thao tác">
                    <template #default="{ row }">
                        <el-button
                            size="small"
                            @click="selectTable(row)"
                            :disabled="
                                row.status === true || row.id === currentTableId
                            "
                            :type="row.status === true ? 'danger' : 'primary'"
                            plain
                        >
                            {{
                                row.status === true
                                    ? "Không thể chuyển"
                                    : "Chuyển tới ngay"
                            }}
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div v-else>
            <el-empty description="Không có dữ liệu bàn" />
        </div>
    </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { Tables } from "~/constant/api";
import {
    getAllTable,
    getbyIdTable,
    updateTable,
    updateTableMenuItemTransfer,
} from "~/services/home.service";
import {
    getBookingByIDBooking,
    updateBooking,
} from "~/services/booking.service";
import axios from "axios";
import { useRouter } from "vue-router";

const props = defineProps<{
    modelValue: boolean;
    currentTableId: string | number;
}>();
const emit = defineEmits(["update:modelValue", "transfer-success"]);

const isVisible = ref(props.modelValue);

const tableData = ref<Tables[]>([]);

const route = useRouter();

watch(
    () => props.modelValue,
    (val) => {
        isVisible.value = val;
    }
);

watch(isVisible, (val) => {
    emit("update:modelValue", val);
});

const fetchData = async () => {
    try {
        const res = await getAllTable();
        tableData.value = res;
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    }
};

onMounted(() => {
    fetchData();
});

const selectTable = async (table: Tables) => {
    emit("update:modelValue", false);
    const tableDetailNew = await getbyIdTable(String(table?._id));
    const tableDetailOld = await getbyIdTable(String(props.currentTableId));
    if (!tableDetailNew.status) {
        try {
            await updateTable({
                _id: String(table?._id),
                table_number: Number(tableDetailNew?.table_number),
                table_type_id: String(tableDetailNew?.table_type_id),
                status: true,
                start_date: String(tableDetailOld?.start_date),
                end_date: String(tableDetailOld?.end_date),
                description: String(tableDetailNew?.description),
                name: String(tableDetailOld?.name),
                phone: String(tableDetailOld?.phone),
                booking_id: tableDetailOld?.booking_id
                    ? String(tableDetailOld.booking_id)
                    : "",
            });

            await updateTableMenuItemTransfer({
                old_table_id: String(props.currentTableId),
                new_table_id: String(table?._id),
            });

            if (tableDetailOld?.booking_id) {
                const resBooking = await getBookingByIDBooking(
                    String(tableDetailOld?.booking_id)
                );
                updateBooking({
                    _id: String(resBooking?._id),
                    user_id: String(resBooking?.user_id),
                    table_id: String(tableDetailNew?._id),
                    status: String(resBooking?.status),
                    start_time: String(resBooking?.start_time),
                    phone: String(resBooking?.phone),
                    name: String(resBooking?.name),
                    money_paid: String(resBooking?.money_paid),
                    end_time: String(resBooking?.end_time),
                    created_at: String(resBooking?.created_at),
                });
            }

            await updateTable({
                _id: String(props.currentTableId),
                table_number: Number(tableDetailOld?.table_number),
                table_type_id: String(tableDetailOld?.table_type_id),
                status: false,
                start_date: String(tableDetailOld?.start_date),
                end_date: String(tableDetailOld?.end_date),
                description: String(tableDetailOld?.description),
                name: "",
                phone: "",
                booking_id: "",
            });

            ElMessage.success(
                `Bạn chuyển bàn thành công sang bàn ${tableDetailNew?.table_number}`
            );
            route.push(`/${table?._id}`);
            await emit("transfer-success", table?._id);
            await fetchData();
        } catch (error) {
            if (axios.isAxiosError(error)) {
                ElMessage.warning(error.response?.data.detail);
            }
        }
    } else {
        ElMessage.warning("Bàn này đã được dùng!");
    }
};

const handleClose = () => {
    emit("update:modelValue", false);
};
</script>
