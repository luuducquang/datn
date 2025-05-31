export const getTodayDate = () => {
    const today = new Date();
    const offset = today.getTimezoneOffset();
    const vietnamTime = new Date(today.getTime() - offset * 60000); 
    return vietnamTime.toISOString().slice(0, 10);
};
