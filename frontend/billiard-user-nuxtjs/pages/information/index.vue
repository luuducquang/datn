<template>
    <div class="container mt-3">
        <form @submit.prevent="handleUpdateInformation">
            <div class="mb-3">
                <label class="form-label fw-bold">Xếp hạng hiện tại</label>

                <div class="current-points mb-2">
                    {{ formData.loyalty_points.toLocaleString("de-DE") || 0 }}
                    điểm ({{
                        getMembershipRank(formData.loyalty_points || 0).rank
                    }}) khi mua hàng bạn sẽ được giảm
                    {{
                        getMembershipRank(formData.loyalty_points || 0).voucher
                    }}
                    %
                </div>

                <div class="progress-rank-container">
                    <div class="progress-bar-bg">
                        <div
                            class="progress-bar-fill"
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
                    <div class="rank-labels">
                        <span style="left: 1%">0</span>
                        <span style="left: 25%">500.000</span>
                        <span style="left: 50%">1.000.000</span>
                        <span style="left: 100%">3.000.000</span>
                    </div>
                </div>
            </div>

            <div class="mb-3">
                <label for="avatar" class="form-label fw-bold">Avatar</label>
                <input
                    type="file"
                    class="form-control"
                    id="avatar"
                    @change="handleAvatarChange"
                />
                <img
                    v-if="fileList.length"
                    :src="fileList[0].url"
                    class="img-thumbnail mt-2"
                    alt="avatar"
                />
                <img
                    v-else-if="formData.anhDaiDien"
                    :src="formData.anhDaiDien"
                    class="img-thumbnail mt-2"
                    alt="avatar"
                />
                <p v-if="formData.fileName">{{ formData.fileName }}</p>
            </div>
            <div class="mb-3">
                <label for="hoTen" class="form-label fw-bold">Họ tên</label>
                <input
                    type="text"
                    class="form-control"
                    id="hoTen"
                    v-model="formData.hoTen"
                />
            </div>
            <div class="mb-3">
                <label for="soDienThoai" class="form-label fw-bold"
                    >Số điện thoại</label
                >
                <input
                    type="text"
                    class="form-control"
                    id="soDienThoai"
                    v-model="formData.soDienThoai"
                />
            </div>
            <div class="mb-3">
                <label for="email" class="form-label fw-bold">Email</label>
                <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="formData.email"
                />
            </div>
            <div class="mb-3">
                <label for="matKhau" class="form-label fw-bold">Mật khẩu</label>
                <input
                    type="password"
                    class="form-control"
                    id="matKhau"
                    v-model="formData.matKhau"
                />
            </div>
            <div class="mb-3">
                <label for="diaChi" class="form-label fw-bold">Địa chỉ</label>
                <textarea
                    class="form-control"
                    id="diaChi"
                    v-model="formData.diaChi"
                ></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn_updater">
                Cập nhật
            </button>
        </form>
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
</style>
