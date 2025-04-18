<template>
    <div class="home-product-item">
        <NuxtLink class="linkproduct" :to="`/detail/${product?._id}`">
            <div class="home-product-item_img">
                <img
                    style="min-height: 200px; min-width: 100px"
                    :src="apiImage + product?.image"
                    alt=""
                />
            </div>
            <h4 class="home-product-item_name">{{ product?.item_name }}</h4>
            <span class="decrip-item">{{ product?.description }} </span>
        </NuxtLink>
        <span v-if="isSale" class="banner-sale">NEW</span>
        <span class="sale-up"
            >{{
                (
                    100 -
                    (product?.price_reduction / product?.price) * 100
                ).toFixed()
            }}
            <sup>%</sup>
            <div>Giảm</div></span
        >
        <div class="home-product-item_price">
            <span class="home-product-item_price_current"
                >{{
                    product?.price_reduction > 0
                        ? product?.price_reduction.toLocaleString("DE-de")
                        : ""
                }}<sup>đ</sup></span
            >
            <span class="home-product-item_price_old"
                >{{
                    product?.price > 0
                        ? product?.price.toLocaleString("DE-de")
                        : ""
                }}<sup>đ</sup></span
            >
        </div>
        <!-- <div class="icon_item_product">
            <div class="home-icon-recommend">
                 <span v-if="product?.view > 0">{{
                    product?.view > 0 ? product?.view.toFixed(1) : ""
                }}</span>
                <i
                    v-if="product?.view > 0"
                    title="Đánh giá"
                    class="fa-solid fa-star"
                ></i> 
                 <span v-if="product?.view > 0">|</span> 
                <span v-if="Number(product?.sales) > 0" title="Đã bán" class="fa-solid fa-shop"></span>
                <span title="Đã bán" class="amount-product">{{
                    Number(product?.sales) > 0
                        ? Number(product?.sales).toLocaleString("DE-de")
                        : ""
                }}</span>
            </div>
            <span class="fa-solid fa-truck-fast free-ship"></span>
        </div> -->
        <div class="icon_item_product">
            <div v-if="Number(product?.view) > 0" class="view">
                <i class="fa-solid fa-eye"></i>
                {{
                    Number(product?.view) > 0
                        ? Number(product?.view).toLocaleString("DE-de")
                        : ""
                }}
            </div>
            <div class="country">
                {{ product?.origin }}
            </div>
        </div>
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

<style>
.home-product-item {
    box-sizing: border-box;
    border: solid 1px #dddddd;
    margin: 1% 0;
    background-color: #ffffff;
    overflow: hidden;
    position: relative;
    width: 100%;
    /* box-shadow: rgba(0, 0, 0, 0.4) 0px 0px 10px; */
}

.home-product-item:hover {
    border: solid 1px var(--color-primary-two);
}

.home-product-item a {
    text-decoration: none;
    position: relative;
}

.home-product-item_img img:hover {
    transform: scale(1.1);
}

.home-product-item_img {
    overflow: hidden;
}

.home-product-item_img img {
    width: 100%;
    background-size: cover;
    background-position: center;
    transition: 0.2s ease-in-out;
}

.banner-sale {
    position: absolute;
    background-color: var(--color-sale);
    color: #ffffff;
    padding: 5px;
    top: 10px;
}

.sale-up {
    position: absolute;
    right: 0;
    top: 0;
    background-color: var(--color-saleup);
    padding: 5px;
    color: #ffffff;
    padding: 2px;
    font-size: 11px;
}

/* .sale-up::after {
    content: "";
    position: absolute;
    border-width: 0 17px 6px;
    right: 0;
    bottom: -5.43px;
    border-style: solid;
    border-color: transparent var(--color-saleup) transparent var(--color-saleup);
} */

.home-product-item_name {
    margin: 10px 10px;
    line-height: 1.3rem;
    font-size: 1rem;
    height: 2.6rem;
    overflow: hidden;
    display: block;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    color: black;
    transition: all 0.2s ease;
}

.home-product-item_name:hover {
    color: var(--color-primary-two);
}

.decrip-item {
    margin: 0px 10px;
    line-height: 1.3rem;
    height: 2.6rem;
    overflow: hidden;
    display: block;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    font-size: 0.9rem;
    color: #555555;
}

.decrip-item:hover {
    color: #222222;
}

.home-product-item_price {
    text-align: left;
    margin-left: 10px;
}

.home-product-item_price_current {
    font-size: 1rem;
    color: var(--color-primary-two);
}

.home-product-item_price_old {
    text-decoration: line-through;
    margin-right: 10px;
    color: var(--color-price-old);
    margin-left: 5px;
    font-size: 1rem;
}

.icon_item_product {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0px 10px;
}

.home-icon-recommend {
    display: flex;
    align-items: center;
    gap: 6px;
}

.home-icon-recommend i,
.icon-recommend i {
    font-size: 13px;
}

.view {
    font-size: 15px;
    color: #999999;
    display: flex;
    align-items: center;
    gap: 5px;
}

.country {
    font-size: 15px;
    color: #999999;
    float: right;
    padding: 6px 0;
}

.fa-star {
    color: var(--color-saleup);
}

.fa-shop {
    color: #5f9ea0;
}

.fa-truck-fast {
    color: #63c2b6;
}
</style>
