import Cookies from "js-cookie";

export function checkIsAdmin(): boolean {
    const customer = Cookies.get("user");

    if (!customer) return false;

    try {
        const parsed = JSON.parse(customer);
        return parsed.role_name === "ADMIN";
    } catch (error) {
        console.error("Invalid cookie format:", error);
        return false;
    }
}
