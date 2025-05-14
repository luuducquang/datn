export default function ConvertPriceToK(price: number): string {
    if (typeof price !== "number" || isNaN(price)) {
        return "Invalid price";
    }

    const roundedPrice = Math.ceil(price / 1000) * 1000;

    return roundedPrice.toLocaleString("vi-VN", {
        style: "currency",
        currency: "VND",
    });
}
