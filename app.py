import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# CẤU HÌNH TRANG
# =====================================

st.set_page_config(
    page_title="Smart Loan Advisor",
    page_icon="🏦",
    layout="wide"
)

# =====================================
# CSS GIAO DIỆN
# =====================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

h1{
    color:#0d47a1;
}

.stButton>button{
    width:100%;
    height:50px;
    font-size:18px;
    background:#1565C0;
    color:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TIÊU ĐỀ
# =====================================

st.title("🏦 SMART LOAN ADVISOR")

st.write(
"""
Ứng dụng hỗ trợ khách hàng:

- 💰 Tính khoản vay
- 📊 So sánh phương thức trả nợ
- 📈 Phân tích khả năng trả nợ
- 🤖 Đề xuất khoản vay tối ưu
"""
)

st.divider()

# =====================================
# THÔNG TIN KHÁCH HÀNG
# =====================================

st.header("👤 Thông tin khách hàng")

col1,col2=st.columns(2)

with col1:

    ho_ten=st.text_input(
        "Họ và tên",
        placeholder="Nhập họ tên"
    )

    thu_nhap=st.number_input(
        "Thu nhập hàng tháng (VNĐ)",
        min_value=0,
        value=20000000,
        step=1000000
    )

with col2:

    nghe_nghiep=st.text_input(
        "Nghề nghiệp",
        placeholder="Ví dụ: Nhân viên văn phòng"
    )

    chi_tieu=st.number_input(
        "Chi tiêu hàng tháng (VNĐ)",
        min_value=0,
        value=8000000,
        step=500000
    )

st.divider()

# =====================================
# THÔNG TIN KHOẢN VAY
# =====================================

st.header("💳 Thông tin khoản vay")

left,right=st.columns(2)

with left:

    so_tien=st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=1000000,
        value=500000000,
        step=1000000
    )

    thoi_han=st.slider(
        "Thời hạn vay (tháng)",
        6,
        360,
        60
    )

with right:

    muc_dich=st.selectbox(
        "Mục đích vay",

        [
            "Mua nhà",
            "Mua ô tô",
            "Kinh doanh",
            "Tiêu dùng",
            "Du học",
            "Khác"
        ]
    )

# =====================================
# LÃI SUẤT TỰ ĐỘNG
# =====================================

lai_suat_dict={

    "Mua nhà":7.2,

    "Mua ô tô":8.0,

    "Kinh doanh":9.5,

    "Tiêu dùng":11.5,

    "Du học":8.8,

    "Khác":10.0

}

lai_suat=lai_suat_dict[muc_dich]

st.info(f"📌 Lãi suất áp dụng theo mục đích vay: **{lai_suat}%/năm**")

lai_thang=lai_suat/100/12

st.divider()

# =====================================
# CHỌN PHƯƠNG THỨC
# =====================================

st.header("📑 Phương thức tính")

phuong_thuc=st.radio(

    "Chọn phương thức trả nợ",

    [

        "Dư nợ giảm dần",

        "Trả góp đều"

    ],

    horizontal=True

)

st.divider()

# =====================================
# DASHBOARD NHANH
# =====================================

st.subheader("📊 Thông tin nhanh")

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "Số tiền vay",

        f"{so_tien:,.0f} VNĐ"

    )

with c2:

    st.metric(

        "Lãi suất",

        f"{lai_suat}%"

    )

with c3:

    st.metric(

        "Thời hạn",

        f"{thoi_han} tháng"

    )

with c4:

    st.metric(

        "Thu nhập",

        f"{thu_nhap:,.0f}"

    )

st.divider()

# =====================================
# NÚT TÍNH TOÁN
# =====================================

tinh=st.button("🚀 BẮT ĐẦU PHÂN TÍCH KHOẢN VAY")

