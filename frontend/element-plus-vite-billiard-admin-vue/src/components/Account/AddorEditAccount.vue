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

            <el-form-item label="Email" prop="email">
                <el-input v-model="ruleForm.email" />
            </el-form-item>

            <el-form-item label="Số điện thoại" prop="phone">
                <el-input v-model="ruleForm.phone" />
            </el-form-item>

            <el-form-item label="Mật khẩu" prop="password">
                <el-input
                    v-model="ruleForm.password"
                    :placeholder="
                        route.params.id ? 'Nhập mật khẩu mới nếu muốn đổi' : ''
                    "
                    type="password"
                />
            </el-form-item>

            <el-form-item label="Họ tên" prop="fullname">
                <el-input v-model="ruleForm.fullname" />
            </el-form-item>

            <el-form-item label="Địa chỉ" prop="address">
                <el-input v-model="ruleForm.address" />
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
import { Users, OptionSelect } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { getAllTypeAccount } from "~/services/typeaccount.service";
import {
    createAccount,
    getDetailAccount,
    updateAccount,
} from "~/services/account.service";
import axios from "axios";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const useStore = useUserStore();
const token = useStore?.user?.token;
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

const ruleForm = reactive<Users>({
    email: "",
    password: "",
    fullname: "",
    phone: "",
    address: "",
    avatar: "",
    loyalty_points: 0,
    wallet: 0,
    role_name: "",
});

const rules = reactive<FormRules>({
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

if (!route.params.id) {
    rules.password = [
        {
            required: true,
            message: "Vui lòng nhập mật khẩu",
            trigger: "blur",
        },
    ];
}

const optionsTypeAccount = ref<OptionSelect[]>();

async function fetchTypeAccount() {
    const res = await getAllTypeAccount();
    ruleForm.role_name = String(res[0].role_name);
    optionsTypeAccount.value = res?.map(function ({ _id, role_name }) {
        return {
            value: role_name || 0,
            label: role_name || "",
        };
    });
}

onMounted(() => {
    fetchTypeAccount();
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

const fetchById = async (id: string) => {
    const resId = await getDetailAccount(id);
    ruleForm.email = resId?.email || "";
    ruleForm.fullname = resId?.fullname || "";
    ruleForm.password = resId?.password || "";
    ruleForm.address = resId?.address || "";
    ruleForm.phone = resId?.phone || "";
    ruleForm.role_name = String(resId?.role_name || "");
    ruleForm.avatar = resId?.avatar || "";

    console.log(resId);

    fileListImg.value = [
        {
            name: resId.avatar,
            url: apiImage + resId.avatar,
        },
    ];
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
                    await updateAccount({
                        _id: String(route.params.id),
                        password: ruleForm.password,
                        fullname: ruleForm.fullname,
                        email: ruleForm.email,
                        phone: ruleForm.phone,
                        address: ruleForm.address,
                        avatar: ruleForm.avatar,
                        loyalty_points: 0,
                        role_name: ruleForm.role_name,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/account");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createAccount({
                        password: ruleForm.password,
                        fullname: ruleForm.fullname,
                        email: ruleForm.email,
                        phone: ruleForm.phone,
                        address: ruleForm.address,
                        avatar: ruleForm.avatar,
                        loyalty_points: 0,
                        wallet: 0,
                        role_name: ruleForm.role_name,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/account");
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
    fileListImg.value = [];
};
</script>
