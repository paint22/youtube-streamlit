document.addEventListener("DOMContentLoaded", function () {
    const materials = [
        { code: "0001", name: "A" },
        { code: "0002", name: "B" },
        { code: "0003", name: "C" },
        // 他の材料データを追加
    ];

    const orders = [];

    const materialSearchInput = document.getElementById("material-search");
    const quantityInput = document.getElementById("quantity");
    const orderList = document.getElementById("order-list");
    const addOrderButton = document.getElementById("add-order-button");
    const clearOrderButton = document.getElementById("clear-order-button");
    const saveOrderButton = document.getElementById("save-order-button");

    // 材料名または材料コード検索関数
    function searchMaterial() {
        const materialSearch = materialSearchInput.value.toLowerCase();
        orderList.innerHTML = "";

        materials.forEach(material => {
            if (material.name.toLowerCase().includes(materialSearch) || material.code.includes(materialSearch)) {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${material.code}</td>
                    <td>${material.name}</td>
                    <td><button onclick="addOrder('${material.code}', '${material.name}')">発注追加</button></td>
                `;
                orderList.appendChild(row);
            }
        });
    }

    // 発注を追加する関数
    function addOrder(materialCode, materialName) {
        const quantity = quantityInput.value;

        if (quantity <= 0) {
            alert("数量は1以上で指定してください。");
            return;
        }

        orders.push({ materialCode, materialName, quantity });
        updateOrderList();
        quantityInput.value = "";
    }

    // 発注リストを表示する関数
    function updateOrderList() {
        orderList.innerHTML = "";

        orders.forEach(order => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${order.materialCode}</td>
                <td>${order.materialName}</td>
                <td>${order.quantity}</td>
            `;
            orderList.appendChild(row);
        });
    }

    // 発注リストをクリアする関数
    function clearOrderList() {
        orders.length = 0;
        updateOrderList();
    }

    // 発注リストを保存する関数
    function saveOrderList() {
        localStorage.setItem("orders", JSON.stringify(orders));
        alert("発注リストが保存されました。");
    }

    addOrderButton.addEventListener("click", function () {
        const selectedMaterial = materials.find(material => material.code === materialSearchInput.value || material.name === materialSearchInput.value);
        if (!selectedMaterial) {
            alert("材料が見つかりませんでした。");
            return;
        }
        addOrder(selectedMaterial.code, selectedMaterial.name);
    });

    clearOrderButton.addEventListener("click", clearOrderList);
    saveOrderButton.addEventListener("click", saveOrderList);

    // ページが読み込まれた時にローカルストレージから発注リストを読み込む
    const savedOrders = localStorage.getItem("orders");
    if (savedOrders) {
        orders.push(...JSON.parse(savedOrders));
        updateOrderList();
    }
});