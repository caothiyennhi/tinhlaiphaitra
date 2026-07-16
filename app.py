import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ứng dụng tính khoản vay", layout="wide")

st.title("💰 Ứng dụng tính tiền vay ngân hàng")

st.write("### Nhập thông tin khoản vay")

#=========================
# Lãi suất theo mục đích vay
#=========================

rates = {
    "Vay mua nhà":8.5,
    "Vay mua xe":9.2,
    "Vay kinh doanh":10.5,
    "Vay tiêu dùng":12
}

col1,col2=st.columns(2)

with col1:
    amount = st.number_input(
        "Số tiền vay (VNĐ)",
        min_value=1000000,
        value=500000000,
        step=1000000
    )

    months = st.number_input(
        "Thời hạn vay (tháng)",
        min_value=1,
        value=60
    )

with col2:
    purpose = st.selectbox(
        "Mục đích vay",
        list(rates.keys())
    )

    custom = st.checkbox("Nhập lãi suất thủ công")

    if custom:
        annual_rate = st.number_input(
            "Lãi suất (%/năm)",
            value=10.0
        )
    else:
        annual_rate = rates[purpose]

st.success(f"Lãi suất áp dụng: {annual_rate}%/năm")

monthly_rate = annual_rate/100/12

#=========================
# DƯ NỢ GIẢM DẦN
#=========================

goc = amount/months
remain = amount

schedule1=[]

for m in range(1,months+1):

    lai = remain*monthly_rate

    tong = goc+lai

    remain -= goc

    schedule1.append([
        m,
        round(goc),
        round(lai),
        round(tong),
        max(round(remain),0)
    ])

df1=pd.DataFrame(schedule1,
columns=[
"Tháng",
"Gốc",
"Lãi",
"Tổng trả",
"Dư nợ"
])

#=========================
# TRẢ GÓP ĐỀU
#=========================

remain=amount

payment=amount*monthly_rate*(1+monthly_rate)**months/((1+monthly_rate)**months-1)

schedule2=[]

for m in range(1,months+1):

    lai=remain*monthly_rate

    goc=payment-lai

    remain-=goc

    schedule2.append([
        m,
        round(goc),
        round(lai),
        round(payment),
        max(round(remain),0)
    ])

df2=pd.DataFrame(schedule2,
columns=[
"Tháng",
"Gốc",
"Lãi",
"Tổng trả",
"Dư nợ"
])

#=========================
# HIỂN THỊ
#=========================

tab1,tab2,tab3=st.tabs([
"Dư nợ giảm dần",
"Trả góp đều",
"So sánh"
])

with tab1:

    st.subheader("Phương thức dư nợ giảm dần")

    st.dataframe(df1,use_container_width=True)

    st.metric(
        "Tổng tiền lãi",
        f"{df1['Lãi'].sum():,.0f} VNĐ"
    )

    st.metric(
        "Tổng phải trả",
        f"{df1['Tổng trả'].sum():,.0f} VNĐ"
    )

with tab2:

    st.subheader("Phương thức trả góp đều")

    st.dataframe(df2,use_container_width=True)

    st.metric(
        "Tổng tiền lãi",
        f"{df2['Lãi'].sum():,.0f} VNĐ"
    )

    st.metric(
        "Tổng phải trả",
        f"{df2['Tổng trả'].sum():,.0f} VNĐ"
    )

with tab3:

    st.subheader("So sánh")

    compare=pd.DataFrame({

        "Phương thức":[
            "Dư nợ giảm dần",
            "Trả góp đều"
        ],

        "Tổng lãi":[
            df1["Lãi"].sum(),
            df2["Lãi"].sum()
        ],

        "Tổng thanh toán":[
            df1["Tổng trả"].sum(),
            df2["Tổng trả"].sum()
        ]

    })

    st.dataframe(compare,use_container_width=True)

    if df1["Lãi"].sum()<df2["Lãi"].sum():

        st.success("""
### ✅ Tư vấn

**Dư nợ giảm dần** là phương án tối ưu nếu:

- Muốn tiết kiệm chi phí lãi vay.
- Có khả năng trả nhiều tiền ở những tháng đầu.
- Tổng số tiền lãi thấp hơn.
""")

    else:

        st.info("""
### ✅ Tư vấn

**Trả góp đều** phù hợp nếu:

- Muốn số tiền thanh toán mỗi tháng cố định.
- Dễ lập kế hoạch tài chính.
- Thu nhập ổn định.
""")

#=========================
# BIỂU ĐỒ
#=========================

st.subheader("📊 Biểu đồ dư nợ còn lại")

fig,ax=plt.subplots(figsize=(12,5))

ax.bar(df1["Tháng"]-0.2,
       df1["Dư nợ"],
       width=0.4,
       label="Dư nợ giảm dần")

ax.bar(df2["Tháng"]+0.2,
       df2["Dư nợ"],
       width=0.4,
       label="Trả góp đều")

ax.set_xlabel("Tháng")

ax.set_ylabel("Dư nợ còn lại")

ax.legend()

st.pyplot(fig)
