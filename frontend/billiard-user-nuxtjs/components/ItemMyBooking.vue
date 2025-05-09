<template>
    <div v-show="booking.length === 0">
        <h4 class="text-center m-0 pt-3">Bạn chưa đặt bàn lần nào</h4>
        <div class="text-center mt-2">
            <NuxtLink v-if="booking.length === 0" to="/"
                >Quay Lại trang chủ</NuxtLink
            >
        </div>
    </div>
    <div class="accordion" id="accordionExample">
        <div
            class="accordion-item"
            v-for="(value, index) in booking"
            :key="index"
        >
            <h2 class="accordion-header" :id="`heading${value?._id}`">
                <button
                    class="accordion-button collapsed"
                    type="button"
                    data-bs-toggle="collapse"
                    :data-bs-target="`#collapse${value?._id}`"
                    aria-expanded="false"
                    :aria-controls="`collapse${value?._id}`"
                >
                    <span class="fw-bold text-primary">
                        Từ {{ formatTime(value?.start_time) }} đến
                        {{ formatTime(value?.end_time) }}
                    </span>
                    |
                    {{ value?.name }}
                    |
                    {{
                        value?.money_paid > 0
                            ? `${value.money_paid.toLocaleString("de-DE")}đ_`
                            : "0đ"
                    }}
                    <span
                        :class="value?.status ? 'text-success' : 'text-danger'"
                    >
                        {{
                            value?.status ? "Đã thanh toán" : "Chưa thanh toán"
                        }}
                    </span>
                </button>
            </h2>

            <div
                :id="`collapse${value?._id}`"
                class="accordion-collapse collapse"
                :aria-labelledby="`heading${value?._id}`"
                data-bs-parent="#accordionExample"
                style=""
            >
                <div
                    class=""
                    v-for="(item, index) in detailBookingItems"
                    :key="index"
                >
                    <div
                        v-if="item.booking_id === value?._id"
                        class="d-flex mb-3"
                    >
                        <img
                            :src="item.image ? apiImage + item.image : ''"
                            alt="image"
                            width="100"
                            height="100"
                        />
                        <div class="p-3 flex-grow-1">
                            <h5>{{ item.name || "" }}</h5>
                            <div>Số lượng: {{ item.quantity }}</div>
                            <div>
                                Đơn giá:
                                {{
                                    item.unit_price > 0
                                        ? item.unit_price.toLocaleString(
                                              "de-DE"
                                          )
                                        : 0
                                }}đ
                            </div>
                            <div>
                                Tổng giá:
                                {{
                                    (
                                        Number(item.quantity) *
                                        Number(item.unit_price)
                                    ).toLocaleString("de-DE")
                                }}đ
                            </div>
                        </div>
                    </div>
                </div>

                <div class="text-center">
                    <button
                        v-if="
                            new Date(now) < new Date(value?.start_time) &&
                            value.status
                        "
                        class="btn btn-danger mt-2 mb-3"
                        @click="
                            handleCancelBooking(
                                String(value?._id),
                                Number(value?.money_paid)
                            )
                        "
                    >
                        Huỷ đặt bàn
                    </button>
                </div>

                <div
                    v-if="new Date(now) >= new Date(value?.end_time)"
                    class="mt-3 text-center"
                >
                    <h6>Đánh giá dịch vụ</h6>

                    <textarea
                        v-model="reviewText"
                        class="form-control mb-2"
                        placeholder="Nhập nhận xét của bạn"
                        rows="3"
                    ></textarea>

                    <div class="mb-2">
                        <label class="me-2">Chọn số sao:</label>
                        <span
                            v-for="star in 5"
                            :key="star"
                            class="me-1"
                            style="cursor: pointer"
                            @click="selectedStar = star"
                        >
                            <i
                                :class="
                                    star <= selectedStar
                                        ? 'bi bi-star-fill text-warning'
                                        : 'bi bi-star text-muted'
                                "
                            ></i>
                        </span>
                    </div>

                    <div class="mb-2">
                        <input
                            type="file"
                            @change="handleImageUpload"
                            accept="image/*"
                        />
                        <div v-if="previewImage" class="mt-2">
                            <img
                                :src="previewImage"
                                alt="Preview"
                                style="max-width: 100%; max-height: 200px"
                            />
                        </div>
                    </div>

                    <button
                        class="btn btn-primary"
                        @click="submitReview(String(value?._id))"
                    >
                        Gửi đánh giá
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, type Ref, ref } from "vue";
import type { Bookings, BookingItems } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { getDetailBookingItemById } from "~/services/mybooking.service";
import formatTime from "~/store/formatTime";
import Swal from "sweetalert2";
import Cookies from "js-cookie";
import {
    getInformation,
    updateInformation,
} from "~/services/information.service";
import { updateStatusBooking } from "~/services/booking.service";

