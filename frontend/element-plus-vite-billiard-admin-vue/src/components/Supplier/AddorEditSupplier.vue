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
            <el-form-item label="Tên nhà phân phối" prop="name">
                <el-input v-model="ruleForm.name" />
            </el-form-item>

            <el-form-item label="Số điện thoại" prop="phone">
                <el-input v-model="ruleForm.phone" />
            </el-form-item>

            <el-form-item label="Địa chỉ" prop="address">
                <el-input v-model="ruleForm.address" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm(ruleFormRef)">
                    {{ route.params.id ? "Update" : "Create" }}
                </el-button>
                <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
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
import { Suppliers } from "~/constant/api";
import {
    createSuppliers,
    getbyIdSuppliers,
    updateSuppliers,
} from "~/services/supplier.service";
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

const ruleForm = reactive<Suppliers>({
    name: "",
    phone: "",
    address: "",
});

const rules = reactive<FormRules>({
    name: [
        {
            required: true,
            message: "Vui lòng nhập tên hãng",
            trigger: "blur",
        },
    ],
    phone: [
        {
            required: true,
            message: "Vui lòng nhập số điện thoại",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]{10,11}$/,
            message: "Số điện thoại không hợp lệ. Vui lòng nhập 10-11 số.",
            trigger: "blur",
        },
    ],
    address: [
        {
            required: true,
            message: "Vui lòng nhập địa chỉ",
            trigger: "blur",
        },
    ],
});

const fetchById = async (id: string) => {
    const resId = await getbyIdSuppliers(id);
    ruleForm.name = resId?.name;
    ruleForm.phone = resId?.phone;
    ruleForm.address = resId?.address;
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
                    await updateSuppliers({
                        _id: String(route.params.id),
                        name: ruleForm.name,
                        phone: ruleForm.phone,
                        address: ruleForm.address,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/supplier");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createSuppliers({
                        name: ruleForm.name,
                        phone: ruleForm.phone,
                        address: ruleForm.address,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/supplier");
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
