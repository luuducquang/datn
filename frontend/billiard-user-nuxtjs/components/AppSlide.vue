<template>
    <div>
        <div
            id="carouselExampleIndicators"
            class="carousel slide"
            data-bs-ride="carousel"
        >
            <div class="carousel-indicators">
                <button
                    v-for="(slide, index) in listSlide"
                    :key="index"
                    type="button"
                    :data-bs-target="'#carouselExampleIndicators'"
                    :data-bs-slide-to="index"
                    :class="{ active: index === 0 }"
                    :aria-label="'Slide ' + (index + 1)"
                ></button>
            </div>
            <div class="carousel-inner">
                <div
                    v-for="(slide, index) in listSlide"
                    :key="index"
                    :class="{ 'carousel-item': true, active: index === 0 }"
                >
                    <img
                        :src="apiImage + slide.image"
                        class="d-block w-100"
                        alt="Slide Image"
                    />
                </div>
            </div>
            <button
                class="carousel-control-prev"
                type="button"
                data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev"
            >
                <span
                    class="carousel-control-prev-icon"
                    aria-hidden="true"
                ></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button
                class="carousel-control-next"
                type="button"
                data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next"
            >
                <span
                    class="carousel-control-next-icon"
                    aria-hidden="true"
                ></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { type Banner } from "~/constant/api";
import { apiImage } from "~/constant/request";
import { getAllImagesBanner } from "~/services/banner.service";

const listSlide = ref<Banner[]>([]);

const fetchSlides = async () => {
    try {
        const res = await getAllImagesBanner();
        listSlide.value = res;
    } catch (error) {
        console.error("Failed to fetch slides:", error);
    }
};

onMounted(() => {
    fetchSlides();
});
</script>
