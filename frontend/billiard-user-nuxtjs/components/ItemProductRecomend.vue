<template>
    <div class="product-recommend">
        <NuxtLink :to="`/detail/${product?._id}`" class="recommend-link">
            <div class="product-recommend-img">
                <img :src="apiImage + product?.image" alt="Product image" />
                <div v-if="product?.price > 0 && product?.price_reduction > 0" class="sale-badge">
                    -{{
                        (
                            100 -
                            (product?.price_reduction / product?.price) * 100
                        ).toFixed()
                    }}<sup>%</sup>
                </div>
            </div>
            <div class="product-recommend-content">
                <h4 class="product-recommend-name" :title="product?.item_name">
                    {{ product?.item_name }}
                </h4>
                <div class="product-recommend-price-box">
                    <span class="product-recommend-price">
                        {{
                            product?.price_reduction > 0
                                ? product?.price_reduction.toLocaleString("de-DE")
                                : ""
                        }}<sup>đ</sup>
                    </span>
                    <span class="product-recommend-price-old">
                        {{
                            product?.price > 0
                                ? product?.price.toLocaleString("de-DE")
                                : ""
                        }}<sup>đ</sup>
                    </span>
                </div>
            </div>
        </NuxtLink>
    </div>
</template>

<script lang="ts" setup>
import { type Products } from "~/constant/api";
import { apiImage } from "~/constant/request";

const props = defineProps<{
    product: Products;
}>();
</script>


<style scoped>
.product-recommend {
    background-color: #fff;
    border-radius: 10px;
    overflow: hidden;
    margin: 10px 5px;
    border: 1px solid transparent;
    transition: box-shadow 0.2s ease;
}

.product-recommend:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.recommend-link {
    text-decoration: none;
    color: inherit;
    display: block;
}

.product-recommend-img {
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid #f0f0f0;
}

.product-recommend-img img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 10px 10px 0 0;
    transition: transform 0.3s ease;
}

.product-recommend-img:hover img {
    transform: scale(1.05);
}

.sale-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    background-color: var(--color-saleup-two);
    color: #fff;
    font-size: 13px;
    padding: 4px 6px;
    border-radius: 4px;
}

.product-recommend-content {
    padding: 10px;
}

.product-recommend-name {
    font-size: 0.95rem;
    font-weight: 500;
    margin: 0 0 8px;
    line-height: 1.3rem;
    height: 2.6rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    color: #222;
}

.product-recommend-price-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-recommend-price {
    color: var(--color-sale);
    font-weight: bold;
    font-size: 1rem;
}

.product-recommend-price-old {
    text-decoration: line-through;
    color: #999;
    font-size: 0.85rem;
}
</style>