if tinh:

    bang=[]

    #    # =====================================
    # TÍNH TOÁN KHOẢN VAY
    # =====================================

    tong_lai = 0
    tong_goc = so_tien
    du_no = so_tien

    # Danh sách dùng để vẽ biểu đồ
    ds_du_no = []
    ds_goc = []
    ds_lai = []
    ds_tong = []
    ds_thang = []

    # =====================================
    # PHƯƠNG THỨC 1
    # DƯ NỢ GIẢM DẦN
    # =====================================

    if phuong_thuc == "Dư nợ giảm dần":

        goc_thang = so_tien / thoi_han

        for thang in range(1, thoi_han + 1):

            lai = du_no * lai_thang

            tong = goc_thang + lai

            tong_lai += lai

            bang.append([
                thang,
                round(goc_thang),
                round(lai),
                round(tong),
                round(max(du_no - goc_thang,0))
            ])

            ds_thang.append(thang)
            ds_goc.append(goc_thang)
            ds_lai.append(lai)
            ds_tong.append(tong)
            ds_du_no.append(max(du_no-goc_thang,0))

            du_no -= goc_thang

    # =====================================
    # PHƯƠNG THỨC 2
    # TRẢ GÓP ĐỀU
    # =====================================

    else:

        tien_tra = (
            so_tien
            * lai_thang
            * (1 + lai_thang) ** thoi_han
        ) / (
            (1 + lai_thang) ** thoi_han - 1
        )

        for thang in range(1, thoi_han + 1):

            lai = du_no * lai_thang

            goc = tien_tra - lai

            tong_lai += lai

            bang.append([
                thang,
                round(goc),
                round(lai),
                round(tien_tra),
                round(max(du_no-goc,0))
            ])

            ds_thang.append(thang)
            ds_goc.append(goc)
            ds_lai.append(lai)
            ds_tong.append(tien_tra)
            ds_du_no.append(max(du_no-goc,0))

            du_no -= goc

    # =====================================
    # DATAFRAME
    # =====================================

    df = pd.DataFrame(

        bang,

        columns=[

            "Tháng",

            "Tiền gốc",

            "Tiền lãi",

            "Tổng phải trả",

            "Dư nợ còn lại"

        ]

    )

    tong_thanh_toan = tong_goc + tong_lai

    # =====================================
    # KẾT QUẢ TỔNG QUAN
    # =====================================

    st.success("✅ Đã tính toán thành công!")

    st.header("📋 Kết quả khoản vay")

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.metric(

            "💰 Tổng tiền vay",

            f"{tong_goc:,.0f} VNĐ"

        )

    with c2:

        st.metric(

            "💸 Tổng tiền lãi",

            f"{tong_lai:,.0f} VNĐ"

        )

    with c3:

        st.metric(

            "💳 Tổng thanh toán",

            f"{tong_thanh_toan:,.0f} VNĐ"

        )

    with c4:

        st.metric(

            "📅 Trả tháng đầu",

            f"{ds_tong[0]:,.0f} VNĐ"

        )

    st.divider()

    # =====================================
    # THÔNG TIN KHÁCH HÀNG
    # =====================================

    st.subheader("👤 Thông tin khoản vay")

    info1,info2=st.columns(2)

    with info1:

        st.write(f"**Khách hàng:** {ho_ten}")

        st.write(f"**Nghề nghiệp:** {nghe_nghiep}")

        st.write(f"**Mục đích vay:** {muc_dich}")

    with info2:

        st.write(f"**Lãi suất:** {lai_suat}%/năm")

        st.write(f"**Thời hạn:** {thoi_han} tháng")

        st.write(f"**Phương thức:** {phuong_thuc}")

    st.divider()

    # =====================================
    # BẢNG TRẢ NỢ
    # =====================================

    st.subheader("📑 Bảng kế hoạch trả nợ")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(

        "📥 Tải bảng trả nợ CSV",

        csv,

        "BangTraNo.csv",

        "text/csv"

    )

    st.divider()

    # ==================================================
    # PHẦN 3 SẼ VIẾT TIẾP TẠI ĐÂY
      # ==================================================
    # SO SÁNH HAI PHƯƠNG THỨC TRẢ NỢ
    # ==================================================

    st.header("📊 So sánh hai phương thức trả nợ")

    # ---------- Dư nợ giảm dần ----------
    goc_giam = so_tien / thoi_han
    du_no = so_tien
    tong_lai_giam = 0

    for i in range(thoi_han):
        lai = du_no * lai_thang
        tong_lai_giam += lai
        du_no -= goc_giam

    tong_tt_giam = so_tien + tong_lai_giam

    # ---------- Trả góp đều ----------
    tien_tra_deu = (
        so_tien * lai_thang * (1 + lai_thang) ** thoi_han
    ) / (
        (1 + lai_thang) ** thoi_han - 1
    )

    du_no = so_tien
    tong_lai_deu = 0

    for i in range(thoi_han):

        lai = du_no * lai_thang
        goc = tien_tra_deu - lai

        tong_lai_deu += lai
        du_no -= goc

    tong_tt_deu = so_tien + tong_lai_deu

    bang_ss = pd.DataFrame({

        "Phương thức":[
            "Dư nợ giảm dần",
            "Trả góp đều"
        ],

        "Tổng tiền lãi":[
            round(tong_lai_giam),
            round(tong_lai_deu)
        ],

        "Tổng thanh toán":[
            round(tong_tt_giam),
            round(tong_tt_deu)
        ]

    })

    st.dataframe(bang_ss, use_container_width=True)

    st.bar_chart(
        bang_ss.set_index("Phương thức")["Tổng tiền lãi"]
    )

    # ==================================================
    # TƯ VẤN PHƯƠNG THỨC TỐI ƯU
    # ==================================================

    st.subheader("🤖 Khuyến nghị")

    if tong_lai_giam < tong_lai_deu:

        chenh = tong_lai_deu - tong_lai_giam

        st.success(f"""

### ✅ Khuyến nghị: Dư nợ giảm dần

✔ Tiết kiệm khoảng **{chenh:,.0f} VNĐ**

✔ Tổng tiền lãi thấp hơn

✔ Phù hợp với khách hàng có thu nhập ổn định

✔ Muốn giảm tổng chi phí vay

""")

    else:

        chenh = tong_lai_giam - tong_lai_deu

        st.info(f"""

### ✅ Khuyến nghị: Trả góp đều

✔ Tiền trả hàng tháng cố định

✔ Dễ quản lý tài chính

✔ Chênh lệch tiền lãi khoảng **{chenh:,.0f} VNĐ**

""")

    st.divider()

    # ==================================================
    # BIỂU ĐỒ DƯ NỢ
    # ==================================================

    st.header("📈 Biểu đồ dư nợ")

    fig1, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        ds_thang,
        ds_du_no,
        linewidth=2
    )

    ax.set_xlabel("Tháng")

    ax.set_ylabel("VNĐ")

    ax.grid(True)

    st.pyplot(fig1)

    # ==================================================
    # BIỂU ĐỒ GỐC - LÃI
    # ==================================================

    st.header("📉 Biểu đồ tiền gốc và tiền lãi")

    fig2, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        ds_thang,
        ds_goc,
        label="Tiền gốc"
    )

    ax.plot(
        ds_thang,
        ds_lai,
        label="Tiền lãi"
    )

    ax.legend()

    ax.grid(True)

    st.pyplot(fig2)

    # ==================================================
    # ĐÁNH GIÁ KHẢ NĂNG TRẢ NỢ
    # ==================================================

    st.header("💳 Đánh giá khả năng trả nợ (DSR)")

    tien_tra_thang = ds_tong[0]

    dsr = tien_tra_thang / thu_nhap * 100

    st.metric(

        "DSR",

        f"{dsr:.1f}%"

    )

    if dsr <= 35:

        st.success("""

🟢 Rất tốt

Khoản vay nằm trong khả năng chi trả.

""")

    elif dsr <= 50:

        st.warning("""

🟡 Chấp nhận được

Nên cân đối thêm chi tiêu.

""")

    else:

        st.error("""

🔴 Rủi ro

Khoản vay vượt khả năng tài chính.

""")

    st.divider()

    # ==================================================
    # ƯỚC TÍNH HẠN MỨC VAY
    # ==================================================

    st.header("💰 Ước tính hạn mức vay")

    thu_nhap_an_toan = thu_nhap * 0.4

    han_muc = thu_nhap_an_toan * thoi_han

    st.metric(

        "Hạn mức vay khuyến nghị",

        f"{han_muc:,.0f} VNĐ"

    )

    if so_tien <= han_muc:

        st.success("""

Khoản vay hiện tại nằm trong hạn mức an toàn.

""")

    else:

        st.error(f"""

Khoản vay cao hơn khoảng

**{so_tien-han_muc:,.0f} VNĐ**

so với mức khuyến nghị.

""")

    st.divider()

    # ==================================================
    # CHẤM ĐIỂM KHẢ NĂNG TRẢ NỢ
    # ==================================================

    st.header("⭐ Xếp hạng hồ sơ")

    score = 100

    if dsr > 35:
        score -= 15

    if dsr > 50:
        score -= 20

    if thoi_han > 120:
        score -= 10

    if chi_tieu > thu_nhap * 0.7:
        score -= 20

    if score >= 90:

        st.success(f"🏆 Điểm tài chính: {score}/100 (Xuất sắc)")

    elif score >= 75:

        st.info(f"🥈 Điểm tài chính: {score}/100 (Tốt)")

    elif score >= 60:

        st.warning(f"🥉 Điểm tài chính: {score}/100 (Trung bình)")

    else:

        st.error(f"⚠ Điểm tài chính: {score}/100 (Rủi ro cao)")

    st.divider()

    # ==================================================
    # KHUYẾN NGHỊ CUỐI CÙNG
    # ==================================================

    st.header("📌 Kết luận")

    if score >= 90:

        st.success("""

### 🎉 Hồ sơ rất tốt

✔ Nên vay theo đúng kế hoạch.

✔ Khuyến nghị chọn **Dư nợ giảm dần** để tiết kiệm chi phí.

""")

    elif score >= 75:

        st.info("""

### 👍 Hồ sơ tốt

✔ Có thể vay.

✔ Nên cân đối chi tiêu để giảm DSR.

""")

    elif score >= 60:

        st.warning("""

### ⚠ Cần cân nhắc

✔ Nên giảm số tiền vay hoặc kéo dài thời hạn.

""")

    else:

        st.error("""

### ❌ Không khuyến nghị vay

✔ DSR quá cao.

✔ Thu nhập chưa đáp ứng khả năng trả nợ.

""")    # =========================================================
    # DASHBOARD TỔNG QUAN
    # =========================================================

    st.divider()

    st.header("📊 Dashboard khoản vay")

    col1,col2,col3,col4=st.columns(4)

    col1.metric(
        "💵 Khoản vay",
        f"{so_tien:,.0f}"
    )

    col2.metric(
        "💸 Tổng lãi",
        f"{tong_lai:,.0f}"
    )

    col3.metric(
        "📅 Trả tháng đầu",
        f"{ds_tong[0]:,.0f}"
    )

    col4.metric(
        "⭐ Điểm tài chính",
        f"{score}/100"
    )

    st.divider()

    # =========================================================
    # BIỂU ĐỒ TRÒN GỐC - LÃI
    # =========================================================

    st.header("🥧 Cơ cấu khoản thanh toán")

    fig3, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        [tong_goc,tong_lai],
        labels=["Tiền gốc","Tiền lãi"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig3)

    st.divider()

    # =========================================================
    # BIỂU ĐỒ THANH TOÁN HÀNG THÁNG
    # =========================================================

    st.header("📈 Tiền phải trả theo từng tháng")

    fig4, ax = plt.subplots(figsize=(12,4))

    ax.bar(
        ds_thang,
        ds_tong
    )

    ax.set_xlabel("Tháng")

    ax.set_ylabel("VNĐ")

    ax.grid(True)

    st.pyplot(fig4)

    st.divider()

    # =========================================================
    # AI RECOMMENDATION
    # =========================================================

    st.header("🤖 AI Loan Advisor")

    if dsr < 35:

        st.success(f"""

### 🎯 Khuyến nghị

Khách hàng **{ho_ten}**

Có khả năng trả nợ tốt.

✔ Có thể vay **{so_tien:,.0f} VNĐ**

✔ Nên chọn **Dư nợ giảm dần**

để tiết kiệm khoảng

**{abs(tong_lai_deu-tong_lai_giam):,.0f} VNĐ**

tiền lãi.

""")

    elif dsr < 50:

        st.warning("""

### Khuyến nghị

✔ Có thể vay

✔ Nên kéo dài thời hạn vay

để giảm áp lực tài chính.

""")

    else:

        st.error("""

### Khuyến nghị

Không nên vay với số tiền hiện tại.

Hãy:

✔ Giảm số tiền vay

hoặc

✔ Tăng thời hạn vay

""")

    st.divider()

    # =========================================================
    # GỢI Ý THỜI HẠN
    # =========================================================

    st.header("📅 Gợi ý thời hạn vay")

    if dsr > 50:

        st.info("""

Nên tăng thời hạn vay lên:

- 84 tháng

hoặc

- 120 tháng

để giảm số tiền phải trả hàng tháng.

""")

    elif dsr < 30:

        st.success("""

Bạn hoàn toàn có thể:

✔ Rút ngắn thời hạn vay

để tiết kiệm chi phí lãi.

""")

    st.divider()

    # =========================================================
    # NHẬN XÉT CUỐI CÙNG
    # =========================================================

    st.header("📝 Báo cáo đánh giá")

    st.write(f"""

### Thông tin khách hàng

- Họ tên: **{ho_ten}**

- Nghề nghiệp: **{nghe_nghiep}**

- Thu nhập: **{thu_nhap:,.0f} VNĐ**

- Chi tiêu: **{chi_tieu:,.0f} VNĐ**

---

### Khoản vay

- Mục đích: **{muc_dich}**

- Số tiền vay: **{so_tien:,.0f} VNĐ**

- Lãi suất: **{lai_suat}%/năm**

- Thời hạn: **{thoi_han} tháng**

---

### Đánh giá

- DSR: **{dsr:.2f}%**

- Điểm tài chính: **{score}/100**

- Tổng tiền lãi: **{tong_lai:,.0f} VNĐ**

- Tổng thanh toán: **{tong_thanh_toan:,.0f} VNĐ**

""")

    st.divider()

    # =========================================================
    # XUẤT FILE CSV
    # =========================================================

    st.download_button(
        "📥 Xuất bảng trả nợ (.csv)",
        df.to_csv(index=False).encode("utf-8-sig"),
        "BangTraNo.csv",
        "text/csv"
    )

    st.success("✅ Phân tích khoản vay hoàn tất.")
