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
            <el-row :gutter="20" class="chart-row">
                <el-col :span="24">
                    <el-card>
                        <h2>Biểu đồ Doanh Thu Theo Ngày</h2>
                        <el-tooltip
                            content="Số liệu doanh thu theo ngày"
                            placement="top"
                        >
                            <div id="revenueChart" style="height: 300px"></div>
                        </el-tooltip>
                    </el-card>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
</template>

<script setup lang="ts">
import * as echarts from "echarts";
import { ref, onMounted } from "vue";
import { getOverview, getRevenue } from "~/services/statistic.service";

const formatCurrency = (value: any) => {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
    }).format(value);
};

const summaryStats = ref<any>([]);

const revenueData = ref<any>([]);

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
            label: "Số lượng đặt bàn trong ngày",
            value: resOverview.soLuongBanNgay,
        },
        { label: "Số lượng hoá đơn bán", value: resOverview.hoaDonBan },
        { label: "Số lượng hoá đơn nhập", value: resOverview.hoaDonNhap },
        { label: "Tổng số khách hàng", value: resOverview.khachHang },
        {
            label: "Khách hàng mới trong tháng",
            value: resOverview.khachHangMoi,
        },
        { label: "Đơn hàng bị huỷ", value: resOverview.donHuy },
        { label: "Đơn hàng chờ", value: resOverview.donCho },
        { label: "Đơn hàng đang giao", value: resOverview.dangGiao },
        { label: "Đơn hàng hoàn tất", value: resOverview.hoantat },
        { label: "Đơn hàng đổi trả", value: resOverview.doiTra },
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

    const resRevenue = await getRevenue();
    // const dataRevenue = resRevenue.map((value: any) => {
    //     return {
    //         date: value.date,
    //         revenue:
    //             Math.floor(Math.random() * (10000000 - 1000000 + 1)) + 1000000,
    //     };
    // });
    const dataRevenue = Array.from({ length: 19 }, (_, index) => ({
        date: `2024-12-${String(index + 1).padStart(2, "0")}`, //
        revenue: Math.floor(Math.random() * (10000000 - 1000000 + 1)) + 1000000,
    }));
    revenueData.value = dataRevenue;

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
        tooltip: { trigger: "axis" },
    };
    chart.setOption(option);
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
</style>
