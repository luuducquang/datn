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
            <el-form-item label="Ảnh đại diện" prop="anhDaiDien">
                <el-upload
                    :file-list="fileListImg"
                    class="upload-demo"
                    :action="uploadProps.action"
                    :on-remove="handleRemoveImg"
                    :on-change="handlerChange"
                    list-type="picture-card"
                >
                    <el-icon><Plus /></el-icon>
                </el-upload>
            </el-form-item>

            <el-form-item label="Tên tài khoản" prop="username">
                <el-input
                    v-model="ruleForm.username"
                    :disabled="Boolean(route.params.id)"
                />
            </el-form-item>

            <el-form-item label="Mật khẩu" prop="password">
                <el-input v-model="ruleForm.password" type="password" />
            </el-form-item>

            <el-form-item label="Họ tên" prop="fullname">
                <el-input v-model="ruleForm.fullname" />
            </el-form-item>

            <el-form-item label="Địa chỉ" prop="address">
                <el-input v-model="ruleForm.address" />
            </el-form-item>

            <el-form-item label="Email" prop="email">
                <el-input v-model="ruleForm.email" />
            </el-form-item>

            <el-form-item label="Số điện thoại" prop="phone">
                <el-input v-model="ruleForm.phone" />
            </el-form-item>

            <el-form-item label="Loại tài khoản" prop="role_name">
                <el-select
                    v-model="ruleForm.role_name"
                    filterable
                    placeholder="Vui lòng chọn"
                >
                    <el-option
                        v-for="item in optionsTypeAccount"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Loại nhân viên" prop="employee_type_id">
                <el-select
                    v-model="ruleForm.employee_type_id"
                    filterable
                    placeholder="Vui lòng chọn"
                >
                    <el-option
                        v-for="item in optionsTypeEmployee"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Lương theo giờ" prop="hourly_rate">
                <el-input v-model="ruleForm.hourly_rate" />
            </el-form-item>

            <el-form-item label="Lương theo tháng" prop="monthly_salary">
                <el-input v-model="ruleForm.monthly_salary" />
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
import type {
    ComponentSize,
    FormInstance,
    FormRules,
    UploadProps,
    UploadUserFile,
} from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import { useUserStore } from "~/store";
import { ElMessage } from "element-plus";
import router from "~/router";
import { useRoute } from "vue-router";
import { Employees, OptionSelect, Users } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    createEmployee,
    getbyIdEmployee,
    updateEmployee,
} from "~/services/employee.service";
import axios from "axios";
import { getAllTypeAccount } from "~/services/typeaccount.service";
import {
    createAccount,
    getDetailAccount,
    updateAccount,
} from "~/services/account.service";
import { getAllEmployeeType } from "~/services/employeetype.service";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const useStore = useUserStore();
const route = useRoute();
const token = useStore.user.token;

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const ruleForm = reactive<Employees & Users>({
    employee_type_id: "",
    user_id: "",
    hourly_rate: 0,
    monthly_salary: 0,
    username: "",
    password: "",
    fullname: "",
    email: "",
    phone: "",
    address: "",
    avatar: "",
    loyalty_points: 0,
    role_name: "",
});

