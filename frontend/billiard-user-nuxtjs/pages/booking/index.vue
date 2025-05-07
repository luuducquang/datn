<template>
    <div class="container py-4">
        <div class="row g-3">
            <div class="col-12 col-lg-9 order-1 order-lg-1">
                <div class="row g-3">
                    <div
                        class="col-6 col-md-6 col-lg-4"
                        v-for="table in tableData"
                        :key="table._id"
                    >
                        <div
                            class="card text-center p-3 position-relative"
                            :class="table.status ? 'bg-danger' : 'bg-success'"
                        >
                            <h1 class="text-white">{{ table.table_number }}</h1>
                            <p class="m-0 text-white">
                                {{
                                    table.status ? "Đang sử dụng" : "Đang trống"
                                }}
                            </p>
                            <button
                                class="btn btn-primary btn-booking"
                                v-if="!table.status"
                                data-bs-toggle="modal"
                                data-bs-target="#exampleModal"
                                @click="openModal(String(table?._id))"
                                href="#exampleModalToggle"
                                role="button"
                            >
                                Đặt bàn
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-12 col-lg-3 order-2 order-lg-2">
                <div class="p-3 border rounded shadow-sm bg-light list-booking">
                    <h4>Danh sách đặt bàn</h4>
                    <div v-if="searchBookingData && searchBookingData.length">
                        <div
                            v-for="(booking, index) in searchBookingData"
                            :key="index"
                            class="mb-3 p-2 border-bottom"
                        >
                            <p class="fw-bold">
                                Bàn: {{ booking.table?.table_number }}
                            </p>
                            <p>Tên: {{ booking.name }}</p>
                            <p>Điện thoại: {{ booking.phone }}</p>
                            <p>Bắt đầu: {{ formatTime(booking.start_time) }}</p>
                            <p>Kết thúc: {{ formatTime(booking.end_time) }}</p>
                            <p class="text-end">
                                {{ getTimeDifference(booking.created_at) }}
                            </p>
                        </div>
                    </div>
                    <div v-else>
                        <p>Không có dữ liệu đặt bàn.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div
        class="modal fade"
        id="exampleModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
        v-show="isModalOpen"
    >
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content shadow-lg border-0">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="exampleModalLabel">
                        Thông tin đặt bàn
                    </h5>
                    <button
                        type="button"
                        class="btn-close btn-close-white"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <form id="booking-form" @submit.prevent="submitBooking">
                        <div class="mb-3">
                            <label
                                for="recipient-name"
                                class="form-label fw-bold"
                                >Tên khách hàng:</label
                            >
                            <input
                                type="text"
                                class="form-control rounded-3"
                                id="recipient-name"
                                v-model="customerName"
                                placeholder="Nhập tên khách hàng"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label
                                for="recipient-phone"
                                class="form-label fw-bold"
                                >Số điện thoại:</label
                            >
                            <input
                                type="tel"
                                class="form-control rounded-3"
                                id="recipient-phone"
                                v-model="customerPhone"
                                placeholder="Nhập số điện thoại"
                                required
                            />
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label
                                    for="start-time"
                                    class="form-label fw-bold"
                                    >Thời gian bắt đầu:</label
                                >
                                <input
                                    type="datetime-local"
                                    class="form-control rounded-3"
                                    id="start-time"
                                    v-model="startTime"
                                    required
                                />
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="end-time" class="form-label fw-bold"
                                    >Thời gian kết thúc:</label
                                >
                                <input
                                    type="datetime-local"
                                    class="form-control rounded-3"
                                    id="end-time"
                                    v-model="endTime"
                                    required
                                />
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Đóng
                    </button>
                    <button
                        type="submit"
                        class="btn btn-success"
                        @click="submitBooking"
                    >
                        Đặt bàn ngay
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { io } from "socket.io-client";
import {
    checkBooking,
    createBooking,
    getAllTable,
    getTableById,
    searchBooking,
} from "~/services/booking.service";
import { type Bookings, type Tables } from "~/constant/api";
import Swal from "sweetalert2";
import axios from "axios";

const getDefaultDateTime = () => {
    const now = new Date();
    const vietnamTime = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    return vietnamTime.toISOString().slice(0, 16);
};

const tableData = ref<Tables[]>([]);
const searchBookingData = ref<Bookings[]>([]);
const loading = ref(true);
const customerName = ref("");
const customerPhone = ref("");
const startTime = ref(getDefaultDateTime());
const endTime = ref(getDefaultDateTime());
const selectedTableId = ref("");
const isModalOpen = ref(false);

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

const openModal = (id: string) => {
    selectedTableId.value = id;
    isModalOpen.value = true;
};

