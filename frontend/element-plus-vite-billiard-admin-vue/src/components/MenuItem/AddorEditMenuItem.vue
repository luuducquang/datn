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
            <el-form-item label="Tên sản phẩm" prop="name">
                <el-input v-model="ruleForm.name" :rows="4" type="textarea" />
            </el-form-item>

            <el-form-item label="Ảnh sản phẩm" prop="image">
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

            <el-form-item label="Danh mục" prop="category_id">
                <el-select
                    v-model="ruleForm.category_id"
                    filterable
                    placeholder="Vui lòng chọn"
                >
                    <el-option
                        v-for="item in optionsCategory"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Loại sản phẩm" prop="is_rental">
                <el-select
                    v-model="ruleForm.is_rental"
                    placeholder="Vui lòng chọn"
                >
                    <el-option label="Thuê" :value="true" />
                    <el-option label="Bán" :value="false" />
                </el-select>
            </el-form-item>

            <el-form-item label="Tồn kho" prop="stock_quantity">
                <el-input v-model="ruleForm.stock_quantity" :disabled="true" />
            </el-form-item>

            <el-form-item label="Giá gốc" prop="price_origin">
                <el-input v-model="ruleForm.price_origin" :disabled="true" />
            </el-form-item>

            <el-form-item label="Giá" prop="price">
                <el-input v-model="ruleForm.price" />
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
    UploadFile,
    UploadProps,
    UploadUserFile,
} from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import { useUserStore } from "~/store";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { ElMessage } from "element-plus";
import router from "~/router";
import { useRoute } from "vue-router";
import { MenuItems, OptionSelect } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    createMenuItem,
    getbyIdMenuItems,
    updateMenuItem,
} from "~/services/menuitem.service";
import axios from "axios";
import { getAllCategoryMenuItem } from "~/services/categorymenuitem.service";

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

const ruleForm = reactive<MenuItems>({
    name: "",
    image: "",
    stock_quantity: 0,
    price: 0,
    category_id: "",
    price_origin: 0,
    is_rental: false,
});

const rules = reactive<FormRules>({
    name: [
        {
            required: true,
            message: "Vui lòng nhập tên sản phẩm",
            trigger: "blur",
        },
    ],
    image: [
        {
            required: true,
            message: "Vui lòng chọn ảnh",
            trigger: "blur",
        },
    ],
    stock_quantity: [
        {
            required: true,
            message: "Vui lòng nhập số lượng",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    price: [
        {
            required: true,
            message: "Vui lòng nhập giá",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    category_id: [
        {
            required: true,
            message: "Vui lòng chọn danh mục sản phẩm",
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
    ruleForm.image = "/static/uploads/" + fileListImg.value[0].name;
};

const handleRemoveImg: UploadProps["onRemove"] = (uploadFile, uploadFiles) => {
    ruleForm.image = "";
};

const optionsCategory = ref<OptionSelect[]>();

async function fetchCategory() {
    const res = await getAllCategoryMenuItem();
    ruleForm.category_id = String(res[0]._id);
    optionsCategory.value = res?.map(function ({ _id, category_name }) {
        return {
            value: _id || 0,
            label: category_name || "",
        };
    });
}

const fetchById = async (id: string) => {
    const resId = await getbyIdMenuItems(id);
    ruleForm.name = resId?.name;
    ruleForm.image = resId?.image;
    ruleForm.stock_quantity = resId?.stock_quantity;
    ruleForm.price = resId?.price;
    ruleForm.category_id = resId?.category_id;
    ruleForm.price_origin = resId?.price_origin;
    ruleForm.is_rental = resId?.is_rental;

    fileListImg.value = [
        {
            name: resId.image,
            url: apiImage + resId.image,
        },
    ];
};

onMounted(() => {
    fetchCategory();
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
                    await updateMenuItem({
                        _id: String(route.params.id),
                        name: ruleForm.name,
                        image: ruleForm.image,
                        stock_quantity: ruleForm.stock_quantity,
                        price: ruleForm.price,
                        category_id: ruleForm.category_id,
                        price_origin: ruleForm.price_origin,
                        is_rental: ruleForm.is_rental,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/menuitem");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createMenuItem({
                        name: ruleForm.name,
                        image: ruleForm.image,
                        stock_quantity: ruleForm.stock_quantity,
                        price: ruleForm.price,
                        category_id: ruleForm.category_id,
                        price_origin: ruleForm.price_origin,
                        is_rental: ruleForm.is_rental,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/menuitem");
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
