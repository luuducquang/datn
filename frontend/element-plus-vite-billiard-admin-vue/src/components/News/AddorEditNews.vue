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
            <el-form-item label="Tiêu đề" prop="title">
                <el-input v-model="ruleForm.title" :rows="4" type="textarea" />
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

            <el-form-item label="Trạng thái" prop="status">
                <el-select
                    v-model="ruleForm.status"
                    placeholder="Vui lòng chọn"
                >
                    <el-option label="Hiện" :value="true" />
                    <el-option label="Ẩn" :value="false" />
                </el-select>
            </el-form-item>

            <el-form-item label="Nội dung" prop="content">
                <ckeditor :editor="editor" v-model="ruleForm.content" />
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
import { News } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { createNew, getbyIdNews, updateNew } from "~/services/news.service";
import axios from "axios";

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const useStore = useUserStore();
const token = useStore?.user?.token;
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

const ruleForm = reactive<News>({
    title: "",
    image: "",
    status: true,
    content: "",
    view: 0,
});

const rules = reactive<FormRules>({
    title: [
        {
            required: true,
            message: "Vui lòng nhập tiêu đề",
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
    status: [
        {
            required: true,
            message: "Vui lòng chọn trạng thái",
            trigger: "blur",
        },
    ],
    content: [
        {
            required: true,
            message: "Vui lòng nhập nội dung",
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

const fetchById = async (id: string) => {
    const resId = await getbyIdNews(id);
    ruleForm.title = resId?.title;
    ruleForm.image = resId?.image;
    ruleForm.status = resId?.status;
    ruleForm.content = resId?.content;
    ruleForm.view = resId?.view;

    fileListImg.value = [
        {
            name: resId.image,
            url: apiImage + resId.image,
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
                    await updateNew({
                        _id: String(route.params.id),
                        title: ruleForm.title,
                        content: ruleForm.content,
                        image: ruleForm.image,
                        view: Number(ruleForm.view),
                        user_id: String(useStore?.user?._id),
                        status: ruleForm.status,
                    });
                    Notification("Cập nhật thành công", "success");
                    router.push("/news");
                } catch (error) {
                    if (axios.isAxiosError(error)) {
                        Notification(error.response?.data.detail, "warning");
                    }
                }
            } else {
                try {
                    await createNew({
                        title: ruleForm.title,
                        content: ruleForm.content,
                        image: ruleForm.image,
                        user_id: String(useStore?.user?._id),
                        status: ruleForm.status,
                    });
                    Notification("Thêm thành công", "success");
                    router.push("/news");
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
