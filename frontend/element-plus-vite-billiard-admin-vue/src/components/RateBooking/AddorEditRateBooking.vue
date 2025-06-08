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
            <el-form-item label="Mô tả" prop="text">
                <el-input v-model="ruleForm.text" />
            </el-form-item>

            <el-form-item label="Mức độ" prop="quality">
                <el-select
                    v-model="ruleForm.quality"
                    placeholder="Vui lòng chọn"
                >
                    <el-option label="1 sao" :value="1" />
                    <el-option label="2 sao" :value="2" />
                    <el-option label="3 sao" :value="3" />
                    <el-option label="4 sao" :value="4" />
                    <el-option label="5 sao" :value="5" />
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm(ruleFormRef)">
                    {{ route.params.id ? "Chỉnh sửa" : "Thêm" }}
                </el-button>
                <el-button @click="resetForm(ruleFormRef)">Làm mới</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import type { ComponentSize, FormInstance, FormRules } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import router from "~/router";
import { useRoute } from "vue-router";
import { RateBookings } from "~/constant/api";
import {
    createRateBooking,
    getbyIdRateBooking,
    updateRateBooking,
} from "~/services/ratebooking.service";
import axios from "axios";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const route = useRoute();

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const ruleForm = reactive<RateBookings>({
    booking_id: "",
    user_id: "",
    quality: 0,
    text: "",
});

const rules = reactive<FormRules>({
    table_type_name: [
        {
            required: true,
            message: "Vui lòng nhập loại bàn",
            trigger: "blur",
        },
    ],
});

const fetchById = async (id: string) => {
    const resId = await getbyIdRateBooking(id);
    ruleForm.quality = resId?.quality;
    ruleForm.text = resId?.text;
    ruleForm.booking_id = resId?.booking_id;
    ruleForm.user_id = resId?.user_id;
};

onMounted(() => {
    if (route.params.id) {
        fetchById(String(route.params.id));
    }
});

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return;

    try {
        const valid = await formEl.validate();
        if (valid) {
            if (route.params.id) {
                try {
                    await updateRateBooking({
                        _id: String(route.params.id),
                        booking_id: String(ruleForm.booking_id),
                        user_id: String(ruleForm.user_id),
                        quality: Number(ruleForm.quality),
                        text: String(ruleForm.text),
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/ratebooking");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createRateBooking({
                        booking_id: String(ruleForm.booking_id),
                        user_id: String(ruleForm.user_id),
                        quality: Number(ruleForm.quality),
                        text: String(ruleForm.text),
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/ratebooking");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
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
</script>
