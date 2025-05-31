<template>
    <el-container>
        <el-main>
            <el-row :gutter="20" class="summary-row">
                <el-col
                    :span="6"
                    v-for="stat in summaryStats"
                    :key="stat.label"
                >
                    <el-card class="summary-card">
                        <h2 class="stat-label">{{ stat.label }}</h2>
                        <p class="stat-value">{{ stat.value }}</p>
                    </el-card>
                </el-col>
            </el-row>
            <el-row :gutter="20" class="chart-row" style="margin-top: 20px">
                <el-col :span="24">
                    <el-card>
                        <h2>Sản phẩm sắp hết hàng (dưới 10 sản phẩm)</h2>
                        <div class="table-scroll-wrapper">
                            <el-table
                                class="low-stock-card"
                                :data="lowStockProducts"
                            >
                                <el-table-column
                                    label="Ảnh"
                                    width="200"
                                    header-align="center"
                                    align="center"
                                >
                                    <template #default="{ row }">
                                        <el-image
                                            style="width: 100px; height: 100px"
                                            :src="apiImage + row.image"
                                            fit="contain"
                                        />
                                    </template>
                                </el-table-column>

                                <el-table-column
                                    prop="name"
                                    label="Tên sản phẩm"
                                />

                                <el-table-column
                                    prop="quantity"
                                    label="Tồn kho"
                                    header-align="center"
                                    align="center"
                                />

                                <el-table-column prop="price" label="Giá">
                                    <template #default="{ row }">
                                        <p>{{ formatCurrency(row.price) }}</p>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
            <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>
                            Biểu đồ giờ chơi:
                            {{
                                Math.round(totalPlaytimeMonth)?.toLocaleString(
                                    "de-DE"
                                )
                            }}
                            giờ
                        </h2>
                        <el-tooltip content="" placement="top" disabled>
                            <div id="playTimeChart" style="height: 300px"></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row>
            <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>
                            Biểu đồ doanh thu 7 ngày gần nhất:
                            {{ ConvertPrice(Number(totalRevenueWeek)) }}
                        </h2>
                        <el-tooltip content="" placement="top" disabled>
                            <div
                                id="revenueChartWeek"
                                style="height: 300px"
                            ></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row>
            <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>
                            Biểu đồ doanh thu theo tháng:
                            {{ ConvertPrice(Number(totalRevenueMonth)) }}
                        </h2>
                        <el-tooltip content="" placement="top" disabled>
                            <div id="revenueChart" style="height: 300px"></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row>
            <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>
                            Biểu đồ doanh thu năm {{ yearRevenue }}:
                            {{ ConvertPrice(Number(totalRevenueYear)) }}
                        </h2>
                        <el-tooltip content="" placement="top" disabled>
                            <div
                                id="revenueChartYear"
                                style="height: 300px"
                            ></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row>
            <!-- <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>Biểu đồ tồn kho sản phẩm</h2>
                        <el-tooltip content="" placement="top" disabled>
                            <div
                                id="inventoryItemChart"
                                style="height: 300px"
                            ></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row> -->
        </el-main>
    </el-container>
</template>

<script setup lang="ts">
import * as echarts from "echarts";
import { ref, onMounted } from "vue";
import {
    getInventoryItem,
    getLowStock,
    getOverview,
    getPlaytime,
    getRevenue,
    getRevenueWeek,
    getRevenueYear,
} from "~/services/statistic.service";
import ConvertPrice from "~/utils/convertprice";
import { apiImage } from "~/constant/request";

const formatCurrency = (value: any) => {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
    }).format(value);
};

const summaryStats = ref<any>([]);

const revenueDataWeek = ref<any>([]);
const totalRevenueWeek = ref(0);

const revenueData = ref<any>([]);
const totalRevenueMonth = ref(0);

const revenueDataYear = ref<any>([]);
const totalRevenueYear = ref(0);
const yearRevenue = ref(0);

const playTimeData = ref<any>([]);
const totalPlaytimeMonth = ref(0);

const inventoryData = ref<any>([]);

const lowStockProducts = ref([]);

onMounted(() => {
    Fetchdata();
});

