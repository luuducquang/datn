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
            <el-form-item label="Mô tả" prop="decription">
                <el-input v-model="ruleForm.decription" />
            </el-form-item>

            <el-form-item label="Code" prop="code">
                <el-input v-model="ruleForm.code" />
            </el-form-item>

            <el-form-item label="Giá trị" prop="discount_value">
                <el-input v-model="ruleForm.discount_value" />
            </el-form-item>
            <el-form-item label="Số lượng" prop="quantity">
                <el-input v-model="ruleForm.quantity" />
            </el-form-item>
            <el-form-item label="Đã dùng" prop="used_count">
                <el-input disabled v-model="ruleForm.used_count" />
            </el-form-item>

            <el-form-item label="Trạng thái" prop="status">
                <el-select
                    v-model="ruleForm.status"
                    placeholder="Vui lòng chọn"
                >
                    <el-option label="Đang hoạt động" :value="true" />
                    <el-option label="Đã hết hạn" :value="false" />
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
import { Discounts } from "~/constant/api";
import {
    createDiscount,
    getbyIdDiscount,
    updateDiscount,
} from "~/services/discount.service";
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

const ruleForm = reactive<Discounts>({
    code: "",
    discount_value: 0,
    decription: "",
    quantity: 0,
    used_count: 0,
    status: true,
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
    const resId = await getbyIdDiscount(id);
    ruleForm.code = resId?.code;
    ruleForm.discount_value = resId?.discount_value;
    ruleForm.decription = resId?.decription;
    ruleForm.quantity = resId?.quantity;
    ruleForm.used_count = resId?.used_count;
    ruleForm.status = resId?.status;
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
                    await updateDiscount({
                        _id: String(route.params.id),
                        code: String(ruleForm.code),
                        discount_value: Number(ruleForm.discount_value),
                        decription: String(ruleForm.decription),
                        quantity: Number(ruleForm.quantity),
                        used_count: Number(ruleForm.used_count),
                        status: ruleForm.status,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/discount");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createDiscount({
                        code: String(ruleForm.code),
                        discount_value: Number(ruleForm.discount_value),
                        decription: String(ruleForm.decription),
                        quantity: Number(ruleForm.quantity),
                        used_count: Number(ruleForm.used_count),
                        status: ruleForm.status,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/discount");
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
