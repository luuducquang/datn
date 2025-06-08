<template>
    <el-card class="card_content" v-loading="loading">
        <div class="button_add" v-if="checkIsAdmin()">
            <el-button @click="handlerAdd" type="primary"
                ><el-icon><CirclePlus /></el-icon
            ></el-button>
        </div>
        <el-table :data="tableData" class="table_content">
            <el-table-column label="Khách hàng" align="center" prop="name">
                <template #default="scope">
                    <span :title="scope.row.name" class="name_item">{{
                        scope.row.name
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column
                label="Người tạo"
                align="center"
                prop="user_info.fullname"
            />
            <el-table-column
                label="Tổng tiền"
                align="center"
                prop="total_price"
            >
                <template #default="scope">
                    <span
                        >{{
                            parseInt(scope.row.total_price).toLocaleString(
                                "en-US"
                            )
                        }}
                        đ</span
                    >
                </template>
            </el-table-column>
            <el-table-column
                label="Địa chỉ giao"
                align="center"
                prop="address_detail"
            />
            <el-table-column label="Số điện thoại" align="center" prop="phone">
            </el-table-column>
            <el-table-column label="Ngày tạo" align="center" prop="sell_date">
                <template #default="scope">
                    <p>
                        {{ convertDate(scope.row.sell_date) }}
                    </p>
                </template>
            </el-table-column>
            <el-table-column label="Trạng thái" align="center" prop="status">
                <template #default="scope">
                    <div
                        :class="
                            scope.row.status != 'Huỷ đơn' ? 'paid' : 'unpaid'
                        "
                    >
                        <p>
                            {{ scope.row.status }}
                        </p>
                    </div>
                </template>
            </el-table-column>

            <el-table-column label="Thanh toán" align="center" prop="is_paid">
                <template #default="scope">
                    <div :class="scope.row.status ? 'paid' : 'unpaid'">
                        <p>
                            {{
                                scope.row.status
                                    ? "Đã thanh toán"
                                    : "Chưa thanh toán"
                            }}
                        </p>
                    </div>
                </template>
            </el-table-column>

            <el-table-column align="right">
                <template #header>
                    <el-input
                        v-model="search_term"
                        size="small"
                        placeholder="Nhập tên khách hàng"
                    />
                </template>
                <template #default="scope">
                    <el-button
                        v-if="scope.row.status != 'Huỷ đơn'"
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
                        v-if="checkIsAdmin()"
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
            />
        </div>
    </el-card>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useUserStore } from "~/store";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import debounce from "~/utils/debounce";
import { BillSells } from "~/constant/api";
import { deleteBillSell, searchBillSell } from "~/services/billsell.service";
import router from "~/router";
import { ElMessage } from "element-plus";
import { convertDate } from "~/utils/convertDate";
import { checkIsAdmin } from "~/utils/checkRole";

const search_term = ref("");
const loading = ref(false);

const tableData = ref<BillSells[]>([]);

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
        fetchData(search_term.value);
    }
});

const handleEdit = (index: number, row: BillSells) => {
    router.push(`/billsell/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteBillSell(Id);
        Notification("Xoá thành công", "success");
        fetchData(search_term.value);
    } catch (error) {
        console.error("Error deleting =:", error);
        Notification("Lỗi khi xoá =", "error");
    }
};

const fetchData = async (searchTerm = "") => {
    loading.value = true;
    try {
        const payLoad = {
            page: currentPage.value,
            pageSize: 10,
            search_term: searchTerm,
        };
        const res = await searchBillSell(payLoad);
        totalItemPage.value = res.totalItems;
        tableData.value = res.data.reverse();
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    } finally {
        loading.value = false;
    }
};

const debouncedFetchData = debounce(fetchData, 300);

watch(search_term, (newSearch) => {
    debouncedFetchData(newSearch);
});

onMounted(() => {
    fetchData(search_term.value);
});

const handlerAdd = () => {
    router.push("/billsell/add");
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
