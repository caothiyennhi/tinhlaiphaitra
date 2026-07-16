import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Ứng dụng tính khoản vay",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng dụng tính tiền gốc và lãi vay ngân hàng")

st.markdown("### Thông tin khoản vay")

# Mục đích vay vốn
muc_dich = st.selectbox(
    "Mục đích vay vốn",
    [
        "Mua nhà",
        "Xây dựng/Sửa chữa nhà",
        "Mua ô tô",
        "Tiêu dùng",
        "Bổ sung vốn kinh doanh",
        "Du học",
        "Khác"
    ]
)

# Sản phẩm cho vay
san_pham = st.selectbox(
    "Sản phẩm cho vay",
    [
        "Vay thế chấp",
        "Vay tín chấp",
        "Vay mua nhà",
        "Vay mua ô tô",
        "Vay kinh doanh",
        "Vay tiêu dùng"
    ]
)

# Số tiền vay
so_tien = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=1000000,
    step=1000000,
    value=500000000,
    format="%d"
)

# Thời hạn vay
thoi_han = st.number_input(
    "Thời hạn vay (tháng)",
    min_value=1,
    max_value=420,
    value=120
)

# Lãi suất
lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=30.0,
    value=8.5,
    step=0.1
)

# Phương thức trả nợ
phuong_thuc = st.selectbox(
    "Phương thức trả nợ",
    [
        "Dư nợ giảm dần",
        "Trả góp đều (Annuity)",
        "Trả lãi định kỳ, gốc cuối kỳ"
    ]
)

# Ngày giải ngân
ngay_giai_ngan = st.date_input(
    "Ngày giải ngân",
    value=date.today()
)

# Ngày thanh toán
ngay_thanh_toan = st.slider(
    "Ngày thanh toán hàng tháng",
    min_value=1,
    max_value=28,
    value=5
)

st.divider()

if st.button("Xác nhận thông tin"):
    st.success("Đã lưu thông tin khoản vay.")

    st.subheader("Thông tin đã nhập")

    st.write(f"**Mục đích vay:** {muc_dich}")
    st.write(f"**Sản phẩm vay:** {san_pham}")
    st.write(f"**Số tiền vay:** {so_tien:,.0f} VNĐ")
    st.write(f"**Thời hạn:** {thoi_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương thức trả nợ:** {phuong_thuc}")
    st.write(f"**Ngày giải ngân:** {ngay_giai_ngan.strftime('%d/%m/%Y')}")
    st.write(f"**Ngày thanh toán hàng tháng:** Ngày {ngay_thanh_toan}")

    st.info("👉 Bước tiếp theo: Tính bảng gốc và lãi theo lịch trả nợ.")
