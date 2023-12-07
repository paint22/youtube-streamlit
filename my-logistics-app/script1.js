// サンプルの発注情報データ
const orders = [
    { id: "1", product: "商品1", quantity: 10, confirmed: false },
    { id: "2", product: "商品2", quantity: 5, confirmed: false },
    // 他の発注情報
];

// 初期表示時に発注情報一覧を更新
updateOrderList();

// 予約一覧を表示する関数
function updateOrderList() {
    const orderList = document.getElementById("order-list");

    // 予約一覧をクリア
    orderList.innerHTML = "";

    // 予約情報を表示
    orders.forEach((order) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.product}</td>
            <td>${order.quantity}</td>
            <td class="qrcode-column"></td> <!-- 空のQRコードカラム -->
        `;
        orderList.appendChild(row);
    });
}

// QRコード生成ボタンのクリックイベントリスナーを設定
document.getElementById("generate-qrcode").addEventListener("click", generateQRCode);

// QRコード生成関数
function generateQRCode() {
    const qrCodeCells = document.querySelectorAll(".qrcode-column");
    qrCodeCells.forEach((cell, index) => {
        const text = `材料コード: ${orders[index].id}, 数量: ${orders[index].quantity}`;

        // 既存のQRコードをクリア
        cell.innerHTML = "";

        // QRコード生成の実装
        const qrCodeDiv = document.createElement("div");
        new QRCode(qrCodeDiv, {
            text: text, // 材料コードと数量をQRコードに埋め込む
            width: 128,
            height: 128,
        });

        // 生成したQRコードをセルに追加
        cell.appendChild(qrCodeDiv);
    });
}