st.write("## So sánh hai phương thức vay")

# ===== DƯ NỢ GIẢM DẦN =====

goc = so_tien / thoi_han
du_no = so_tien

tong_lai_giam = 0

for i in range(thoi_han):
    tong_lai_giam += du_no * lai_thang
    du_no -= goc


# ===== TRẢ GÓP ĐỀU =====

tien_tra = so_tien * lai_thang * (1 + lai_thang) ** thoi_han
tien_tra /= ((1 + lai_thang) ** thoi_han - 1)

du_no = so_tien

tong_lai_deu = 0

for i in range(thoi_han):
    lai = du_no * lai_thang
    goc = tien_tra - lai
    tong_lai_deu += lai
    du_no -= goc

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
        round(so_tien + tong_lai_giam),
        round(so_tien + tong_lai_deu)
    ]

})

st.dataframe(bang_ss, use_container_width=True)
