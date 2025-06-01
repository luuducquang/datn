export default function ConvertPrice(price: number): string {
    if (typeof price !== "number") {
        return "Invalid price";
    }
    if (price < 1) {
        return "0 ₫";
    }
    return price.toLocaleString("vi-VN", {
        style: "currency",
        currency: "VND",
    });
}
