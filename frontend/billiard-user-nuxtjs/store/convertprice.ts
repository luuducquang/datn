export default function ConvertPrice(price: number): string {
    if (typeof price !== "number") {
        return "Invalid price";
    }
    return price.toLocaleString("vi-VN", {
        style: "currency",
        currency: "VND",
    });
}
