"""
Loan Advisor - Streamlit Demo
Run:
    pip install streamlit pandas plotly
    streamlit run app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Loan Advisor", layout="wide")

def annuity(P,r,n):
    rm=r/12/100
    pay=P*rm*(1+rm)**n/((1+rm)**n-1) if rm else P/n
    bal=P
    rows=[]
    for i in range(1,n+1):
        interest=bal*rm
        principal=pay-interest
        end=max(0,bal-principal)
        rows.append([i,bal,principal,interest,pay,end])
        bal=end
    return pd.DataFrame(rows,columns=["Tháng","Dư nợ đầu kỳ","Gốc","Lãi","Tổng trả","Dư nợ cuối kỳ"])

def declining(P,r,n):
    rm=r/12/100
    gp=P/n
    bal=P
    rows=[]
    for i in range(1,n+1):
        interest=bal*rm
        total=gp+interest
        end=max(0,bal-gp)
        rows.append([i,bal,gp,interest,total,end])
        bal=end
    return pd.DataFrame(rows,columns=["Tháng","Dư nợ đầu kỳ","Gốc","Lãi","Tổng trả","Dư nợ cuối kỳ"])

st.title("💰 Loan Advisor")

with st.sidebar:
    st.header("Thông tin khoản vay")
    purpose=st.selectbox("Mục đích",["Mua nhà","Sửa nhà","Mua ô tô","Tiêu dùng","Kinh doanh"])
    amount=st.number_input("Số tiền vay",1000000,10000000000,500000000,1000000)
    years=st.slider("Thời hạn (năm)",1,35,20)
    rate=st.number_input("Lãi suất %/năm",0.1,30.0,8.0,0.1)
    method=st.radio("Phương thức",["Trả góp đều","Dư nợ giảm dần"])

months=years*12
df=annuity(amount,rate,months) if method=="Trả góp đều" else declining(amount,rate,months)

total_interest=df["Lãi"].sum()
total_payment=df["Tổng trả"].sum()

c1,c2,c3,c4=st.columns(4)
c1.metric("Khoản vay",f"{amount:,.0f}")
c2.metric("Tổng lãi",f"{total_interest:,.0f}")
c3.metric("Tổng thanh toán",f"{total_payment:,.0f}")
c4.metric("Tháng đầu",f"{df.iloc[0]['Tổng trả']:,.0f}")

tabs=st.tabs(["Lịch trả nợ","Biểu đồ","So sánh","Đánh giá DSR"])

with tabs[0]:
    st.dataframe(df.style.format("{:,.0f}"))

with tabs[1]:
    st.plotly_chart(px.line(df,x="Tháng",y="Dư nợ cuối kỳ",title="Dư nợ còn lại"),use_container_width=True)
    st.plotly_chart(px.bar(df.head(24),x="Tháng",y=["Gốc","Lãi"],barmode="group",title="24 tháng đầu"),use_container_width=True)

with tabs[2]:
    st.subheader("So sánh phương án")
    r2=st.number_input("Lãi suất PA2",0.1,30.0,9.0,0.1)
    y2=st.slider("Thời hạn PA2",1,35,25,key="y2")
    df2=annuity(amount,r2,y2*12)
    i1=total_interest
    i2=df2["Lãi"].sum()
    comp=pd.DataFrame({
        "":["PA1","PA2"],
        "Lãi suất":[rate,r2],
        "Thời hạn":[years,y2],
        "Tổng lãi":[i1,i2]
    })
    st.dataframe(comp)
    if i1<i2:
        st.success(f"PA1 tiết kiệm hơn {i2-i1:,.0f} đồng tiền lãi.")
    else:
        st.info(f"PA2 tiết kiệm hơn {i1-i2:,.0f} đồng tiền lãi.")

with tabs[3]:
income=st.number_input("Thu nhập/tháng",1000000,500000000,30000000,1000000)
    expense=st.number_input("Chi phí sinh hoạt",0,500000000,10000000,1000000)
    other=st.number_input("Khoản trả nợ khác",0,500000000,0,1000000)
    monthly=df.iloc[0]["Tổng trả"]
    dsr=(monthly+other)/income*100
    st.metric("DSR",f"{dsr:.1f}%")
    if dsr<40:
        st.success("🟢 Khả năng trả nợ tốt.")
    elif dsr<60:
        st.warning("🟡 Cần cân nhắc.")
    else:
        st.error("🔴 Rủi ro cao.")
    affordable=max(0,(income*0.4-other))
    st.write(f"Gợi ý: Khoản trả nợ nên dưới **{affordable:,.0f} đ/tháng**.")
