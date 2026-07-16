st.subheader("📊 So sánh hai phương thức vay")

# =============================
# TÍNH DƯ NỢ GIẢM DẦN
# =============================

goc_thang = so_tien / thoi_han
du_no = so_tien
tong_lai_giam = 0

for i in range(thoi_han):
    lai = du_no * lai_thang
    tong_lai_giam += lai
    du_no -= goc_thang


# =============================
# TÍNH TRẢ GÓP ĐỀU
# =============================

tien_tra = so_tien * lai_thang * (1 + lai_thang) ** thoi_han
tien_tra /= ((1 + lai_thang) ** thoi_han - 1)

du_no = so_tien
tong_lai_deu = 0

for i in range(thoi_han):
    lai = du_no * lai_thang
    goc = tien_tra - lai
    tong_lai_deu += lai
    du_no -= goc


# =============================
# BẢNG SO SÁNH
# =============================

bang_ss = pd.DataFrame({
    "Phương thức": [
        "Dư nợ giảm dần",
        "Trả góp đều"
    ],
    "Tổng tiền lãi (VNĐ)": [
        round(tong_lai_giam),
        round(tong_lai_deu)
    ],
    "Tổng thanh toán (VNĐ)": [
        round(so_tien + tong_lai_giam),
        round(so_tien + tong_lai_deu)
    ]
})

st.dataframe(bang_ss, use_container_width=True)

# =============================
# HIỂN THỊ METRIC
# =============================

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "💵 Dư nợ giảm dần",
        f"{tong_lai_giam:,.0f} VNĐ"
    )

with col2:
    st.metric(
        "💳 Trả góp đều",
        f"{tong_lai_deu:,.0f} VNĐ"
    )


# =============================
# TƯ VẤN KHÁCH HÀNG
# =============================

st.subheader("💡 Tư vấn lựa chọn")

if tong_lai_giam < tong_lai_deu:

    chenh_lech = tong_lai_deu - tong_lai_giam

    st.success(
        f"""
✅ **Khuyến nghị:** Nên chọn **Dư nợ giảm dần**

- Tiết kiệm khoảng **{chenh_lech:,.0f} VNĐ** tiền lãi.
- Phù hợp với khách hàng có thu nhập ổn định.
- Tổng chi phí vay thấp hơn.
"""
    )

else:

    chenh_lech = tong_lai_giam - tong_lai_deu

    st.info(
        f"""
✅ **Khuyến nghị:** Nên chọn **Trả góp đều**

- Tiền trả hàng tháng cố định.
- Dễ quản lý tài chính cá nhân.
- Chênh lệch tiền lãi khoảng **{chenh_lech:,.0f} VNĐ**.
"""
    )
