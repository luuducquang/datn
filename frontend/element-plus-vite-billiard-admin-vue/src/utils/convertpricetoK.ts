export default function ConvertPriceToK(price: number): string {
    if (typeof price !== "number" || isNaN(price)) {
        return "Invalid price";
    }

    if (price < 1) {
        return "0 ₫";
    }

    const roundedPrice = Math.round(price / 1000) * 1000;

    return roundedPrice.toLocaleString("vi-VN", {
        style: "currency",
        currency: "VND",
    });
}