const rules = reactive<FormRules>({
    employee_type_id: [
        {
            required: true,
            message: "Vui lòng chọn loại tài khoản",
            trigger: "blur",
        },
    ],
    hourly_rate: [
        {
            required: true,
            message: "Vui lòng nhập lương theo giờ",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Lương không hợp lệ. Vui lòng nhập lại",
            trigger: "blur",
        },
    ],
    monthly_salary: [
        {
            required: true,
            message: "Vui lòng nhập lương theo tháng",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Lương không hợp lệ. Vui lòng nhập lại",
            trigger: "blur",
        },
    ],
    username: [
        {
            required: true,
            message: "Vui lòng nhập tên tài khoản",
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
    fullname: [
        {
            required: true,
            message: "Vui lòng nhập họ tên",
            trigger: "blur",
        },
    ],
    password: [
        {
            required: true,
            message: "Vui lòng nhập mật khẩu",
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
    role_name: [
        {
            required: true,
            message: "Vui lòng chọn loại tài khoản",
            trigger: "blur",
        },
    ],
    avatar: [
        {
            required: true,
            message: "Vui lòng chọn ảnh đại diện",
            trigger: "blur",
        },
    ],
});

const uploadProps = {
    name: "file",
    action: `${apiImage}/upload`,
    headers: {
        authorization: `Bearer ${token}`,
    },
};

const fileListImg = ref<UploadUserFile[]>([]);

const handlerChange = (file: UploadUserFile, fileList: UploadUserFile[]) => {
    fileListImg.value = fileList.slice(-1);
    ruleForm.avatar = "/static/uploads/" + fileListImg.value[0].name;
};

const handleRemoveImg: UploadProps["onRemove"] = (uploadFile, uploadFiles) => {
    ruleForm.avatar = "";
};

const optionsTypeAccount = ref<OptionSelect[]>();
const optionsTypeEmployee = ref<OptionSelect[]>();

async function fetchTypeAccount() {
    const res = await getAllTypeAccount();
    ruleForm.role_name = String(res[0].role_name);
    optionsTypeAccount.value = res?.map(function ({ _id, role_name }) {
        return {
            value: _id || 0,
            label: role_name || "",
        };
    });
}

async function fetchTypeEmployee() {
    const res = await getAllEmployeeType();
    ruleForm.employee_type_id = String(res[0]._id);
    optionsTypeEmployee.value = res?.map(function ({
        _id,
        employee_type_name,
    }) {
        return {
            value: _id || 0,
            label: employee_type_name || "",
        };
    });
}

const fetchById = async (id: string) => {
    const resId = await getbyIdEmployee(id);
    const resDetailAccountId = await getDetailAccount(String(resId.user_id));
    ruleForm.user_id = resId.user_id || "";
    ruleForm.username = resDetailAccountId?.username || "";
    ruleForm.email = resDetailAccountId?.email || "";
    ruleForm.fullname = resDetailAccountId?.fullname || "";
    ruleForm.password = resDetailAccountId?.password || "";
    ruleForm.address = resDetailAccountId?.address || "";
    ruleForm.phone = resDetailAccountId?.phone || "";
    ruleForm.role_name = String(resDetailAccountId?.role_name || "");
    ruleForm.avatar = resDetailAccountId?.avatar || "";
    ruleForm.employee_type_id = resId?.employee_type_id || "";
    ruleForm.hourly_rate = resId?.hourly_rate || 0;
    ruleForm.monthly_salary = resId?.monthly_salary || 0;

    fileListImg.value = [
        {
            name: resDetailAccountId.avatar,
            url: apiImage + resDetailAccountId.avatar,
        },
    ];
};

onMounted(() => {
    fetchTypeAccount();
    fetchTypeEmployee();
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
                    const results = await Promise.allSettled([
                        updateEmployee({
                            _id: String(route.params.id),
                            employee_type_id: ruleForm.employee_type_id,
                            user_id: String(ruleForm.user_id),
                            hourly_rate: ruleForm.hourly_rate,
                            monthly_salary: ruleForm.monthly_salary,
                        }),
                        updateAccount({
                            _id: String(ruleForm.user_id),
                            username: ruleForm.username,
                            password: ruleForm.password,
                            fullname: ruleForm.fullname,
                            email: ruleForm.email,
                            phone: ruleForm.phone,
                            address: ruleForm.address,
                            avatar: ruleForm.avatar,
                            loyalty_points: 0,
                            role_name: ruleForm.role_name,
                        }),
                    ]);

                    const employeeResult = results[0];
                    const accountResult = results[1];

                    if (
                        employeeResult.status === "fulfilled" ||
                        accountResult.status === "fulfilled"
                    ) {
                        Notification("Cập nhật thành công", "success");
                        router.push("/employee");
                    } else {
                        Notification("Lỗi khi cập nhật", "error");
                    }
                } catch (error) {
                    console.error("Error:", error);
                    Notification("Lỗi khi cập nhật", "error");
                }
            } else {
                try {
                    const user = await createAccount({
                        username: ruleForm.username,
                        password: ruleForm.password,
                        fullname: ruleForm.fullname,
                        email: ruleForm.email,
                        phone: ruleForm.phone,
                        address: ruleForm.address,
                        avatar: ruleForm.avatar,
                        loyalty_points: 0,
                        role_name: ruleForm.role_name,
                    });
                    await createEmployee({
                        employee_type_id: ruleForm.employee_type_id,
                        user_id: String(user._id),
                        hourly_rate: ruleForm.hourly_rate,
                        monthly_salary: ruleForm.monthly_salary,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/employee");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            }
            console.log(ruleForm);
        } else {
            Notification("Bạn cần điền đủ thông tin", "warning");
        }
    } catch (fields) {
        Notification("Bạn cần điền đủ thông tin", "warning");
        console.log("error submit!", fields);
    }
};

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return;
    formEl.resetFields();
    fileListImg.value = [];
};
</script>
