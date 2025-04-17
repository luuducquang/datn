export const maskEmail = (email: string): string => {
    const [username, domain] = email.split("@");

    if (!username || !domain) {
        throw new Error("Định dạng email không hợp lệ");
    }

    const visiblePart = username.slice(0, 3);
    const maskedPart = "*".repeat(Math.max(username.length - 3, 0));

    return `${visiblePart}${maskedPart}@${domain}`;
};
