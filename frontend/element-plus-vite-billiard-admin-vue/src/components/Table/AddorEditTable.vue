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
            <el-form-item label="Số hiệu bàn" prop="table_number">
                <el-input
                    v-model="ruleForm.table_number"
                    :disabled="Boolean(route.params.id)"
                />
            </el-form-item>

            <el-form-item label="Ghi chú" prop="description">
                <el-input v-model="ruleForm.description" />
            </el-form-item>

            <el-form-item label="Loại bàn" prop="table_type_id">
                <el-select
                    v-model="ruleForm.table_type_id"
                    filterable
                    placeholder="Vui lòng chọn"
                >
                    <el-option
                        v-for="item in optionsTableType"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
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
import { OptionSelect, Tables } from "~/constant/api";
import {
    createTable,
    getbyIdTable,
    updateTable,
} from "~/services/table.service";
import { getAllTableType } from "~/services/tabletype.service";
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

const ruleForm = reactive<Tables>({
    table_number: 0,
    table_type_id: "",
    status: false,
    description: "",
    booking_id: "",
    start_date: null,
    end_date: null,
});

const rules = reactive<FormRules>({
    table_number: [
        {
            required: true,
            message: "Vui lòng nhập số hiệu bàn bàn",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    table_type_id: [
        {
            required: true,
            message: "Vui lòng chọn loại bàn",
            trigger: "blur",
        },
    ],
    status: [
        {
            required: true,
            message: "Vui lòng chọn trạng thái",
            trigger: "blur",
        },
    ],
});

const optionsTableType = ref<OptionSelect[]>();

async function fetchTableType() {
    const res = await getAllTableType();
    ruleForm.table_type_id = String(res[0]._id);
    optionsTableType.value = res?.map(function ({ _id, table_type_name }) {
        return {
            value: _id || 0,
            label: table_type_name || "",
        };
    });
}

const fetchById = async (id: string) => {
    const resId = await getbyIdTable(id);
    ruleForm.table_number = resId?.table_number;
    ruleForm.table_type_id = resId?.table_type_id;
    ruleForm.status = resId?.status;
    ruleForm.description = resId?.description;
    ruleForm.start_date = resId?.start_date;
    ruleForm.end_date = resId?.end_date;
    ruleForm.booking_id = resId?.booking_id;
};

onMounted(() => {
    fetchTableType();
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
                    await updateTable({
                        _id: String(route.params.id),
                        table_number: ruleForm.table_number,
                        description: ruleForm.description,
                        table_type_id: ruleForm.table_type_id,
                        status: ruleForm.status,
                        booking_id: String(ruleForm.booking_id),
                        start_date: ruleForm.start_date ?? null,
                        end_date: ruleForm.end_date ?? null,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/table");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification("Cập nhật thành công", "success");
                        router.push("/table");
                    }
                }
            } else {
                try {
                    await createTable({
                        table_number: ruleForm.table_number,
                        description: ruleForm.description,
                        table_type_id: ruleForm.table_type_id,
                        status: ruleForm.status,
                        booking_id: "",
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/table");
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
