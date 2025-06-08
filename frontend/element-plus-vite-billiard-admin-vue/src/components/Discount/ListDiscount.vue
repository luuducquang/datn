<template>
    <el-card class="card_content" v-loading="loading">
        <div class="button_add">
            <el-button @click="handlerAdd" type="primary"
                ><el-icon><CirclePlus /></el-icon
            ></el-button>
        </div>
        <el-table :data="tableData" class="table_content">
            <el-table-column label="STT" align="center">
                <template #default="scope">
                    {{ (currentPage - 1) * currentPageSize + scope.$index + 1 }}
                </template>
            </el-table-column>
            <el-table-column label="Mô tả" align="center" prop="decription" />
            <el-table-column label="Code" align="center" prop="code" />
            <el-table-column
                label="Giá trị"
                align="center"
                prop="discount_value"
            >
                <template #default="scope">
                    <span class="name_item"
                        >{{ scope.row.discount_value }}%</span
                    >
                </template>
            </el-table-column>
            <el-table-column label="Số lượng" align="center" prop="quantity" />
            <el-table-column label="Trạng thái" align="center" prop="status">
                <template #default="scope">
                    <div :class="scope.row.status ? 'paid' : 'unpaid'">
                        <p>
                            {{
                                scope.row.status
                                    ? "Đang hoạt động"
                                    : "Đã hết hạn"
                            }}
                        </p>
                    </div>
                </template>
            </el-table-column>
            <el-table-column align="right">
                <template #header>
                    <el-input
                        v-model="search"
                        size="small"
                        placeholder="Nhập thông tin cần tìm"
                    />
                </template>
                <template #default="scope">
                    <el-button
                        size="small"
                        @click="handleEdit(scope.$index, scope.row)"
                    >
                        Sửa
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
                                Xoá
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
                :page-size="currentPageSize"
            />
        </div>
    </el-card>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import debounce from "~/utils/debounce";
import { Discounts } from "~/constant/api";
import { deleteDiscount, searchDiscount } from "~/services/discount.service";
import router from "~/router";
import { ElMessage } from "element-plus";
import axios from "axios";

const search = ref("");
const loading = ref(false);

const tableData = ref<Discounts[]>([]);

const currentPage = ref(1);
const currentPageSize = ref(10);
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
        fetchData(search.value);
    }
});

const handleEdit = (index: number, row: Discounts) => {
    router.push(`/discount/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteDiscount(Id);
        Notification("Xoá thành công", "success");
        fetchData(search.value);
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Notification(error.response?.data.detail, "warning");
        }
    }
};

const fetchData = async (searchTerm = "") => {
    loading.value = true;
    try {
        const payLoad = {
            page: currentPage.value,
            pageSize: currentPageSize.value,
            search_term: searchTerm,
        };
        const res = await searchDiscount(payLoad);
        totalItemPage.value = res.totalItems;
        tableData.value = res.data;
        console.log(res.data);
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    } finally {
        loading.value = false;
    }
};

const debouncedFetchData = debounce(fetchData, 300);

watch(search, (newSearch) => {
    debouncedFetchData(newSearch);
});

onMounted(() => {
    fetchData(search.value);
});

const handlerAdd = () => {
    router.push("/discount/add");
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
    width: 70px;
    height: 70px;
    object-fit: cover;
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
