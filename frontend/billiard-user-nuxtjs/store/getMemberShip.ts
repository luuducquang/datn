export const getMembershipRank = (points: number) => {
    if (points < 500000) return { rank: "Đồng", color: "#cd7f32", voucher: 0 };
    if (points < 1000000) return { rank: "Bạc", color: "#c0c0c0", voucher: 5 };
    if (points < 3000000)
        return { rank: "Vàng", color: "#e8c021", voucher: 10 };
    return { rank: "Kim Cương", color: "#33FFCC", voucher: 20 };
};
