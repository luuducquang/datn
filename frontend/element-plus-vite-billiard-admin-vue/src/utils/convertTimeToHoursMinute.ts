export function convertTimeToHoursMinute(
    startDateStr: string,
    endDateStr: string
): string {
    const startDate: Date = new Date(startDateStr);
    const endDate: Date = new Date(endDateStr);

    const diffMs: number = endDate.getTime() - startDate.getTime();
    const totalMinutes: number = Math.floor(diffMs / 60000);

    const hours: number = Math.floor(totalMinutes / 60);
    const minutes: number = totalMinutes % 60;

    return `${hours}h${minutes}p`;
}
