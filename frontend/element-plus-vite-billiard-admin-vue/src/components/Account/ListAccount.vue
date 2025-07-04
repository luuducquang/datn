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
            <el-table-column label="Ảnh đại diện" align="center" prop="avatar">
                <template #default="scope">
                    <img
                        :src="apiImage + scope.row.avatar"
                        alt="Ảnh đại diện"
                        class="img_item"
                    /> </template
            ></el-table-column>
            <el-table-column label="Email" align="center" prop="email" />
            <el-table-column label="Điểm thành viên" align="center">
                <template #default="{ row }">
                    <span>
                        {{
                            row.loyalty_points
                                ? row.loyalty_points?.toLocaleString("de-DE")
                                : 0
                        }}
                        -
                        <span
                            :style="{
                                color: getMembershipRank(row.loyalty_points)
                                    .color,
                            }"
                        >
                            {{ getMembershipRank(row.loyalty_points).rank }}
                        </span>
                    </span>
                </template>
            </el-table-column>
            <el-table-column label="Số dư ví" align="center" prop="wallet">
                <template #default="scope">
                    <p>{{ ConvertPrice(scope.row.wallet) }}</p>
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
import { Users } from "~/constant/api";
import { deleteAccount, searchAccount } from "~/services/account.service";
import router from "~/router";
import { ElMessage } from "element-plus";
import { apiImage } from "~/constant/request";
import axios from "axios";
import ConvertPrice from "~/utils/convertprice";
import { getMembershipRank } from "~/utils/getMemberShip";

const search = ref("");
const loading = ref(false);

const tableData = ref<Users[]>([]);

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

const handleEdit = (index: number, row: Users) => {
    router.push(`/account/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteAccount(Id);
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
        const res = await searchAccount(payLoad);
        console.log(res);
        totalItemPage.value = res.totalItems;
        tableData.value = res.data;
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
    router.push("/account/add");
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
