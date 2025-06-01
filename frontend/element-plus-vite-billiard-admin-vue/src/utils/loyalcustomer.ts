export function DiscountLoyalCustomer(number: number): number {
    if (number < 1) {
        return 0;
    } else if (number <= 5) {
        return 2;
    } else if (number <= 10) {
        return 4;
    } else if (number <= 15) {
        return 8;
    } else if (number <= 20) {
        return 10;
    } else {
        return 15;
    }
}
