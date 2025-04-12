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
            <el-form-item label="Loại bàn" prop="type_table_id">
                <el-select
                    v-model="ruleForm.type_table_id"
                    filterable
                    placeholder="Vui lòng chọn"
                    :disabled="Boolean(route.params.id)"
                >
                    <el-option
                        v-for="item in optionsTableType"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Giá chơi trong 1 phút" prop="rate_per_minute">
                <el-input v-model="ruleForm.rate_per_minute" />
            </el-form-item>

            <el-form-item label="Giá chơi trong 1 giờ" prop="rate_per_hour">
                <el-input v-model="ruleForm.rate_per_hour" />
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
import { OptionSelect, PricingRules } from "~/constant/api";
import {
    createPricingRule,
    getbyIdPricingRule,
    updatePricingRule,
} from "~/services/pricingrule.service";
import { ExecException } from "child_process";
import axios from "axios";
import { getAllTableType } from "~/services/tabletype.service";

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

const ruleForm = reactive<PricingRules>({
    type_table_id: "",
    rate_per_hour: 0,
    rate_per_minute: 0,
});

const rules = reactive<FormRules>({
    type_table_id: [
        {
            required: true,
            message: "Vui chọn loại bàn",
            trigger: "blur",
        },
    ],
    rate_per_minute: [
        {
            required: true,
            message: "Vui lòng nhập giá chơi trong 1 phút",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    rate_per_hour: [
        {
            required: true,
            message: "Vui lòng nhập giá chơi trong 1 giờ",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
});

const optionsTableType = ref<OptionSelect[]>();

async function fetchTableType() {
    const res = await getAllTableType();
    ruleForm.type_table_id = String(res[0]._id);
    optionsTableType.value = res?.map(function ({ _id, table_type_name }) {
        return {
            value: _id || 0,
            label: table_type_name || "",
        };
    });
}

const fetchById = async (id: string) => {
    const resId = await getbyIdPricingRule(id);
    ruleForm.type_table_id = resId?.type_table_id;
    ruleForm.rate_per_hour = resId?.rate_per_hour;
    ruleForm.rate_per_minute = resId?.rate_per_minute;
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
                    await updatePricingRule({
                        _id: String(route.params.id),
                        type_table_id: ruleForm.type_table_id,
                        rate_per_hour: ruleForm.rate_per_hour,
                        rate_per_minute: ruleForm.rate_per_minute,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/pricingrule");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createPricingRule({
                        type_table_id: ruleForm.type_table_id,
                        rate_per_hour: ruleForm.rate_per_hour,
                        rate_per_minute: ruleForm.rate_per_minute,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/pricingrule");
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
