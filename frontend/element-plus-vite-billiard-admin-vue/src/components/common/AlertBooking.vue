<template>
    <el-dialog
        v-model="visible"
        title="Đặt bàn"
        width="600px"
        @close="handleClose"
    >
        <el-form :model="form" label-position="top">
            <el-form-item label="Chọn bàn">
                <el-select
                    v-model="selectedTableId"
                    placeholder="-- Chọn bàn --"
                    size="large"
                    class="w-full"
                >
                    <el-option
                        v-for="table in dataTable"
                        :key="table._id"
                        :label="`Bàn số ${table.table_number} ${table.description ? `- ${table.description}` : ''} - ${table.status ? 'Đang sử dụng' : 'Đang trống'}`"
                        :value="String(table._id)"
                    />
                </el-select>
            </el-form-item>

            <el-row :gutter="20">
                <el-col :span="12">
                    <el-form-item label="Tên khách hàng">
                        <el-input
                            v-model="form.customerName"
                            placeholder="Nhập tên khách hàng"
                            size="large"
                        />
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Số điện thoại">
                        <el-input
                            v-model="form.customerPhone"
                            placeholder="Nhập số điện thoại"
                            type="tel"
                            size="large"
                        />
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="20">
                <el-col :span="12">
                    <el-form-item label="Thời gian bắt đầu">
                        <el-date-picker
                            v-model="startDate"
                            type="date"
                            placeholder="Chọn ngày"
                            format="YYYY-MM-DD"
                            class="w-full"
                        />
                        <el-select
                            v-model="startHour"
                            placeholder="Chọn giờ"
                            class="w-full mt-2"
                        >
                            <el-option
                                v-for="time in timeSlots"
                                :key="time"
                                :label="time"
                                :value="time"
                            />
                        </el-select>
                    </el-form-item>
                </el-col>

                <el-col :span="12">
                    <el-form-item label="Thời gian kết thúc">
                        <el-date-picker
                            v-model="endDate"
                            type="date"
                            placeholder="Chọn ngày"
                            format="YYYY-MM-DD"
                            class="w-full"
                        />
                        <el-select
                            v-model="endHour"
                            placeholder="Chọn giờ"
                            class="w-full mt-2"
                        >
                            <el-option
                                v-for="time in timeSlots"
                                :key="time"
                                :label="time"
                                :value="time"
                            />
                        </el-select>
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
import { watch, ref, onMounted, computed } from "vue";
import { Tables } from "~/constant/api";
import {
    checkAvailableTables,
    checkBooking,
    createBooking,
} from "~/services/booking.service";
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

const startDate = ref("");
const endDate = ref("");
const startHour = ref("");
const endHour = ref("");

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

const timeSlots = computed(() => {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
        for (let minute of [0, 30]) {
            const h = hour.toString().padStart(2, "0");
            const m = minute.toString().padStart(2, "0");
            times.push(`${h}:${m}`);
        }
    }
    return times;
});

const startDateTime = computed(() => {
    return startDate.value && startHour.value
        ? `${startDate.value}T${startHour.value}:00`
        : "";
});

const endDateTime = computed(() => {
    return endDate.value && endHour.value
        ? `${endDate.value}T${endHour.value}:00`
        : "";
});

watch([startDateTime, endDateTime], async ([start, end]) => {
    const resAvailableTable = await checkAvailableTables({
        start_time: start,
        end_time: end,
    });
    selectedTableId.value = resAvailableTable;
    console.log(resAvailableTable);
});

const form = ref({
    customerName: "",
    customerPhone: "",
    startTime: "",
    endTime: "",
});

watch(selectedTableId, (val) => {
    const selectedTable = dataTable.value.find((t) => String(t._id) === val);
    if (selectedTable) {
        const offset = selectedTable.status ? 4 : 1;
    }
});

const handleClose = () => {
    visible.value = false;
    selectedTableId.value = "";
    form.value.customerName = "";
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
        const selectedStartTime = new Date(startDateTime.value).getTime();
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
            start_time: startDateTime.value,
            end_time: endDateTime.value,
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
            start_time: startDateTime.value,
            end_time: endDateTime.value,
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

    const now = new Date();

    const start = new Date(now.getTime() + 60 * 60 * 1000);
    startDate.value = start.toISOString().slice(0, 10);
    startHour.value = `${start.getHours().toString().padStart(2, "0")}:${start.getMinutes() < 30 ? "30" : "00"}`;

    const end = new Date(now.getTime() + 120 * 60 * 1000);
    endDate.value = end.toISOString().slice(0, 10);
    endHour.value = `${end.getHours().toString().padStart(2, "0")}:${end.getMinutes() < 30 ? "30" : "00"}`;

    // startDateTime.value = `${startDate.value}T${startHour.value}:00`;
    // endDateTime.value = `${endDate.value}T${endHour.value}:00`;
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
