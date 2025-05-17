<template>
    <el-card class="card_content" v-loading="loading">
        <el-table :data="tableData" class="table_content">
            <el-table-column label="Bàn số" align="center" prop="table_number">
                <template #default="scope">
                    <span :title="scope.row.table.table_number" class="name_item">{{
                        scope.row.table.table_number
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column label="Bắt đầu" align="center" prop="start_time">
                <template #default="scope">
                    <span :title="scope.row.start_time" class="name_item">{{
                        convertDate(scope.row.start_time)
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column label="Kết thúc" align="center" prop="end_time">
                <template #default="scope">
                    <span :title="scope.row.end_time" class="name_item">{{
                        convertDate(scope.row.end_time)
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column label="Số giờ" align="center" prop="">
                <template #default="scope">
                    <span :title="scope.row" class="name_item">{{
                        convertTimeToHoursMinute(
                            scope.row.start_time,
                            scope.row.end_time
                        )
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column
                label="Khách hàng"
                align="center"
                prop="total_price"
            >
                <template #default="scope">
                    <span :title="scope.row.name" class="name_item">{{
                        scope.row.name
                    }}</span>
                </template>
            </el-table-column>

            <el-table-column
                label="Số điện thoại"
                align="center"
                prop="total_price"
            >
                <template #default="scope">
                    <span :title="scope.row.phone" class="name_item">{{
                        scope.row.phone
                    }}</span>
                </template>
            </el-table-column>

            <el-table-column
                label="Đã thanh toán"
                align="center"
                prop="total_price"
            >
                <template #default="scope">
                    <span
                        v-if="scope.row.status === true"
                        :title="scope.row.money_paid"
                        class="name_item"
                    >
                        {{ ConvertPrice(scope.row.money_paid) }}
                    </span>
                    <div
                        v-else
                        :title="scope.row.money_paid"
                        class="unpaid name_item"
                    >
                        <p>Chưa thanh toán</p>
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
                        Info
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
    <el-dialog v-model="dialogVisible" title="Thông tin hoá đơn" width="50%">
        <template #default>
            <p>
                Bắt đầu:
                {{ convertDate(dataBooking?.start_time) }}
            </p>
            <p>
                Kết thúc:
                {{ convertDate(dataBooking?.end_time) }}
            </p>
            <p>
                Số giờ:
                {{
                    convertTimeToHoursMinute(
                        String(dataBooking?.start_time),
                        String(dataBooking?.end_time)
                    )
                }}
            </p>

            <el-table
                :data="dataOrderMenuItem"
                v-if="dataOrderMenuItem.length > 0"
                class="table-menu-item"
            >
                <el-table-column label="Hình ảnh" align="center" prop="image">
                    <template #default="scope">
                        <img
                            :src="apiImage + scope.row.image"
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
                        <span>{{ scope.row.name }}</span>
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
import { BookingItems, Bookings } from "~/constant/api";
import { apiImage } from "~/constant/request";
import router from "~/router";
import { ElMessage } from "element-plus";
import { convertDate } from "~/utils/convertDate";
import ConvertPrice from "~/utils/convertprice";
import { convertTimeToHoursMinute } from "~/utils/convertTimeToHoursMinute";
import { getbyOrderId } from "~/services/ordermenuitem.service";
import axios from "axios";
import { deleteBooking, searchBooking } from "~/services/booking.service";
import { getBookingItemByIDBooking } from "~/services/bookingitem.service";

const search = ref("");
const loading = ref(false);

const tableData = ref<Bookings[]>([]);

const currentPage = ref(1);
const currentPageSize = ref(10);
const totalItemPage = ref(0);

const dialogVisible = ref(false);
const dataOrderMenuItem = ref<BookingItems[]>([]);
const dataBooking = ref<Bookings>();

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

const handleEdit = async (index: number, row: Bookings) => {
    dialogVisible.value = true;
    dataBooking.value = row;
    const dataDetailMenu = await getBookingItemByIDBooking(String(row._id));
    dataOrderMenuItem.value = dataDetailMenu;
    console.log(dataDetailMenu);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteBooking(Id);
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
        const res = await searchBooking(payLoad);
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

.unpaid {
    background-color: var(--ep-color-danger);
    color: #fff;
    height: 30px;
    border-radius: 10px;
    padding-left: 5px;
    padding-right: 5px;
}

.unpaid p {
    padding: 0;
    margin: 0;
    line-height: 30px;
}
</style>
