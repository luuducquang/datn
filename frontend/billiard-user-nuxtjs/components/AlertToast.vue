<template>
    <transition name="slide-fade">
        <div
            v-if="props.visible"
            class="alert alert-success alert-dismissible"
            role="alert"
        >
            {{ message }}
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";

const props = defineProps<{
    visible: boolean;
    message: string;
}>();
</script>

<style scoped>
.alert-success {
    position: fixed;
    right: 20px;
    top: 70px;
    z-index: 999;
    transition: all 0.3s ease-in-out;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.5s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
}
</style>