const props = defineProps<{
    booking: Bookings[];
}>();

const emit = defineEmits(["refreshBooking"]);

const detailBookingItems = ref<BookingItems[]>([]);
const now = new Date();
const reviewText: Ref<string> = ref("");

function handleCancelBooking(bookingId: string, money_paid: number) {
    Swal.fire({
        title: "Bạn có chắc muốn huỷ đặt bàn?",
        text:
            money_paid > 0
                ? `Số tiền đã thanh toán: ${money_paid.toLocaleString(
                      "de-DE"
                  )}đ sẽ được chuyển vào ví của bạn`
                : "Đặt bàn chưa được thanh toán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Có, huỷ ngay",
        cancelButtonText: "Không",
    }).then(async (result) => {
        if (result.isConfirmed) {
            const customerData = Cookies.get("customer");
            if (customerData) {
                const customer = JSON.parse(customerData);
                const dataUser = await getInformation(customer._id);
                await updateInformation({
                    _id: customer._id,
                    username: customer.username,
                    password: customer.password,
                    fullname: customer.fullname,
                    email: customer.email,
                    phone: customer.phone,
                    address: customer.address,
                    avatar: dataUser.avatar,
                    loyalty_points: customer.loyalty_points + money_paid,
                    role_name: customer.role_name,
                });
                await updateStatusBooking(bookingId);
                emit("refreshBooking");
            }
            Swal.fire("Đã huỷ!", "Bàn đã được huỷ thành công.", "success");
        }
    });
}

const selectedStar = ref<number>(0);
const uploadedImage = ref<File | null>(null);
const previewImage = ref<string | null>(null);

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (file) {
    uploadedImage.value = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

const submitReview = async (id: string) => {
  if (!reviewText.value || selectedStar.value === 0) {
    alert('Vui lòng nhập nhận xét và chọn số sao.');
    return;
  }

  const formData = new FormData();
  formData.append('reviewText', reviewText.value);
  formData.append('rating', selectedStar.value.toString());

  if (uploadedImage.value) {
    formData.append('image', uploadedImage.value);
  }

  try {
      console.log(selectedStar.value);

    alert('Đánh giá đã được gửi!');
    reviewText.value = '';
    selectedStar.value = 0;
    uploadedImage.value = null;
    previewImage.value = null;
  } catch (error) {
    console.error('Lỗi khi gửi đánh giá:', error);
    alert('Có lỗi xảy ra. Vui lòng thử lại.');
  }
};

const fetchData = () => {
    setTimeout(async () => {
        const listDetail = await Promise.all(
            props.booking.map(async (value) => {
                const dataDetail = await getDetailBookingItemById(
                    String(value._id)
                );
                return dataDetail;
            })
        );
        detailBookingItems.value = listDetail.flat();
    }, 1000);
};

onMounted(() => {
    fetchData();
});

const cancelOrder = (id: number) => {
    console.log(id);
};
</script>

<style lang="css" scoped>
.btn_cancel {
    border: none;
    padding: 7px 10px;
    background-color: #ff0033;
    outline: none;
    color: #fff;
    margin-bottom: 10px;
}

.btn_cancel:hover {
    opacity: 0.8;
}
</style>