const submitBooking = async () => {
    if (!customerName.value.trim()) {
        Swal.fire("Lỗi", "Vui lòng nhập tên khách hàng!", "error");
        return;
    }
    if (!customerPhone.value.trim()) {
        Swal.fire("Lỗi", "Vui lòng nhập số điện thoại!", "error");
        return;
    }
    if (!startTime.value) {
        Swal.fire("Lỗi", "Vui lòng chọn thời gian bắt đầu!", "error");
        return;
    }
    if (!endTime.value) {
        Swal.fire("Lỗi", "Vui lòng chọn thời gian kết thúc!", "error");
        return;
    }

    try {
        const bookingData = {
            table_id: selectedTableId.value,
            name: customerName.value,
            phone: customerPhone.value,
            start_time: startTime.value,
            end_time: endTime.value,
            status: true,
        };
        const TableInfo = await getTableById(selectedTableId.value);
        if (TableInfo?.status === true) {
            Swal.fire(
                "Thất bại",
                "Bàn này đã có người chơi, vui lòng đặt bàn khác!",
                "warning"
            );
        } else {
            const ischeckBooking = await checkBooking({
                table_id: selectedTableId.value,
                start_time: startTime.value,
                end_time: endTime.value,
            });
            if (ischeckBooking) {
                await createBooking(bookingData);
                closeModal();
                fetchData();
                Swal.fire("Thành công", "Đặt bàn thành công!", "success");
                console.log(startTime.value);
                console.log(endTime.value);
            } else {
                Swal.fire(
                    "Thất bại",
                    "Thời gian này đã có khách đặt!",
                    "warning"
                );
            }
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Swal.fire("Lỗi", error.response?.data.detail, "error");
            // console.log(error.response?.data.detail);
        }
    }
};

const onModalHidden = () => {
    const backdrop = document.querySelector(".modal-backdrop");
    if (backdrop) {
        backdrop.remove();
    }
};

const closeModal = () => {
    const modalElement = document.getElementById("exampleModal");
    const modalInstance = bootstrap?.Modal.getInstance(modalElement);
    modalInstance?.hide();

    isModalOpen.value = false;
    customerName.value = "";
    customerPhone.value = "";
    startTime.value = getDefaultDateTime();
    endTime.value = getDefaultDateTime();
    selectedTableId.value = "";
};

const getTimeDifference = (createdAt: Date) => {
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

const formatTime = (datetime: Date) => {
    const date = new Date(datetime);
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();

    return `${hours}:${minutes} | ${day}/${month}/${year}`;
};

const fetchData = async () => {
    try {
        const res = await getAllTable();
        tableData.value = res;

        const resBooking = await searchBooking({
            page: 1,
            pageSize: 100,
            status: true,
        });
        searchBookingData.value = resBooking?.data.reverse();
    } catch (error) {
        console.error("Error fetching:", error);
        tableData.value = [];
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    await fetchData();
    // const now = DateTime.now().toISO();
    // console.log(now);
    const modalElement = document.getElementById("exampleModal");
    if (modalElement) {
        modalElement.addEventListener("hidden.bs.modal", onModalHidden);
    }
});
</script>

<style lang="css" scoped>
.type {
    background: linear-gradient(90deg, var(--color-primary) 0%, #001815 100%) 0%
        0% no-repeat;
    padding: 10px;
    color: #fff;
    margin-top: 10px;
}

.type a {
    text-decoration: none;
    color: #ddd;
    font-size: 14px;
    text-transform: uppercase;
}

.type i {
    color: #fff;
    font-size: 10px;
    padding: 0 10px;
}
.card {
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
    position: relative;
    overflow: hidden;
}

.card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card:hover h1,
.card:hover p {
    opacity: 0.1;
    transition: opacity 0.2s ease;
}

.btn-booking {
    position: absolute;
    left: 50%;
    transform: translate(-50%, 50%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    background: linear-gradient(90deg, #4caf50, #81c784);
    color: #fff;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    cursor: pointer;
}

.btn-booking:hover {
    background: linear-gradient(90deg, #388e3c, #66bb6a);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
    transform: translate(-50%, 60%) scale(1.05);
}

.card:hover .btn-booking {
    opacity: 1;
    visibility: visible;
}

.card h1 {
    font-size: 3rem;
    font-weight: bold;
    transition: opacity 0.2s ease;
}

.card p {
    font-size: 1.2rem;
    transition: opacity 0.2s ease;
}

.bg-danger {
    background-color: #e74c3c !important;
}

.bg-success {
    background-color: #2ecc71 !important;
}

.btn-success {
    background-color: var(--color-primary) !important;
    border: none;
}

.modal-content {
    border-radius: 10px;
    overflow: hidden;
}

.modal-header {
    background: linear-gradient(90deg, var(--color-primary), #0056b3);
}

.btn-close-white {
    filter: brightness(0) invert(1);
}

.modal-body {
    background-color: #f8f9fa;
}

.modal-footer {
    border-top: none;
}

.form-control {
    background-color: #fff;
    border: 1px solid #ced4da;
    box-shadow: none;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.form-control:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    border-color: var(--color-primary);
}

.list-booking {
    max-height: 560px;
    overflow-y: scroll;
}
</style>
