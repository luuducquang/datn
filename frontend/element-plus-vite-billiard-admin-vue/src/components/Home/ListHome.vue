<template>
    <el-card class="card_content" v-loading="loading">
        <el-row :gutter="20">
            <el-col
                class="container_col"
                v-for="table in tableData"
                :key="table._id"
                :span="6"
                @click="handleEdit(String(table._id))"
            >
                <div
                    class="table-card mt-3"
                    :class="table.status ? 'in-use' : 'available'"
                >
                    <h2>Bàn {{ table.table_number }}</h2>
                    <p class="status-text">
                        {{ table.status ? "Đang sử dụng" : "Đang trống" }}
                    </p>
                    <p>{{ table.description }}</p>
                </div>
            </el-col>
        </el-row>

        <el-row :gutter="20" class="booking-row">
            <el-col :span="24">
                <el-card>
                    <h2>Danh Sách Đặt Bàn</h2>
                    <el-table
                        v-if="searchBookingData.length > 0"
                        :data="searchBookingData"
                        class="table_booking"
                    >
                        <el-table-column
                            label="Số Bàn"
                            prop="tableNumber"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="Tên Khách"
                            prop="customerName"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="Số Điện Thoại"
                            prop="customerPhone"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="Thời Gian Bắt Đầu"
                            prop="startTime"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="Thời Gian Kết Thúc"
                            prop="endTime"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="Đã đặt"
                            prop="timeBefore"
                            width="100"
                            align="center"
                        ></el-table-column>
                        <el-table-column label="Thao tác" align="center">
                            <template #default="{ row }">
                                <el-popconfirm
                                    confirm-button-text="Yes"
                                    cancel-button-text="No"
                                    icon-color="#626AEF"
                                    title="Bạn có muốn huỷ không?"
                                    @confirm="confirmEvent(row.id)"
                                >
                                    <template #reference>
                                        <el-button
                                            v-show="
                                                isCurrentTimeWithinRange(
                                                    row.start_time,
                                                    row.end_time
                                                ) === false
                                            "
                                            class="btn_cancelBooking"
                                            >Huỷ bàn</el-button
                                        >
                                    </template>
                                </el-popconfirm>
                            </template>
                        </el-table-column>
                    </el-table>
                    <p v-if="searchBookingData.length < 0">
                        Không có người đặt bàn
                    </p>
                </el-card>
            </el-col>
        </el-row>
    </el-card>
</template>

<script lang="ts" setup>
import { getAllTable } from "~/services/home.service";
import { Bookings, Tables } from "~/constant/api";
import { io } from "socket.io-client";
import { ref, onMounted } from "vue";
import router from "~/router";
import {
    getBookingAvailable,
    setFalseStatusBooking,
} from "~/services/booking.service";
import { convertDate } from "~/utils/convertDate";

const tableData = ref<Tables[]>([]);
const loading = ref(true);
const searchBookingData = ref<any>([]);

const socket = io("http://127.0.0.1:8000/", {
    transports: ["websocket"],
});

socket.on("connect", () => {
    console.log("Connected to WebSocket server!");
});

socket.on("connect_error", (error) => {
    console.error("Connection failed:", error);
});

socket.on("table_status_updated", (data) => {
    const table = tableData.value.find((t) => t._id === data._id);
    if (table) {
        table.status = data.status;
    }
});

const handleEdit = (id: string) => {
    router.push(`/${id}`);
};

const isCurrentTimeWithinRange = (
    startTime: string | Date,
    endTime: string | Date
) => {
    const start = new Date(startTime);
    const end = new Date(endTime);

    const currentTime = new Date();

    return currentTime >= start && currentTime <= end;
};

const getTimeDifference = (createdAt: Date | string) => {
    const createdDate: any = new Date(createdAt);
    const currentDate: any = new Date();
    const differenceMs = currentDate - createdDate;
    const differenceMinutes = Math.floor(differenceMs / (1000 * 60));
    if (differenceMinutes < 60) {
        return `${differenceMinutes} phút trước`;
    } else if (differenceMinutes < 1440) {
        const hours = Math.floor(differenceMinutes / 60);
        return `${hours} giờ trước`;
    } else {
        const days = Math.floor(differenceMinutes / 1440);
        return `${days} ngày trước`;
    }
};

const confirmEvent = async (id: string) => {
    try {
        await setFalseStatusBooking(id);
        fetchData();
    } catch (error) {
        console.error("Lỗi khi hủy bàn:", error);
        alert("Có lỗi xảy ra khi hủy bàn.");
    }
};

const fetchData = async () => {
    try {
        const res = await getAllTable();
        tableData.value = res;
        const resBooking = await getBookingAvailable();
        const formattedBookingList = resBooking.map((booking: any) => {
            return {
                id: booking._id,
                tableNumber: booking?.table?.table_number,
                customerName: booking.name,
                customerPhone: booking.phone,
                startTime: convertDate(booking.start_time),
                endTime: convertDate(booking.end_time),
                timeBefore: getTimeDifference(booking.created_at),
            };
        });
        searchBookingData.value = formattedBookingList.reverse();
        console.log(searchBookingData.value);
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
</script>

<style scoped>
.grid-content {
    height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
    cursor: pointer;
}

.grid-content > h1 {
    font-size: 50px;
}

/* .grid-content > p {
    margin: 0;
} */

.ep-bg-purple {
    background-color: #3d4d44;
}
.ep-bg-green {
    background-color: #27ae60;
    height: 100%;
}
.status-in-use {
    color: #ff3333;
}
.status-available {
    color: #00bb00;
}
.active_table {
    background-color: #000000;
}

/* bookingtable */
.stat-label {
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.stat-value {
    font-size: 16px;
    font-weight: bold;
    color: #409eff;
    text-align: center;
}

.summary-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 120px;
}

.summary-row {
    margin-bottom: 20px;
}

.chart-row {
    margin-top: 20px;
}

.booking-row {
    margin-top: 20px;
}
.btn_cancelBooking {
    width: 50px;
}

.table_booking {
    width: 100%;
    max-height: 700px;
    overflow-y: auto;
}

/*  */

.container_col {
    display: grid;
}

.table-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition:
        transform 0.2s,
        box-shadow 0.2s;
    text-align: center;
    cursor: pointer;
}

.table-card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.table-card h2 {
    margin: 0;
    font-size: 22px;
    color: #333;
}

.status-text {
    margin-top: 10px;
    font-size: 16px;
    font-weight: 600;
}

.in-use {
    background-color: #ffe5e5;
    border-left: 6px solid #e74c3c;
}

.in-use .status-text {
    color: #e74c3c;
}

.available {
    background-color: #b5f3b5;
    border-left: 6px solid #2ecc71;
}

.available .status-text {
    color: #2ecc71;
}
</style>
