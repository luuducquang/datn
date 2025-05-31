<template>
    <div class="container mt-4 mb-5">
        <div class="card shadow-lg p-4 rounded-4 border-0">
            <h4 class="mb-4 fw-bold">Cập nhật thông tin tài khoản</h4>
            <form @submit.prevent="handleUpdateInformation">
                <div class="mb-4">
                    <label class="form-label fw-semibold"
                        >Xếp hạng hiện tại</label
                    >
                    <div class="text-muted small">
                        {{
                            formData.loyalty_points.toLocaleString("de-DE") || 0
                        }}
                        điểm (<strong>{{
                            getMembershipRank(formData.loyalty_points || 0).rank
                        }}</strong
                        >) – Giảm giá:
                        {{
                            getMembershipRank(formData.loyalty_points || 0)
                                .voucher
                        }}%
                    </div>

                    <div
                        class="progress mt-2"
                        style="height: 20px; border-radius: 10px"
                    >
                        <div
                            class="progress-bar"
                            role="progressbar"
                            :style="{
                                width:
                                    getProgressWidth(
                                        formData.loyalty_points || 0
                                    ) + '%',
                                backgroundColor: getMembershipRank(
                                    formData.loyalty_points || 0
                                ).color,
                            }"
                        ></div>
                    </div>
                    <div
                        class="d-flex justify-content-between small mt-1 text-secondary"
                    >
                        <span>0</span>
                        <span>500K</span>
                        <span>1M</span>
                        <span>3M</span>
                    </div>
                </div>

                <div class="mb-4 row align-items-center">
                    <div class="col-md-3 text-center">
                        <img
                            v-if="fileList.length"
                            :src="fileList[0].url"
                            class="img-thumbnail rounded-circle"
                            alt="avatar"
                            style="
                                width: 100px;
                                height: 100px;
                                object-fit: cover;
                            "
                        />
                        <img
                            v-else-if="formData.anhDaiDien"
                            :src="formData.anhDaiDien"
                            class="img-thumbnail rounded-circle"
                            alt="avatar"
                            style="
                                width: 100px;
                                height: 100px;
                                object-fit: cover;
                            "
                        />
                    </div>
                    <div class="col-md-9">
                        <label for="avatar" class="form-label fw-semibold"
                            >Ảnh đại diện</label
                        >
                        <input
                            type="file"
                            class="form-control"
                            id="avatar"
                            @change="handleAvatarChange"
                        />
                        <p
                            v-if="formData.fileName"
                            class="mt-1 small text-secondary"
                        >
                            Đã chọn: {{ formData.fileName }}
                        </p>
                    </div>
                </div>

                <div class="row g-3">
                    <div class="col-md-6">
                        <label for="hoTen" class="form-label fw-semibold"
                            >Họ tên</label
                        >
                        <input
                            type="text"
                            class="form-control"
                            id="hoTen"
                            v-model="formData.hoTen"
                        />
                    </div>

                    <div class="col-md-6">
                        <label for="soDienThoai" class="form-label fw-semibold"
                            >Số điện thoại</label
                        >
                        <input
                            type="text"
                            class="form-control"
                            id="soDienThoai"
                            v-model="formData.soDienThoai"
                        />
                    </div>

                    <div class="col-md-6">
                        <label for="email" class="form-label fw-semibold"
                            >Email</label
                        >
                        <input
                            type="email"
                            class="form-control"
                            id="email"
                            v-model="formData.email"
                        />
                    </div>

                    <div class="col-md-6">
                        <label for="matKhau" class="form-label fw-semibold"
                            >Mật khẩu</label
                        >
                        <input
                            type="password"
                            class="form-control"
                            id="matKhau"
                            v-model="formData.matKhau"
                        />
                    </div>

                    <div class="col-12">
                        <label for="diaChi" class="form-label fw-semibold"
                            >Địa chỉ</label
                        >
                        <textarea
                            class="form-control"
                            id="diaChi"
                            rows="2"
                            v-model="formData.diaChi"
                        ></textarea>
                    </div>
                </div>

                <div class="text-end mt-4">
                    <button
                        type="submit"
                        class="btn btn-primary px-4 py-2 rounded-3 shadow-sm"
                    >
                        Cập nhật thông tin
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";
import axios from "axios";
import {
    getInformation,
    updateInformation,
} from "~/services/information.service";
import { apiImage } from "~/constant/request";
import { uploadImage } from "~/services/upload.service";
import { login } from "~/services/login.service";
import { getMembershipRank } from "~/store/getMemberShip";
import Swal from "sweetalert2";
import { useHead } from "@unhead/vue";

useHead({
    title: "Thông tin tài khoản",
});

