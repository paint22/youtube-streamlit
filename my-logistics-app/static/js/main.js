// ページが読み込まれたらデータを取得してテーブルを更新
document.addEventListener("DOMContentLoaded", function() {
    // 定期的にデータを更新するための関数を呼び出す
    setInterval(updateData, 5000); // 5秒ごとに更新（必要に応じて調整）
});

// データを取得してテーブルを更新する関数
function updateData() {
    fetch('/api/get_orders') // データを提供するAPIのURLを指定
        .then(response => response.json())
        .then(data => {
            // データをHTMLテーブルに挿入
            const tableBody = document.getElementById('order-table-body');
            tableBody.innerHTML = ''; // テーブルの内容をクリア
            
            data.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.商品コード}</td>
                    <td>${order.商品名}</td>
                    <td>${order.数量}</td>
                    <td>${order.発注日}</td>
                    <td>${order.出庫確認}</td>
                    <td>${order.出発地点}</td>
                    <td>${order.運送責任者}</td>
                    <td>${order.入庫確認}</td>
                    <td>${order.受取地点}</td>
                    <td>${order.受取サイン}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('データの取得エラー:', error));
}