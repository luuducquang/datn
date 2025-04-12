<template>
    <el-card class="card_content" v-loading="loading">
        <div class="button_add">
            <el-button @click="handlerAdd" type="primary"
                ><el-icon><CirclePlus /></el-icon
            ></el-button>
        </div>
        <el-table :data="tableData" class="table_content">
            <el-table-column label="Hình ảnh" align="center" prop="image">
                <template #default="scope">
                    <img
                        :src="apiImage + scope.row.image"
                        alt="Hình ảnh sản phẩm"
                        class="img_item"
                    /> </template
            ></el-table-column>
            <el-table-column label="Mô tả" align="center" prop="description" />

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
        <div class="pagination_wrapper">
            <el-pagination
                background
                layout="prev, pager, next"
                v-model:current-page="currentPage"
                :total="totalItemPage"
            />
        </div>
    </el-card>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import { apiImage } from "~/constant/request";
import { Banner } from "~/constant/api";
import { deleteBanner, searchBanner } from "~/services/banner.service";
import router from "~/router";
import { ElMessage } from "element-plus";

const tableData = ref<Banner[]>([]);
const loading = ref(false);

const currentPage = ref(1);
const totalItemPage = ref(0);

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

watch(currentPage, (newPage: number, oldPage: number) => {
    if (newPage !== oldPage) {
        fetchData();
    }
});

const handleEdit = (index: number, row: Banner) => {
    router.push(`/banner/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteBanner(Id);
        Notification("Xoá thành công", "success");
        fetchData();
    } catch (error) {
        console.error("Error deleting =:", error);
        Notification("Lỗi khi xoá =", "error");
    }
};

const fetchData = async () => {
    loading.value = true;
    try {
        const payLoad = {
            page: currentPage.value,
            pageSize: 10,
        };
        const res = await searchBanner(payLoad);
        totalItemPage.value = res.totalItems;
        tableData.value = res.data;
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
    router.push("/banner/add");
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

.pagination_wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 10px 0;
}
</style>
