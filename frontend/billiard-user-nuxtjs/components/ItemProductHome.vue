<template>
    <div class="product-card">
        <NuxtLink class="product-link" :to="`/detail/${product?._id}`">
            <div class="product-image">
                <img :src="apiImage + product?.image" alt="Product image" />
                <span v-if="isSale" class="label-new">NEW</span>
                <span class="label-discount">
                    {{
                        (
                            100 -
                            (product?.price_reduction / product?.price) * 100
                        ).toFixed()
                    }}<sup>%</sup> Giảm
                </span>
            </div>
            <div class="product-content">
                <h4 class="product-name">{{ product?.item_name }}</h4>
                <p class="product-description">{{ product?.description }}</p>
                <div class="product-price">
                    <span class="price-sale"
                        >{{ product?.price_reduction.toLocaleString("DE-de")
                        }}<sup>đ</sup></span
                    >
                    <span class="price-original"
                        >{{ product?.price.toLocaleString("DE-de")
                        }}<sup>đ</sup></span
                    >
                </div>
                <div class="product-meta">
                    <div class="view" v-if="Number(product?.view) > 0">
                        <i class="fa-solid fa-eye"></i>
                        {{ Number(product?.view).toLocaleString("DE-de") }}
                    </div>
                    <div class="origin">{{ product?.origin }}</div>
                </div>
            </div>
        </NuxtLink>
    </div>
</template>

<script lang="ts" setup>
import { type Product } from "~/constant/api";
import { apiImage } from "~/constant/request";

const props = defineProps<{
    product: Product;
    isSale: boolean;
}>();
</script>

<style scoped>
.product-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.product-link {
    color: inherit;
    text-decoration: none;
}

.product-image {
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid #eee;
}

.product-image img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.product-image:hover img {
    transform: scale(1.05);
}

.label-new {
    position: absolute;
    top: 10px;
    left: 10px;
    background: var(--color-sale);
    color: #fff;
    font-size: 12px;
    padding: 4px 6px;
    border-radius: 4px;
}

.label-discount {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--color-saleup);
    color: #fff;
    font-size: 12px;
    padding: 4px 6px;
    border-radius: 4px;
}

.product-content {
    padding: 12px;
}

.product-name {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 5px;
    color: #222;
    height: 2.4rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
}

.product-description {
    font-size: 0.875rem;
    color: #666;
    height: 2.4rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    margin-bottom: 8px;
}

.product-price {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.price-sale {
    color: var(--color-primary);
    font-weight: bold;
    font-size: 1rem;
}

.price-original {
    text-decoration: line-through;
    font-size: 0.9rem;
    color: #999;
}

.product-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #999;
}

.view,
.origin {
    display: flex;
    align-items: center;
    gap: 4px;
}
</style>
