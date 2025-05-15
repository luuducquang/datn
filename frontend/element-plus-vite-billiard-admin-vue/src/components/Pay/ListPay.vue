<template>
    <el-card class="card_content" v-loading="loading">
        <el-table :data="tableData" class="table_content">
            <el-table-column label="Bắt đầu" align="center" prop="start_time">
                <template #default="scope">
                    <span
                        :title="scope.row.timesession.start_time"
                        class="name_item"
                        >{{
                            convertDate(scope.row.timesession.start_time)
                        }}</span
                    >
                </template>
            </el-table-column>
            <el-table-column label="Kết thúc" align="center" prop="end_time">
                <template #default="scope">
                    <span
                        :title="scope.row.timesession.end_time"
                        class="name_item"
                        >{{ convertDate(scope.row.timesession.end_time) }}</span
                    >
                </template>
            </el-table-column>
            <el-table-column label="Số giờ" align="center" prop="">
                <template #default="scope">
                    <span :title="scope.row.timesession" class="name_item">{{
                        convertTimeToHoursMinute(
                            scope.row.timesession.start_time,
                            scope.row.timesession.end_time
                        )
                    }}</span>
                </template>
            </el-table-column>
            <!-- <el-table-column label="Tiền giờ chơi" align="center" prop="price">
                <template #default="scope">
                    <span
                        :title="scope.row.timesession.price"
                        class="name_item"
                        >{{ ConvertPrice(scope.row.timesession.price) }}</span
                    >
                </template>
            </el-table-column>
            <el-table-column
                label="Tiền dịch vụ"
                align="center"
                prop="total_price"
            >
                <template #default="scope">
                    <span :title="scope.row.total_price" class="name_item">{{
                        ConvertPrice(scope.row.total_price)
                    }}</span>
                </template>
            </el-table-column> -->
            <el-table-column
                label="Tiền thanh toán"
                align="center"
                prop="price_paid"
            >
                <template #default="scope">
                    <span
                        :title="scope.row.timesession.price_paid"
                        class="name_item"
                        >{{
                            ConvertPrice(scope.row.timesession.price_paid)
                        }}</span
                    >
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
                        Info
                    </el-button>
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
    <el-dialog v-model="dialogVisible" title="Thông tin hoá đơn" width="50%">
        <template #default>
            <p>
                Bắt đầu:
                {{ convertDate(dataOrderItem?.timesession?.start_time) }}
            </p>
            <p>
                Kết thúc:
                {{ convertDate(dataOrderItem?.timesession?.end_time) }}
            </p>
            <p>
                Số giờ:
                {{
                    convertTimeToHoursMinute(
                        String(dataOrderItem?.timesession?.start_time),
                        String(dataOrderItem?.timesession?.end_time)
                    )
                }}
            </p>
            <p>
                Tiền giờ chơi:
                {{ ConvertPrice(Number(dataOrderItem?.timesession?.price)) }}
            </p>
            <p>
                Tiền dịch vụ:
                {{ ConvertPrice(Number(dataOrderItem?.total_price)) }}
            </p>
            <p>
                Tiền thanh toán:
                {{
                    ConvertPrice(Number(dataOrderItem?.timesession?.price_paid))
                }}
            </p>
            <el-table
                :data="dataOrderMenuItem"
                v-show="dataOrderMenuItem.length > 0"
                class="table-menu-item"
            >
                <el-table-column label="Hình ảnh" align="center" prop="image">
                    <template #default="scope">
                        <img
                            :src="apiImage + scope.row.menu_items.image"
                            alt="Hình ảnh sản phẩm"
                            class="img-item"
                        />
                    </template>
                </el-table-column>
                <el-table-column
                    label="Sản phẩm"
                    align="center"
                    prop="unit_price"
                >
                    <template #default="scope">
                        <span>{{ scope.row.menu_items.name }}</span>
                    </template>
                </el-table-column>
                <el-table-column
                    label="Số lượng"
                    align="center"
                    prop="quantity"
                >
                    <template #default="scope">
                        <span>{{ scope.row.quantity }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Giá" align="center" prop="unit_price">
                    <template #default="scope">
                        <span>{{ ConvertPrice(scope.row.unit_price) }}</span>
                    </template>
                </el-table-column>
                <el-table-column
                    label="Tổng giá"
                    align="center"
                    prop="total_price"
                >
                    <template #default="scope">
                        <span>{{ ConvertPrice(scope.row.total_price) }}</span>
                    </template>
                </el-table-column>
            </el-table>
        </template>

        <template #footer>
            <el-button @click="dialogVisible = false">Đóng</el-button>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import debounce from "~/utils/debounce";
import { OrderItems, OrderMenuItems } from "~/constant/api";
import { searchOrderItem } from "~/services/orderitem.service";
import { apiImage } from "~/constant/request";
import router from "~/router";
import { ElMessage } from "element-plus";
import { convertDate } from "~/utils/convertDate";
import ConvertPrice from "~/utils/convertprice";
import { convertTimeToHoursMinute } from "~/utils/convertTimeToHoursMinute";
import { getbyOrderId } from "~/services/ordermenuitem.service";
import { number } from "echarts";

const search = ref("");
const loading = ref(false);

const tableData = ref<OrderItems[]>([]);

const currentPage = ref(1);
const currentPageSize = ref(10);
const totalItemPage = ref(0);

const dialogVisible = ref(false);
const dataOrderMenuItem = ref<OrderMenuItems[]>([]);
const dataOrderItem = ref<OrderItems>();

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

watch(currentPage, (payPage: number, oldPage: number) => {
    if (payPage !== oldPage) {
        fetchData(search.value);
    }
});

const handleEdit = async (index: number, row: OrderItems) => {
    dialogVisible.value = true;
    dataOrderItem.value = row;
    const dataDetailMenu = await getbyOrderId(String(row._id));
    dataOrderMenuItem.value = dataDetailMenu;
};

const fetchData = async (searchTerm = "") => {
    loading.value = true;
    try {
        const payLoad = {
            page: currentPage.value,
            pageSize: currentPageSize.value,
            search_term: searchTerm,
        };
        const res = await searchOrderItem(payLoad);
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

watch(search, (paySearch) => {
    debouncedFetchData(paySearch);
});

onMounted(() => {
    fetchData(search.value);
});
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

.img-item {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 8px;
}
</style>
