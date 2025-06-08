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
            <el-form-item label="Tên quyền" prop="role_name">
                <el-input v-model="ruleForm.role_name" />
            </el-form-item>

            <el-form-item label="Mô tả" prop="role_description">
                <el-input v-model="ruleForm.role_description" />
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
import { Roles } from "~/constant/api";
import {
    createTypeAccount,
    getbyIdTypeAccount,
    updateTypeAccount,
} from "~/services/typeaccount.service";
import { ExecException } from "child_process";
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

const ruleForm = reactive<Roles>({
    role_name: "",
    role_description: "",
});

const rules = reactive<FormRules>({
    role_name: [
        {
            required: true,
            message: "Vui lòng nhập tên loại tài khoản",
            trigger: "blur",
        },
    ],
    role_description: [
        {
            required: true,
            message: "Vui lòng nhập mô tả",
            trigger: "blur",
        },
    ],
});

const fetchById = async (id: string) => {
    const resId = await getbyIdTypeAccount(id);
    ruleForm.role_name = resId?.role_name;
    ruleForm.role_description = resId?.role_description;
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
                    await updateTypeAccount({
                        _id: String(route.params.id),
                        role_name: ruleForm.role_name,
                        role_description: ruleForm.role_description,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/typeaccount");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createTypeAccount({
                        role_name: ruleForm.role_name,
                        role_description: ruleForm.role_description,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/typeaccount");
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
