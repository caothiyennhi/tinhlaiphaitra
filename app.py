import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ứng dụng tính vay vốn", page_icon="💰")

st.title("💰 Ứng dụng tính khoản vay ngân hàng")

st.write("### Nhập thông tin khoản vay")

# Nhập thông tin
so_tien = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=1000000,
    step=1000000,
    value=100000000
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=10.0
)

thoi_han = st.number_input(
    "Thời hạn vay (tháng)",
    min_value=1,
    value=12
)

muc_dich = st.selectbox(
    "Mục đích vay vốn",
    [
        "Mua nhà",
        "Mua ô tô",
        "Tiêu dùng",
        "Kinh doanh",
        "Du học",
        "Khác"
    ]
)

phuong_thuc = st.radio(
    "Phương thức trả nợ",
    [
        "Dư nợ giảm dần",
        "Trả góp đều"
    ]
)

if st.button("Tính toán"):

    lai_thang = lai_suat / 100 / 12

    bang = []

    # ==========================
    # DƯ NỢ GIẢM DẦN
    # ==========================

    if phuong_thuc == "Dư nợ giảm dần":

        goc_thang = so_tien / thoi_han
        du_no = so_tien

        tong_lai = 0

        for i in range(1, thoi_han + 1):

            lai = du_no * lai_thang
            tong = goc_thang + lai

            bang.append([
                i,
                round(goc_thang),
                round(lai),
                round(tong),
                round(du_no - goc_thang)
            ])

            tong_lai += lai
            du_no -= goc_thang

    # ==========================
    # TRẢ GÓP ĐỀU
    # ==========================

    else:

        tien_tra = so_tien * lai_thang * (1 + lai_thang) ** thoi_han
        tien_tra /= ((1 + lai_thang) ** thoi_han - 1)

        du_no = so_tien
        tong_lai = 0

        for i in range(1, thoi_han + 1):

            lai = du_no * lai_thang
            goc = tien_tra - lai

            bang.append([
                i,
                round(goc),
                round(lai),
                round(tien_tra),
                round(du_no - goc)
            ])

            tong_lai += lai
            du_no -= goc

    df = pd.DataFrame(
        bang,
        columns=[
            "Tháng",
            "Tiền gốc",
            "Tiền lãi",
            "Tổng thanh toán",
            "Dư nợ còn lại"
        ]
    )

    st.success("Đã tính toán thành công!")

    st.write("## Thông tin khoản vay")

    st.write(f"**Mục đích vay:** {muc_dich}")
    st.write(f"**Số tiền vay:** {so_tien:,.0f} VNĐ")
    st.write(f"**Lãi suất:** {lai_suat}%/năm")
    st.write(f"**Thời hạn:** {thoi_han} tháng")

    st.write("## Kết quả")

    st.metric("Tổng tiền lãi", f"{tong_lai:,.0f} VNĐ")
    st.metric("Tổng phải thanh toán", f"{so_tien + tong_lai:,.0f} VNĐ")

    st.write("## Bảng chi tiết")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 Tải bảng trả nợ",
        csv,
        file_name="Bang_tra_no.csv",
        mime="text/csv"
    )