interface FormData {
    hoTen: string;
    soDienThoai: string;
    email: string;
    diaChi: string;
    anhDaiDien: string;
    matKhau: string;
    fileName: string;
    loyalty_points: number;
    file: File | null;
}

const router = useRouter();
const fileList = ref<{ url: string }[]>([]);
const formData = reactive<FormData>({
    hoTen: "",
    soDienThoai: "",
    email: "",
    diaChi: "",
    anhDaiDien: "",
    matKhau: "",
    fileName: "",
    loyalty_points: 0,
    file: null as File | null,
});

const getProgressWidth = (points: number): number => {
    if (points <= 500000) {
        return (points / 500000) * 25;
    } else if (points <= 1000000) {
        return 25 + ((points - 500000) / 500000) * 25;
    } else if (points <= 3000000) {
        return 50 + ((points - 1000000) / 2000000) * 50;
    } else {
        return 100;
    }
};

const handleAvatarChange = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            fileList.value = [{ url: e.target?.result as string }];
            formData.anhDaiDien = e.target?.result as string;
            formData.fileName = file.name;
            formData.file = file;
        };
        reader.readAsDataURL(file);
    }
};

const fetchData = async () => {
    const customerData = Cookies.get("customer");
    if (customerData) {
        try {
            const customer = JSON.parse(customerData);
            const dataUser = await getInformation(customer._id);
            formData.hoTen = String(dataUser?.fullname);
            formData.soDienThoai = String(dataUser?.phone);
            formData.email = String(dataUser?.email);
            formData.diaChi = String(dataUser?.address);
            formData.matKhau = String(customer?.password);
            formData.anhDaiDien = apiImage + dataUser?.avatar;
            formData.fileName = "";
            formData.loyalty_points = Number(dataUser?.loyalty_points);
            formData.file = null;
        } catch (error) {
            console.error("Failed to parse customer data from cookies:", error);
            Cookies.remove("customer");
            router.push("/login");
        }
    } else {
        router.push("/login");
    }
};

onMounted(async () => {
    fetchData();
});

const handleUpdateInformation = async () => {
    try {
        const formData2 = new FormData();
        const customerData = Cookies.get("customer");
        if (customerData) {
            const customer = JSON.parse(customerData);
            const dataUser = await getInformation(customer._id);

            if (formData.file) {
                formData2.append("file", formData.file);
                await uploadImage(formData2);
                await updateInformation({
                    _id: customer._id,
                    username: customer.username,
                    password: formData.matKhau,
                    fullname: formData.hoTen,
                    email: formData.email,
                    phone: formData.soDienThoai,
                    address: formData.diaChi,
                    avatar: "/static/uploads/" + formData.fileName,
                    loyalty_points: customer.loyalty_points,
                    wallet: Number(dataUser.wallet),
                    role_name: customer.role_name,
                });
            } else {
                await updateInformation({
                    _id: customer._id,
                    username: customer.username,
                    password: formData.matKhau,
                    fullname: formData.hoTen,
                    email: formData.email,
                    phone: formData.soDienThoai,
                    address: formData.diaChi,
                    avatar: dataUser.avatar,
                    loyalty_points: customer.loyalty_points,
                    wallet: Number(dataUser.wallet),
                    role_name: customer.role_name,
                });
            }
            const res = await login({
                email: String(dataUser.email),
                password: String(formData.matKhau),
            });
            Cookies.set("customer", JSON.stringify(res), { expires: 1 });
            Swal.fire("Thành công", "Cập nhật thông tin thành công", "success");
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            Swal.fire("Lỗi", error.response?.data.detail, "error");
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 600px;
}
.img-thumbnail {
    max-width: 150px;
    height: auto;
}

.btn_updater {
    background-color: var(--color-primary);
    border: none;
    margin-bottom: 15px;
    transition: all 0.5s ease-in-out;
}

.btn_updater:hover {
    transform: scale(1.1);
}

.progress-rank-container {
    width: 100%;
}

.progress-bar-bg {
    background-color: #e0e0e0;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
}

.progress-bar-fill {
    height: 100%;
    transition: width 0.3s ease-in-out;
}

.rank-labels {
    position: relative;
    margin-top: 8px;
    height: 20px;
}

.rank-labels span {
    position: absolute;
    transform: translateX(-50%);
    font-size: 12px;
}

.img-thumbnail {
    transition: 0.3s ease-in-out;
}

.img-thumbnail:hover,
.btn-primary:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

input.form-control,
textarea.form-control {
    border-radius: 10px;
}

label.form-label {
    color: #555;
}

.btn-primary {
    background-color: var(--color-primary);
    border: none;
    transition: 0.3s ease-in-out;
}
</style>
