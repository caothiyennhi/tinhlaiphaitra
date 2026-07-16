<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Tính Lãi Suất Vay Ngân Hàng</title>
    <style>
        :root {
            --primary-color: #0056b3;
            --bg-color: #f4f7f6;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: #333;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background-color: #004494;
        }
        .summary {
            background: #e9ecef;
            padding: 15px;
            margin-top: 20px;
            border-radius: 4px;
            border-left: 5px solid var(--primary-color);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: right;
        }
        th {
            background-color: var(--primary-color);
            color: white;
            text-align: center;
        }
        td:first-child {
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Ứng Dụng Tính Tiền Gốc & Lãi Hàng Tháng</h2>
    
    <div class="form-group">
        <label for="purpose">Mục đích vay vốn / Sản phẩm:</label>
        <select id="purpose">
            <option value="Vay mua nhà">Vay mua nhà / Bất động sản</option>
            <option value="Vay mua ô tô">Vay mua ô tô</option>
            <option value="Vay tiêu dùng">Vay tiêu dùng</option>
            <option value="Vay sản xuất kinh doanh">Vay sản xuất kinh doanh</option>
        </select>
    </div>

    <div class="form-group">
        <label for="amount">Số tiền vay (VNĐ):</label>
        <input type="number" id="amount" placeholder="Ví dụ: 1000000000 (1 tỷ)" min="0">
    </div>

    <div class="form-group">
        <label for="months">Thời hạn vay (Tháng):</label>
        <input type="number" id="months" placeholder="Ví dụ: 12, 24, 60..." min="1">
    </div>

    <div class="form-group">
        <label for="rate">Lãi suất cho vay (%/năm):</label>
        <input type="number" id="rate" placeholder="Ví dụ: 8.5" step="0.1" min="0">
    </div>

    <button onclick="calculateLoan()">Tính Toán</button>

    <div id="result"></div>
</div>

<script>
    function formatVND(number) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(number);
    }

    function calculateLoan() {
        const purpose = document.getElementById('purpose').options[document.getElementById('purpose').selectedIndex].text;
        const amount = parseFloat(document.getElementById('amount').value);
        const months = parseInt(document.getElementById('months').value);
        const rateYearly = parseFloat(document.getElementById('rate').value);

        if (isNaN(amount) || isNaN(months) || isNaN(rateYearly) || amount <= 0 || months <= 0 || rateYearly < 0) {
            alert("Vui lòng nhập đầy đủ và chính xác các thông tin bằng số hợp lệ.");
            return;
        }

        // Công thức tính toán
        const principalPerMonth = amount / months;
        const rateMonthly = (rateYearly / 100) / 12;
        
        let remainingBalance = amount;
        let totalInterest = 0;
        
        let tableHTML = `
            <div class="summary">
                <strong>Tóm tắt khoản vay:</strong><br>
                - Mục đích: ${purpose}<br>
                - Tổng số tiền vay: <span style="color:red; font-weight:bold;">${formatVND(amount)}</span><br>
                - Phương pháp tính: Gốc trả đều, lãi tính trên dư nợ giảm dần.
            </div>
            <table>
                <tr>
                    <th>Kỳ (Tháng)</th>
                    <th>Tiền gốc trả hàng tháng</th>
                    <th>Tiền lãi phải trả</th>
                    <th>Tổng tiền phải trả</th>
                    <th>Dư nợ còn lại</th>
                </tr>
        `;

        for (let i = 1; i <= months; i++) {
            // Lãi tháng hiện tại = Dư nợ đầu kỳ * lãi suất tháng
            let interest = remainingBalance * rateMonthly;
            totalInterest += interest;
            
            // Tổng tiền phải trả tháng này = Gốc + Lãi
            let totalPayment = principalPerMonth + interest;
            
            // Cập nhật dư nợ
            remainingBalance -= principalPerMonth;
            
            // Xử lý sai số thập phân cho tháng cuối cùng
            if (remainingBalance < 1) remainingBalance = 0;

            tableHTML += `
                <tr>
                    <td>${i}</td>
                    <td>${formatVND(principalPerMonth)}</td>
                    <td>${formatVND(interest)}</td>
                    <td><strong>${formatVND(totalPayment)}</strong></td>
                    <td>${formatVND(remainingBalance)}</td>
                </tr>
            `;
        }

        let totalAmountPaid = amount + totalInterest;

        tableHTML += `
            <tr>
                <td colspan="2" style="text-align:center; font-weight:bold;">TỔNG CỘNG</td>
                <td style="font-weight:bold; color:red;">${formatVND(totalInterest)}</td>
                <td style="font-weight:bold; color:blue;">${formatVND(totalAmountPaid)}</td>
                <td></td>
            </tr>
        </table>`;

        document.getElementById('result').innerHTML = tableHTML;
    }
</script>

</body>
</html>