const Fetchdata = async () => {
    const resOverview = await getOverview();
    const dataOverview = [
        { label: "Tổng số bàn", value: resOverview.tongSoBan },
        { label: "Bàn đang sử dụng", value: resOverview.banDangDung },
        { label: "Bàn trống", value: resOverview.banTrong },
        {
            label: "Đặt bàn trong ngày",
            value: resOverview.soLuongBookingHomNay,
        },
        {
            label: "Đặt bàn trong tháng",
            value: resOverview.soLuongBookingTrongThang,
        },
        { label: "Tổng hoá đơn bán", value: resOverview.hoaDonBan },
        { label: "Tổng hoá đơn nhập", value: resOverview.hoaDonNhap },
        { label: "Tổng hoá đơn giờ chơi", value: resOverview.hoaDonGioChoi },
        {
            label: "Tổng giờ chơi",
            value: Math.ceil(Number(resOverview.tongGioChoi)),
        },
        { label: "Tổng số khách hàng", value: resOverview.khachHang },
        {
            label: "Khách hàng mới trong tháng",
            value: resOverview.khachHangMoi,
        },
        { label: "Tổng đơn hàng bị huỷ", value: resOverview.donHuy },
        { label: "Tổng đơn hàng chờ", value: resOverview.donCho },
        { label: "Tổng đơn hàng đang giao", value: resOverview.dangGiao },
        { label: "Tổng đơn hàng hoàn tất", value: resOverview.hoantat },
        { label: "Tổng đơn hàng đổi trả", value: resOverview.doiTra },
        { label: "Tổng lượt xem sản phẩm", value: resOverview.luotXem },
        {
            label: "Tổng tiền nhập",
            value: formatCurrency(resOverview.tienNhap),
        },
        {
            label: "Tổng doanh thu",
            value: formatCurrency(resOverview.doanhThu),
        },
    ];
    summaryStats.value = dataOverview;

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

    const resRevenue = await getRevenue();
    const dataRevenue = resRevenue?.daily_revenue.map((value: any) => {
        return {
            date: value.date,
            revenue: value.revenue,
        };
    });
    revenueData.value = dataRevenue;
    totalRevenueMonth.value = resRevenue?.total_revenue;

    const chart = echarts.init(document.getElementById("revenueChart"));
    const option = {
        xAxis: {
            type: "category",
            data: revenueData.value.map((item: any) => item.date),
        },
        yAxis: { type: "value" },
        series: [
            {
                data: revenueData.value.map((item: any) => item.revenue),
                type: "line",
                smooth: true,
            },
        ],
        tooltip: {
            trigger: "axis",
            formatter: function (params: any) {
                const item = params[0];
                return `${item.axisValue}<br/>Doanh thu: ${ConvertPrice(item.data)}`;
            },
        },
    };
    chart.setOption(option);

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    const resPlaytime = await getPlaytime();
    const dataPlaytime = resPlaytime?.daily_revenue.map((value: any) => {
        return {
            date: value.date,
            hours_played: Math.ceil(value.hours_played),
        };
    });
    playTimeData.value = dataPlaytime;
    totalPlaytimeMonth.value = resPlaytime?.total_revenue;

    const chartPlayTime = echarts.init(
        document.getElementById("playTimeChart")
    );
    const optionPlayTime = {
        xAxis: {
            type: "category",
            data: playTimeData.value.map((item: any) => item.date),
        },
        yAxis: { type: "value" },
        series: [
            {
                data: playTimeData.value.map((item: any) => item.hours_played),
                type: "line",
                smooth: true,
            },
        ],
        tooltip: {
            trigger: "axis",
            formatter: function (params: any) {
                const item = params[0];
                return `${item.axisValue}<br/>Giờ chơi: ${item.data} giờ`;
            },
        },
    };
    chartPlayTime.setOption(optionPlayTime);

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    const resInventory = await getInventoryItem();
    const dataInventory = resInventory.map((value: any) => {
        return {
            product_name: value.product_name,
            quantity: value.quantity,
        };
    });
    inventoryData.value = dataInventory;

    const chartImventory = echarts.init(
        document.getElementById("inventoryItemChart")
    );
    const optionImventory = {
        xAxis: {
            type: "category",
            data: inventoryData.value.map((item: any) => item.product_name),
            axisLabel: {
                show: false,
            },
        },
        yAxis: {
            type: "value",
        },
        series: [
            {
                data: inventoryData.value.map((item: any) => item.quantity),
                type: "line",
                smooth: true,
            },
        ],
        tooltip: {
            trigger: "axis",
            formatter: function (params: any) {
                const item = params[0];
                return `${item.axisValue}<br/>Tồn kho: ${item.data}`;
            },
        },
    };
    chartImventory.setOption(optionImventory);

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    const resLowStock = await getLowStock();
    lowStockProducts.value = resLowStock;

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    const resRevenueWeek = await getRevenueWeek();
    const dataRevenueWeek = resRevenueWeek?.daily_revenue.map((value: any) => {
        return {
            date: value.date,
            revenue: value.revenue,
        };
    });
    revenueDataWeek.value = dataRevenueWeek;
    totalRevenueWeek.value = resRevenueWeek?.total_revenue;

    const chartWeek = echarts.init(document.getElementById("revenueChartWeek"));
    const optionWeek = {
        xAxis: {
            type: "category",
            data: revenueDataWeek.value.map((item: any) => item.date),
        },
        yAxis: { type: "value" },
        series: [
            {
                data: revenueDataWeek.value.map((item: any) => item.revenue),
                type: "line",
                smooth: true,
            },
        ],
        tooltip: {
            trigger: "axis",
            formatter: function (params: any) {
                const item = params[0];
                return `${item.axisValue}<br/>Doanh thu: ${ConvertPrice(item.data)}`;
            },
        },
    };
    chartWeek.setOption(optionWeek);

    // aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    const resRevenueYear = await getRevenueYear();
    const dataRevenueYear = resRevenueYear?.monthly_revenue.map(
        (value: any) => {
            return {
                date: "Tháng " + value.month,
                revenue: value.revenue,
            };
        }
    );
    revenueDataYear.value = dataRevenueYear;
    totalRevenueYear.value = resRevenueYear?.total_year_revenue;
    yearRevenue.value = resRevenueYear?.year;

    const chartYear = echarts.init(document.getElementById("revenueChartYear"));
    const optionYear = {
        xAxis: {
            type: "category",
            data: revenueDataYear.value.map((item: any) => item.date),
        },
        yAxis: { type: "value" },
        series: [
            {
                data: revenueDataYear.value.map((item: any) => item.revenue),
                type: "line",
                smooth: true,
            },
        ],
        tooltip: {
            trigger: "axis",
            formatter: function (params: any) {
                const item = params[0];
                return `${item.axisValue}<br/>Doanh thu: ${ConvertPrice(item.data)}`;
            },
        },
    };
    chartYear.setOption(optionYear);
};
</script>

<style scoped>
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

.low-stock-card {
    height: 530px;
    overflow: auto;
    display: flex;
    flex-direction: column;
}

.low-stock-card h2 {
    margin-bottom: 10px;
}

.table-scroll-wrapper {
    flex: 1;
    overflow-y: auto;
}
</style>
