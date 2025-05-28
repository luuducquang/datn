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
                        class="d-flex mb-3 p-2"
                    >
                        <img
                            :src="item.image ? apiImage + item.image : ''"
                            alt="image"
                            width="100"
                            height="100"
                        />
                        <div class="flex-grow-1">
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
                    <h6 class="m-0 mt-3 mb-3">
                        Lưu ý: bạn huỷ bàn trước 2h khi bắt đầu thì sẽ được hoàn
                        trả tiền vào ví nếu sao thời gian đó tiền sẽ không được
                        hoàn <br />
                        Và đánh giá dịch vụ sau khi đã chơi xong
                    </h6>
                    <button
                        v-if="
                            new Date(now) < new Date(value?.start_time) &&
                            value.status
                        "
                        class="btn btn-danger mb-3"
                        @click="
                            handleCancelBooking(
                                String(value?._id),
                                Number(value?.money_paid),
                                value?.start_time
                            )
                        "
                    >
                        Huỷ đặt bàn
                    </button>
                </div>

                <div
                    v-if="
                        new Date(now) >= new Date(value?.end_time) &&
                        value?.status
                    "
                    class="mt-4 p-4 border rounded shadow-sm bg-light"
                >
                    <template v-if="!rateBooking[index]">
                        <h5 class="text-center mb-3 text-primary fw-bold">
                            Đánh giá dịch vụ
                        </h5>

                        <div class="mb-3">
                            <label class="form-label fw-semibold"
                                >Chọn số sao</label
                            >
                            <div>
                                <span
                                    v-for="star in 5"
                                    :key="star"
                                    class="me-1"
                                    style="cursor: pointer; font-size: 1.5rem"
                                    @click="selectedStar = star"
                                >
                                    <i
                                        :class="
                                            star <= selectedStar
                                                ? 'bi bi-star-fill text-warning'
                                                : 'bi bi-star text-secondary'
                                        "
                                    ></i>
                                </span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label
                                for="reviewText"
                                class="form-label fw-semibold"
                                >Nhận xét của bạn</label
                            >
                            <textarea
                                id="reviewText"
                                v-model="reviewText"
                                class="form-control"
                                placeholder="Nhập nhận xét..."
                                rows="3"
                            ></textarea>
                        </div>

                        <div class="text-center">
                            <button
                                class="btn btn-success px-4"
                                @click="submitReview(String(value?._id))"
                            >
                                <i class="bi bi-send-fill me-1"></i> Gửi đánh
                                giá
                            </button>
                        </div>
                    </template>

                    <template v-else>
                        <h5 class="text-center mb-3 text-success fw-bold">
                            Bạn đã đánh giá
                        </h5>
                        <div
                            class="d-flex align-items-center justify-content-center mb-2"
                        >
                            <span
                                v-for="star in 5"
                                :key="star"
                                style="font-size: 1.5rem"
                            >
                                <i
                                    :class="
                                        star <= rateBooking[index]?.quality
                                            ? 'bi bi-star-fill text-warning'
                                            : 'bi bi-star text-secondary'
                                    "
                                ></i>
                            </span>
                        </div>
                        <p class="text-center fst-italic">
                            "{{ rateBooking[index]?.text }}"
                        </p>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, type Ref, ref } from "vue";
import type { Bookings, BookingItems, RateBookings } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { getDetailBookingItemById } from "~/services/mybooking.service";
import formatTime from "~/store/formatTime";
import Swal from "sweetalert2";
import Cookies from "js-cookie";
import {
    getInformation,
    updateInformation,
    updateInformationWalletPoint,
} from "~/services/information.service";
import { updateStatusBooking } from "~/services/booking.service";
import {
    createRateBooking,
    getRateBookingByIdBooking,
} from "~/services/ratebooking.service";
import { useRouter } from "vue-router";
import { login } from "~/services/login.service";

const props = defineProps<{
    booking: Bookings[];
}>();

const emit = defineEmits(["refreshBooking"]);

const detailBookingItems = ref<BookingItems[]>([]);
const now = new Date();
const reviewText: Ref<string> = ref("");
const selectedStar = ref<number>(5);
const router = useRouter();
const rateBooking = ref<RateBookings[]>([]);

async function handleCancelBooking(
    bookingId: string,
    money_paid: number,
    start_time: Date
) {
    const now = new Date();
    const startTime = new Date(start_time);

    const isBefore2Hours =
        now.getTime() < startTime.getTime() - 2 * 60 * 60 * 1000;

    Swal.fire({
        title: "Bạn có chắc muốn huỷ đặt bàn?",
        text: isBefore2Hours
            ? `Số tiền đã thanh toán: ${money_paid.toLocaleString(
                  "de-DE"
              )}đ sẽ được chuyển vào ví của bạn`
            : "Huỷ bàn sau 2 giờ trước giờ bắt đầu, tiền sẽ không được hoàn",
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

                if (isBefore2Hours && money_paid > 0) {
                    await updateInformationWalletPoint({
                        _id: customer._id,
                        username: customer.username,
                        password: customer.password,
                        fullname: customer.fullname,
                        email: customer.email,
                        phone: customer.phone,
                        address: customer.address,
                        avatar: dataUser.avatar,
                        loyalty_points:
                            Number(dataUser.loyalty_points) -
                            Number(money_paid) * 0.2,
                        wallet: Number(dataUser.wallet) + Number(money_paid),
                        role_name: customer.role_name,
                    });
                } else {
                    await updateInformation({
                        _id: customer._id,
                        username: customer.username,
                        password: customer.password,
                        fullname: customer.fullname,
                        email: customer.email,
                        phone: customer.phone,
                        address: customer.address,
                        avatar: dataUser.avatar,
                        loyalty_points: Number(dataUser.loyalty_points),
                        wallet: Number(dataUser.wallet),
                        role_name: customer.role_name,
                    });
                }

                const res = await login({
                    email: String(dataUser.email),
                    password: String(customer.password),
                });
                Cookies.set("customer", JSON.stringify(res), { expires: 1 });

                await updateStatusBooking(bookingId);
                emit("refreshBooking");
                Swal.fire("Đã huỷ!", "Bàn đã được huỷ thành công.", "success");
            }
        }
    });
}

const submitReview = async (id: string) => {
    if (!reviewText.value || selectedStar.value === 0) {
        Swal.fire(
            "Thông báo!",
            "Vui lòng chọn số sao và nhập đánh giá.",
            "warning"
        );
        return;
    }

    try {
        const customerData = Cookies.get("customer");
        if (customerData) {
            try {
                const customer = JSON.parse(customerData);
                await createRateBooking({
                    booking_id: id,
                    user_id: String(customer._id),
                    quality: Number(selectedStar.value),
                    text: String(reviewText.value),
                });
            } catch (error) {
                console.error(
                    "Failed to parse customer data from cookies:",
                    error
                );
                Cookies.remove("customer");
            }
        } else {
            router.push("/login");
        }

        Swal.fire("Đã huỷ!", "Bàn đã được huỷ thành công.", "success");
        fetchData();
    } catch (error) {
        console.error("Lỗi khi gửi đánh giá:", error);
        alert("Có lỗi xảy ra. Vui lòng thử lại.");
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

        const timeRate = await Promise.all(
            props.booking.map(async (value) => {
                const data = await getRateBookingByIdBooking(String(value._id));
                return data;
            })
        );
        rateBooking.value = timeRate;
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
