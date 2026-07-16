import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Loan Advisor",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 SMART LOAN ADVISOR")
st.caption("Ứng dụng tính khoản vay và tư vấn phương thức trả nợ tối ưu")

# ==================================
# NHẬP THÔNG TIN
# ==================================

st.sidebar.header("Thông tin khoản vay")

so_tien = st.sidebar.number_input(
    "Số tiền vay (VNĐ)",
    min_value=1000000,
    value=300000000,
    step=1000000
)

thoi_han = st.sidebar.slider(
    "Thời hạn vay (tháng)",
    6,
    360,
    60
)

muc_dich = st.sidebar.selectbox(
    "Mục đích vay",
    [
        "Mua nhà",
        "Mua ô tô",
        "Kinh doanh",
        "Tiêu dùng",
        "Du học"
    ]
)

# Lãi suất theo mục đích

lai_suat_dict = {
    "Mua nhà":6.8,
    "Mua ô tô":7.5,
    "Kinh doanh":8.5,
    "Tiêu dùng":11,
    "Du học":7
}

lai_suat = lai_suat_dict[muc_dich]

st.sidebar.success(f"Lãi suất áp dụng: {lai_suat}%/năm")

lai_thang = lai_suat/100/12

# ==================================
# HÀM DƯ NỢ GIẢM DẦN
# ==================================

def du_no_giam_dan():

    bang=[]

    du_no=so_tien

    goc=so_tien/thoi_han

    tong_lai=0

    for i in range(1,thoi_han+1):

        lai=du_no*lai_thang

        tong=goc+lai

        tong_lai+=lai

        bang.append([
            i,
            round(goc),
            round(lai),
            round(tong),
            round(du_no-goc)
        ])

        du_no-=goc

    return bang,tong_lai

# ==================================
# HÀM TRẢ GÓP ĐỀU
# ==================================

def tra_gop_deu():

    bang=[]

    tien_tra=so_tien*lai_thang*(1+lai_thang)**thoi_han
    tien_tra/=((1+lai_thang)**thoi_han-1)

    du_no=so_tien

    tong_lai=0

    for i in range(1,thoi_han+1):

        lai=du_no*lai_thang

        goc=tien_tra-lai

        tong_lai+=lai

        bang.append([
            i,
            round(goc),
            round(lai),
            round(tien_tra),
            round(du_no-goc)
        ])

        du_no-=goc

    return bang,tong_lai

# ==================================
# TÍNH TOÁN
# ==================================

if st.button("📈 Tính khoản vay"):

    bang_giam,lai_giam=du_no_giam_dan()

    bang_deu,lai_deu=tra_gop_deu()

    # =======================

    col1,col2,col3=st.columns(3)

    col1.metric(
        "💰 Số tiền vay",
        f"{so_tien:,.0f} VNĐ"
    )

    col2.metric(
        "📅 Thời hạn",
        f"{thoi_han} tháng"
    )

    col3.metric(
        "📈 Lãi suất",
        f"{lai_suat}%/năm"
    )

    st.divider()

    # ==========================
    # BẢNG TRẢ NỢ
    # ==========================

    st.subheader("📄 Bảng trả nợ")

    phuong_thuc = st.radio(
        "Chọn phương thức",
        [
            "Dư nợ giảm dần",
            "Trả góp đều"
        ]
    )

    if phuong_thuc=="Dư nợ giảm dần":

        df=pd.DataFrame(
            bang_giam,
            columns=[
                "Tháng",
                "Tiền gốc",
                "Tiền lãi",
                "Tổng trả",
                "Dư nợ"
            ]
        )

        tong_lai=lai_giam

    else:

        df=pd.DataFrame(
            bang_deu,
            columns=[
                "Tháng",
                "Tiền gốc",
                "Tiền lãi",
                "Tổng trả",
                "Dư nợ"
            ]
        )

        tong_lai=lai_deu

    st.dataframe(df,use_container_width=True)

    st.metric(
        "💵 Tổng tiền lãi",
        f"{tong_lai:,.0f} VNĐ"
    )

    st.metric(
        "💳 Tổng phải thanh toán",
        f"{so_tien+tong_lai:,.0f} VNĐ"
    )

    st.divider()

    # ==================================
    # SO SÁNH
    # ==================================

    st.subheader("📊 So sánh hai phương thức")

    ss=pd.DataFrame({

        "Phương thức":[
            "Dư nợ giảm dần",
            "Trả góp đều"
        ],

        "Tổng lãi":[
            round(lai_giam),
            round(lai_deu)
        ],

        "Tổng thanh toán":[
            round(so_tien+lai_giam),
            round(so_tien+lai_deu)
        ]

    })

    st.dataframe(ss,use_container_width=True)

    st.bar_chart(
        ss.set_index("Phương thức")["Tổng lãi"]
    )

    # ==================================
    # TƯ VẤN
    # ==================================

    st.subheader("🤖 Tư vấn phương thức tối ưu")

    if lai_giam<lai_deu:

        st.success(f"""

### ✅ Khuyến nghị

Nên chọn **Dư nợ giảm dần**

✔ Tổng tiền lãi thấp hơn

✔ Tiết kiệm khoảng **{lai_deu-lai_giam:,.0f} VNĐ**

✔ Phù hợp với khách hàng có thu nhập ổn định.

""")

    else:

        st.info(f"""

### ✅ Khuyến nghị

Nên chọn **Trả góp đều**

✔ Tiền trả hàng tháng cố định

✔ Dễ lập kế hoạch tài chính

✔ Chênh lệch tiền lãi khoảng **{lai_giam-lai_deu:,.0f} VNĐ**

""")

    # ==================================
    # XUẤT EXCEL
    # ==================================

    excel=df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 Tải bảng trả nợ",
        excel,
        "BangTraNo.csv",
        "text/csv"
    )
