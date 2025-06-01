<template>
    <el-dialog
        v-model="visible"
        title="Đặt bàn"
        width="600px"
        @close="handleClose"
    >
        <el-form :model="form" label-position="top" label-width="100%">
            <el-row :gutter="20">
                <el-col>
                    <el-select
                        v-model="selectedTableId"
                        placeholder="-- Chọn bàn --"
                        size="large"
                        class="full-width mb-3"
                    >
                        <el-option
                            v-for="table in dataTable"
                            :key="table._id"
                            :label="`Bàn số ${table?.table_number} ${table?.description ? `- ${table?.description}` : ``} - ${table?.status ? `Đang sử dụng` : `Đang trống`}`"
                            :value="String(table?._id)"
                        />
                    </el-select>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Tên khách hàng">
                        <el-input
                            v-model="form.customerName"
                            placeholder="Nhập tên khách hàng"
                        />
                    </el-form-item>
                </el-col>

                <el-col :span="12">
                    <el-form-item label="Số điện thoại">
                        <el-input
                            v-model="form.customerPhone"
                            placeholder="Nhập số điện thoại"
                            type="tel"
                        />
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="20">
                <el-col>
                    <el-form-item label="Thời gian sử dụng" required>
                        <el-date-picker
                            v-model="dateRange"
                            type="datetimerange"
                            start-placeholder="Thời gian bắt đầu"
                            end-placeholder="Thời gian kết thúc"
                            format="DD-MM-YYYY HH:mm"
                            value-format="YYYY-MM-DDTHH:mm:ss"
                            style="width: 100%"
                        />
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>

        <template #footer>
            <el-button @click="handleClose">Hủy</el-button>
            <el-button type="primary" @click="handleConfirm">Đặt bàn</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import axios from "axios";
import { ElMessage } from "element-plus";
import { watch, ref, onMounted } from "vue";
import { Tables } from "~/constant/api";
import { checkBooking, createBooking } from "~/services/booking.service";
import { getAllTable } from "~/services/home.service";
import { useUserStore } from "~/store";

const props = defineProps({
    modelValue: Boolean,
});

const emit = defineEmits(["update:modelValue", "booking-success"]);

const visible = ref(false);
const selectedTableId = ref("");
const dataTable = ref<Tables[]>([]);
const useStore = useUserStore();

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

watch(
    () => props.modelValue,
    (val) => {
        visible.value = val;
    }
);

function getVietnamDate(offsetHours = 0): Date {
    const nowUTC = new Date();
    const vietnamTime = new Date(
        nowUTC.getTime() + 7 * 60 * 60 * 1000 + offsetHours * 60 * 60 * 1000
    );
    return vietnamTime;
}

function toISOStringWithoutMs(date: Date): string {
    return date.toISOString().split(".")[0];
}

const dateRange = ref<[string, string]>([
    toISOStringWithoutMs(getVietnamDate(1)),
    toISOStringWithoutMs(getVietnamDate(3)),
]);

const form = ref({
    customerName: "",
    customerPhone: "",
    startTime: dateRange.value[0],
    endTime: dateRange.value[1],
});

watch(dateRange, (val) => {
    form.value.startTime = val?.[0] || "";
    form.value.endTime = val?.[1] || "";
});

watch(visible, (val) => {
    if (val) {
        dateRange.value = [
            toISOStringWithoutMs(getVietnamDate(1)),
            toISOStringWithoutMs(getVietnamDate(3)),
        ];
    }
});

watch(selectedTableId, (val) => {
    const selectedTable = dataTable.value.find((t) => String(t._id) === val);
    if (selectedTable) {
        const offset = selectedTable.status ? 4 : 1;
        const newStart = toISOStringWithoutMs(getVietnamDate(offset + 1));
        const newEnd = toISOStringWithoutMs(getVietnamDate(offset + 3));

        dateRange.value = [newStart, newEnd];
    }
});

const handleClose = () => {
    visible.value = false;
    selectedTableId.value = "";
    form.value.customerPhone = "";
    form.value.customerPhone = "";
    emit("update:modelValue", false);
};

const handleConfirm = async () => {
    try {
        if (
            !form.value.customerName.trim() ||
            !form.value.customerPhone.trim()
        ) {
            form.value.customerName = String(useStore?.user?.fullname);
            form.value.customerPhone = String(useStore?.user?.phone);
        }
        const selectedTable = dataTable.value.find(
            (t) => String(t._id) === selectedTableId.value
        );

        if (!selectedTable) {
            Notification("Vui lòng chọn bàn hợp lệ", "warning");
            return;
        }

        const currentTime = new Date().getTime();
        const selectedStartTime = new Date(form.value.startTime).getTime();
        const diffInHours =
            (selectedStartTime - currentTime) / (1000 * 60 * 60);

        if (selectedTable.status && diffInHours < 4) {
            Notification(
                "Bàn này đang được sử dụng. Vui lòng chọn thời gian sau ít nhất 4 tiếng.",
                "warning"
            );
            return;
        }

        const ischeckBooking = await checkBooking({
            table_id: selectedTableId.value,
            start_time: form.value.startTime,
            end_time: form.value.endTime,
        });

        if (!ischeckBooking) {
            Notification("Khung giờ này đã có người đặt", "warning");
            return;
        }

        await createBooking({
            table_id: selectedTableId.value,
            user_id: String(useStore?.user?._id),
            name: form.value.customerName,
            phone: form.value.customerPhone,
            start_time: form.value.startTime,
            end_time: form.value.endTime,
            money_paid: 0,
            status: true,
        });

        handleClose();
        emit("booking-success");
        Notification("Đặt bàn thành công", "success");
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Notification(error.response?.data.detail, "error");
        }
    }
};

const fetchData = async () => {
    const resTable = await getAllTable();
    dataTable.value = resTable;
};

onMounted(() => {
    fetchData();
});
</script>

<style scoped>
.el-alert {
    margin-bottom: 1rem;
}
</style>
