export function convertDate(inputDate: string | Date | any) {
    const date = new Date(inputDate);

    if (isNaN(date.getTime())) {
        throw new Error("Invalid date format");
    }

    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();

    return ` ${day}/${month}/${year} | ${hours}:${minutes}`;
}
