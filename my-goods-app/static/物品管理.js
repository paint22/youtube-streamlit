document.addEventListener("DOMContentLoaded", function () {
    const searchField = document.getElementById("searchField");
    const searchText = document.getElementById("searchText");
    const searchButton = document.getElementById("searchButton");
    const itemTable = document.getElementById("itemTable").getElementsByTagName('tbody')[0];
    const addItemButton = document.getElementById("addItemButton");
    const addItemForm = document.getElementById("addItemForm");
    let currentlyEditingRow = null;

    // ページ読み込み時に全ての物品データを表示
    fetchAndDisplayItems();

    // 備品登録ボタンのクリックイベント
    addItemButton.addEventListener("click", function () {
        // 登録フォームの表示切替
        addItemForm.style.display = addItemForm.style.display === "none" ? "block" : "none";
    });

    const itemForm = document.getElementById('itemForm');
    itemForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(itemForm);

        const fileInput = document.getElementById('写真');
        if (fileInput.files[0]) {
            formData.append('photo', fileInput.files[0]);
        }

        try {
            const response = await fetch('/api/add_item', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                console.error('エラー:', data.error);
            } else {
                console.log('物品が正常に登録されました。');
            }
        } catch (error) {
            console.error('エラー:', error);
        }
    });

    // 検索ボタンがクリックされたときの処理
    searchButton.addEventListener("click", function () {
        fetchAndDisplayItems(searchField.value, searchText.value);
    });


    // 物品データを取得して表示する関数
    function fetchAndDisplayItems(field = '', text = '') {
        clearTable();
        let url = '/api/get_items';
        if (field && text) {
            url += `?field=${encodeURIComponent(field)}&text=${encodeURIComponent(text)}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(items => displayItems(items))
            .catch(error => console.error('データの取得中にエラーが発生しました:', error));
    }

    function clearTable() {
        while (itemTable.firstChild) {
            itemTable.removeChild(itemTable.firstChild);
        }
    }

    function displayItems(items) {
        items.forEach(item => {
            const row = itemTable.insertRow(-1);
            row.setAttribute('data-item-id', item['ID']);

            for (let i = 0; i < 24; i++) {
                const cell = row.insertCell(i);
                const cellValue = item[getColumnHeader(i)];

                if (i === 21) { // 写真
                    if (item['写真']) {
                        const photoLink = document.createElement("a");
                        photoLink.href = `/api/get_photo/${item['ID']}`;
                        photoLink.textContent = item['写真'];
                        photoLink.target = "_blank";
                        cell.appendChild(photoLink);
                    } else {
                        cell.textContent = 'なし';
                    }
                } else if (i === 22) { // QRコード
                    if (item['QRコード']) {
                        const qrLink = document.createElement("a");
                        qrLink.href = `/api/get_qrcode/${item['ID']}`;
                        qrLink.textContent = "QRコードを表示";
                        qrLink.target = "_blank";
                        cell.appendChild(qrLink);
                    } else {
                        cell.textContent = 'なし';
                    }
                } else if (i === 23) { // 編集ボタン
                    const editButton = document.createElement("button");
                    editButton.textContent = "編集";
                    editButton.classList.add('edit-button');
                    editButton.addEventListener("click", function () {
                        editItem(row);
                    });
                    cell.appendChild(editButton);
                } else {
                    cell.textContent = cellValue;
                }
            }
        });
    }

    function getColumnHeader(index) {
        const headers = ["ID", "購入日", "コード", "整理番号", "ST数量", "物品名", "規格", "製造番号", "製造先", "数量", "保管場所", "単価", "金額", "納入日", "支払日", "購入先", "所属", "前所属", "管理責任者", "前任者", "状態", "写真", "QRコード", "操作"];
        return headers[index];
    }

    function isDateField(headerName) {
        return ["購入日", "納入日", "支払日"].includes(headerName);
    }

    function editItem(row) {
        if (currentlyEditingRow && currentlyEditingRow !== row) {
            cancelEdit(currentlyEditingRow);
        }

        currentlyEditingRow = row;
        row.classList.add('editing');
        saveOriginalData(row);
        makeCellsEditable(row);
        addSaveCancelButtons(row);
    }

    function saveOriginalData(row) {
        row.originalData = {};
        for (let i = 0; i < row.cells.length - 1; i++) {
            row.originalData[i] = row.cells[i].textContent;
        }
    }

    function makeCellsEditable(row) {
        for (let i = 0; i < row.cells.length - 1; i++) {
            const headerName = getColumnHeader(i);
            if (i !== 21 && i !== 22) {
                const cell = row.cells[i];
                const input = document.createElement("input");
                input.type = isDateField(headerName) ? "date" : "text";
                input.value = cell.textContent;
                cell.innerHTML = '';
                cell.appendChild(input);
            }
        }
    }

    function addSaveCancelButtons(row) {
        const saveButton = document.createElement("button");
        saveButton.textContent = "保存";
        saveButton.addEventListener("click", function () {
            saveEdit(row);
        });

        const cancelButton = document.createElement("button");
        cancelButton.textContent = "キャンセル";
        cancelButton.addEventListener("click", function () {
            cancelEdit(row);
        });

        const buttonCell = row.cells[row.cells.length - 1];
        buttonCell.innerHTML = '';
        buttonCell.appendChild(saveButton);
        buttonCell.appendChild(cancelButton);
    }

    function saveEdit(row) {
        const itemId = row.getAttribute('data-item-id');
        const formData = new FormData();

        for (let i = 0; i < row.cells.length - 1; i++) {
            if (i !== 21 && i !== 22) {
                const input = row.cells[i].querySelector("input");
                formData.append(getColumnHeader(i), input.value);
            }
        }

        fetch(`/api/edit_item/${itemId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('エラー:', data.error);
            } else {
            // レスポンスが正常の場合、テーブル行を更新
            updateTableRow(formData, row);
            row.classList.remove('editing');
            addEditButton(row);
            }
        }).catch(error => {
            console.error('エラー:', error);
        });
    }

    function updateTableRow(formData, row) {
        for (let [key, value] of formData.entries()) {
            const cellIndex = getColumnHeaderIndex(key);
            if (cellIndex !== -1 && cellIndex < row.cells.length - 1) {  // 操作列を除外
                row.cells[cellIndex].textContent = value;
            }
        }
    }

    function cancelEdit(row) {
        for (let i = 0; i < row.cells.length - 1; i++) {
            if (i !== 21 && i !== 22) {
                const cell = row.cells[i];
                cell.innerHTML = '';
                cell.textContent = row.originalData[i];
            }
        }
        row.classList.remove('editing');
        addEditButton(row);
    }

    function addEditButton(row) {
        const editButton = document.createElement("button");
        editButton.textContent = "編集";
        editButton.addEventListener("click", function () {
            editItem(row);
        });

        const buttonCell = row.cells[row.cells.length - 1];
        buttonCell.innerHTML = '';
        buttonCell.appendChild(editButton);
    }

    function updateTableRow(formData, row) {
        for (let [key, value] of formData.entries()) {
            const cellIndex = getColumnHeaderIndex(key);
            if (cellIndex !== -1) {
                row.cells[cellIndex].textContent = value;
            }
        }
        row.classList.remove('editing');
        addEditButton(row);
    }

    function getColumnHeaderIndex(headerName) {
        const headers = ["ID", "購入日", "コード", "整理番号", "ST数量", "物品名", "規格", "製造番号", "製造先", "数量", "保管場所", "単価", "金額", "納入日", "支払日", "購入先", "所属", "前所属", "管理責任者", "前任者", "状態", "写真", "QRコード", "操作"];
        return headers.indexOf(headerName);
    }
});

