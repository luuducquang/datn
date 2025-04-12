<template>
    <el-card class="card_content" v-loading="loading">
        <div class="button_add">
            <el-button @click="handlerAdd" type="primary"
                ><el-icon><CirclePlus /></el-icon
            ></el-button>
        </div>
        <el-table :data="tableData" class="table_content">
            <el-table-column label="STT" align="center" prop="stt" />
            <el-table-column
                label="Tên loại nhân viên"
                align="center"
                prop="employee_type_name"
            />

            <el-table-column align="right">
                <template #default="scope">
                    <el-button
                        size="small"
                        @click="handleEdit(scope.$index, scope.row)"
                    >
                        Edit
                    </el-button>
                    <el-popconfirm
                        confirm-button-text="Yes"
                        cancel-button-text="No"
                        icon-color="#626AEF"
                        title="Bạn có muốn xoá không?"
                        @confirm="() => confirmEvent(scope.row._id)"
                    >
                        <template #reference>
                            <el-button size="small" type="danger">
                                Delete
                            </el-button>
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import { EmployeeTypes } from "~/constant/api";
import {
    deleteEmployeeType,
    getAllEmployeeType,
} from "~/services/employeetype.service";
import router from "~/router";
import { ElMessage } from "element-plus";
import axios from "axios";

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const tableData = ref<EmployeeTypes[]>([]);
const loading = ref(false);

const handleEdit = (index: number, row: EmployeeTypes) => {
    router.push(`/employeetype/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteEmployeeType(Id);
        Notification("Xoá thành công", "success");
        fetchData();
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Notification(error.response?.data.detail, "warning");
        }
    }
};

const fetchData = async () => {
    loading.value = true;
    try {
        const res = await getAllEmployeeType();
        tableData.value = res.map(function (
            value: EmployeeTypes,
            index: number
        ) {
            return {
                stt: index + 1,
                _id: value._id,
                employee_type_name: value.employee_type_name,
            };
        });
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchData();
});

const handlerAdd = () => {
    router.push("/employeetype/add");
};
</script>

<style scoped>
.card_content {
    max-width: 100wh;
}

.button_add {
    display: flex;
    justify-content: flex-end;
    padding: 0 0 10px 7px;
}

.table_content {
    width: 100%;
}

.img_item {
    width: 150px;
    height: 70px;
    object-fit: contain;
}
.name_item {
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rate_product {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 2px;
}

.rate_product_star {
    color: #ffcc00;
    font-size: 20px;
}
</style>
