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
            <el-form-item label="Tên sản phẩm" prop="item_name">
                <el-input
                    v-model="ruleForm.item_name"
                    :rows="4"
                    type="textarea"
                />
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

            <el-form-item label="Hãng sản xuất" prop="manufactor_id">
                <el-select
                    v-model="ruleForm.manufactor_id"
                    filterable
                    placeholder="Vui lòng chọn"
                >
                    <el-option
                        v-for="item in optionsManufactor"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Giá" prop="price">
                <el-input v-model="ruleForm.price" :disabled="true"/>
            </el-form-item>

            <el-form-item label="Giá Giảm" prop="price_reduction">
                <el-input v-model="ruleForm.price_reduction"  :disabled="true"/>
            </el-form-item>

            <el-form-item label="Giá 1 giờ" prop="rental_price_hours">
                <el-input v-model="ruleForm.rental_price_hours" />
            </el-form-item>

            <el-form-item label="Giá 1 ngày" prop="rental_price_day">
                <el-input v-model="ruleForm.rental_price_day" />
            </el-form-item>

            <el-form-item label="Số lượng" prop="quantity_available">
                <el-input v-model="ruleForm.quantity_available" :disabled="true" />
            </el-form-item>

            <el-form-item label="Xuất xứ" prop="origin">
                <el-input v-model="ruleForm.origin" />
            </el-form-item>

            <el-form-item label="Mô tả" prop="description">
                <el-input
                    v-model="ruleForm.description"
                    :rows="4"
                    type="textarea"
                />
            </el-form-item>

            <el-form-item label="Chi tiết" prop="description_detail">
                <ckeditor
                    :editor="editor"
                    v-model="ruleForm.description_detail"
                />
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
import { RentalItems, OptionSelect } from "~/constant/api";
import { apiImage } from "~/constant/request";
import {
    createRentalItem,
    getbyIdRentalItems,
    updateRentalItem,
} from "~/services/rentalitem.service";
import axios from "axios";
import { getAllCategoryRentalItem } from "~/services/categoryrentalitem.service";
import { getAllManufactor } from "~/services/manufactor.service";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const useStore = useUserStore();
const token = useStore.user.token;
const route = useRoute();

const editor = ClassicEditor;

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const ruleForm = reactive<RentalItems>({
    manufactor_id: "",
    category_id: "",
    item_name: "",
    image: "",
    price: 0,
    price_reduction: 0,
    rental_price_day: 0,
    rental_price_hours: 0,
    quantity_available: 0,
    view: 0,
    origin: "",
    description: "",
    description_detail: "",
});

const rules = reactive<FormRules>({
    category_id: [
        {
            required: true,
            message: "Vui lòng chọn danh mục sản phẩm",
            trigger: "blur",
        },
    ],
    manufactor_id: [
        {
            required: true,
            message: "Vui lòng chọn danh mục sản phẩm",
            trigger: "blur",
        },
    ],
    item_name: [
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
    price: [
        {
            required: true,
            message: "Vui lòng nhập số giá",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    price_reduction: [
        {
            required: true,
            message: "Vui lòng nhập giá giảm",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    rental_price_day: [
        {
            required: true,
            message: "Vui lòng nhập giá thuê theo ngày",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    rental_price_hours: [
        {
            required: true,
            message: "Vui lòng nhập giá thuê theo giờ",
            trigger: "blur",
        },
        {
            pattern: /^[0-9]+$/,
            message: "Vui lòng nhập số tự nhiên",
            trigger: "blur",
        },
    ],
    quantity_available: [
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
    origin: [
        {
            required: true,
            message: "Vui lòng nhập xuất xứ",
            trigger: "blur",
        },
    ],
    description: [
        {
            required: true,
            message: "Vui lòng nhập mô tả sản phẩm",
            trigger: "blur",
        },
    ],
    description_detail: [
        {
            required: true,
            message: "Vui lòng nhập chi tiêt sản phẩm",
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
    const res = await getAllCategoryRentalItem();
    ruleForm.category_id = String(res[0]._id);
    optionsCategory.value = res?.map(function ({ _id, category_name }) {
        return {
            value: _id || 0,
            label: category_name || "",
        };
    });
}

const optionsManufactor = ref<OptionSelect[]>();

async function fetchManufactor() {
    const res = await getAllManufactor();
    ruleForm.manufactor_id = String(res[0]._id);
    optionsManufactor.value = res?.map(function ({ _id, name }) {
        return {
            value: _id || 0,
            label: name || "",
        };
    });
}

const fetchById = async (id: string) => {
    const resId = await getbyIdRentalItems(id);
    ruleForm.manufactor_id = resId?.manufactor_id;
    ruleForm.category_id = resId?.category_id;
    ruleForm.item_name = resId?.item_name;
    ruleForm.price = resId?.price;
    ruleForm.price_reduction = resId?.price_reduction;
    ruleForm.rental_price_day = resId?.rental_price_day;
    ruleForm.rental_price_hours = resId?.rental_price_hours;
    ruleForm.image = resId?.image;
    ruleForm.quantity_available = resId?.quantity_available;
    ruleForm.origin = resId?.origin;
    ruleForm.description = resId?.description;
    ruleForm.description_detail = resId?.description_detail;

    fileListImg.value = [
        {
            name: resId.image,
            url: apiImage + resId.image,
        },
    ];
};

onMounted(() => {
    fetchCategory();
    fetchManufactor();
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
                    await updateRentalItem({
                        _id: String(route.params.id),
                        manufactor_id: ruleForm.manufactor_id,
                        category_id: ruleForm.category_id,
                        item_name: ruleForm.item_name,
                        image: ruleForm.image,
                        price: ruleForm.price,
                        price_reduction: ruleForm.price_reduction,
                        rental_price_day: ruleForm.rental_price_day,
                        rental_price_hours: ruleForm.rental_price_hours,
                        quantity_available: ruleForm.quantity_available,
                        origin: ruleForm.origin,
                        description: ruleForm.description,
                        description_detail: ruleForm.description_detail,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/rentalitem");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createRentalItem({
                        manufactor_id: ruleForm.manufactor_id,
                        category_id: ruleForm.category_id,
                        item_name: ruleForm.item_name,
                        image: ruleForm.image,
                        price: ruleForm.price,
                        price_reduction: ruleForm.price_reduction,
                        rental_price_day: ruleForm.rental_price_day,
                        rental_price_hours: ruleForm.rental_price_hours,
                        quantity_available: ruleForm.quantity_available,
                        origin: ruleForm.origin,
                        description: ruleForm.description,
                        description_detail: ruleForm.description_detail,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/rentalitem");
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

<style>
.ck-editor {
    max-height: 500px;
    overflow: auto;
}
</style>
