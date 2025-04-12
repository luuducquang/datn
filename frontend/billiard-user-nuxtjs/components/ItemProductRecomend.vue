<template>
    <div class="product-recommend">
        <NuxtLink :to="`/detail/${product?._id}`">
            <div class="product-recommend-img">
                <img :src="apiImage + product?.image" alt="" />
            </div>
            <span class="product-recommend-price"
                >{{
                    product?.price_reduction > 0
                        ? product?.price_reduction.toLocaleString("de-DE")
                        : ""
                }}<sup>đ</sup></span
            >
            <span class="product-recommend-price-old"
                >{{
                    product?.price > 0
                        ? product?.price.toLocaleString("de-DE")
                        : ""
                }}<sup>đ</sup></span
            >
            <div class="sale-off">
                {{
                    product?.price_reduction > 0 && product.price > 0
                        ? (
                              100 -
                              (product?.price_reduction / product?.price) * 100
                          ).toFixed()
                        : ""
                }}<sup>%</sup>
            </div>
            <div :title="product?.item_name" class="product-recommend-name">
                {{ product?.item_name }}
            </div>
        </NuxtLink>
        <!-- <div class="icon-recommend">
            <span title="Đánh giá" v-if="product?.danhGia > 0">{{
                product?.danhGia > 0 ? product?.danhGia.toFixed() : ""
            }}</span>
            <i
                title="Đánh giá"
                v-if="product?.danhGia > 0"
                class="fa-solid fa-star star-gold"
            ></i>
            <span v-if="product?.danhGia > 0 && product?.luotBan > 0">|</span>
            <span
                title="Lượt bán"
                v-if="product?.luotBan > 0"
                class="fa-solid fa-shop"
            ></span>
            <span
                title="Lượt bán"
                v-if="product?.luotBan > 0"
                class="amount-product"
                >{{ product?.luotBan }}</span
            >
        </div> -->
    </div>
</template>

<script lang="ts" setup>
import { type Product } from "~/constant/api";
import { apiImage } from "~/constant/request";

const props = defineProps<{
    product: Product;
}>();
</script>

<style>
.product-recommend {
    background-color: #fff;
    margin: 10px 5px;
    border: 1px transparent solid;
}

.product-recommend {
    position: relative;
    transition: all 0.1s ease;
}

.product-recommend a {
    text-decoration: none;
}

.product-recommend:hover {
    border: 1px #ff6600 solid;
}

.product-recommend-img img {
    width: 100%;
    transition: 0.2s ease-in-out;
}

.product-recommend-img {
    overflow: hidden;
    margin-bottom: 5px;
}

.product-recommend-img img:hover {
    transform: scale(1.1);
}

.product-recommend-price {
    color: #ff6600;
    margin-left: 5px;
}

.product-recommend-price-old {
    text-decoration: line-through;
    color: #888888;
    float: right;
    margin-right: 5px;
}

.product-recommend-name {
    line-height: 1.3rem;
    height: 2.6rem;
    overflow: hidden;
    display: block;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    color: black;
    margin: 5px;
}

.sale-off {
    display: block;
    flex-direction: column;
    background-color: #ff235c;
    padding: 4px;
    position: absolute;
    right: 0;
    top: 0;
    color: #fff;
    font-size: 12px;
}

.icon-recommend {
    display: flex;
    align-items: center;
    gap: 3px;
}
</style>
