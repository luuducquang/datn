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
                    /> </template></el-table-column
            ><el-table-column label="Tên sản phẩm" align="center" prop="name" />
            <el-table-column
                label="Danh mục"
                align="center"
                prop="categorymenuitem.category_name"
            />
            <el-table-column
                label="Tồn kho"
                align="center"
                prop="stock_quantity"
            >
                <template #default="scope">
                    <span class="name_item">{{
                        scope.row.stock_quantity
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column label="Loại" align="center" prop="is_rental">
                <template #default="scope">
                    <span class="name_item">{{
                        scope.row.is_rental ? "Thuê" : "Bán"
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column
                label="Giá nhập"
                align="center"
                prop="price_origin"
            >
                <template #default="scope">
                    <span class="name_item">{{
                        ConvertPrice(scope.row.price_origin)
                    }}</span>
                </template>
            </el-table-column>
            <el-table-column label="Giá bán" align="center" prop="price">
                <template #default="scope">
                    <span class="name_item">{{
                        ConvertPrice(scope.row.price)
                    }}</span>
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
                        v-if="checkIsAdmin()"
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
            />
        </div>
    </el-card>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { CirclePlus, StarFilled } from "@element-plus/icons-vue";
import debounce from "~/utils/debounce";
import { MenuItems } from "~/constant/api";
import { deleteMenuItem, searchMenuItem } from "~/services/menuitem.service";
import { apiImage } from "~/constant/request";
import router from "~/router";
import { ElMessage } from "element-plus";
import ConvertPrice from "~/utils/convertprice";
import { checkIsAdmin } from "~/utils/checkRole";

const search = ref("");
const loading = ref(false);

const tableData = ref<MenuItems[]>([]);

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

const handleEdit = (index: number, row: MenuItems) => {
    router.push(`/menuitem/edit/${row._id}`);
};

const confirmEvent = async (Id: string) => {
    try {
        await deleteMenuItem(Id);
        Notification("Xoá thành công", "success");
        fetchData(search.value);
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
            pageSize: currentPageSize.value,
            search_term: searchTerm,
        };
        const res = await searchMenuItem(payLoad);
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
    router.push("/menuitem/add");
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
