function processForm(event) {
    event.preventDefault();  // 防止表單提交後頁面重新加載

    // 提交表單
    const inputText = document.querySelector('input[name="item_name"]').value;
    const formData = new FormData();
    formData.append('input_text', inputText);

    fetch('/scrap_items/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())  // 從Response中提取json格式的資料
        .then(data => {
            const asdaTable = document.getElementById('asda_results');
            const sainsTable = document.getElementById('sains_results');
            const tescoTable = document.getElementById('tesco_results');
            asdaTable.innerHTML = '';  // 清空表格內容
            sainsTable.innerHTML = '';  // 清空表格內容
            tescoTable.innerHTML = '';  // 清空表格內容

            const asda_list = data.businesses[0];
            const sains_list = data.businesses[1];
            const tesco_list = data.businesses[2];

            function attribute_to_table(table, item_list) {

                // 動態生成表格行
                const thead = document.createElement('thead');
                thead.textContent = result['business'];
                table.appendChild(thead);

                const tbody = document.createElement('tbody');
                for (const result of item_list) {
                    const row = document.createElement('tr');
                    const cell1 = document.createElement('td');
                    const cell2 = document.createElement('td');
                    const cell3 = document.createElement('td');
                    const cell4 = document.createElement('td');
                    cell1.textContent = result['name'];
                    cell2.textContent = result['volume'];
                    cell3.textContent = result['price'];
                    cell4.textContent = result['unit_price'];
                    row.appendChild(cell1);
                    row.appendChild(cell2);
                    row.appendChild(cell3);
                    row.appendChild(cell4);
                    tbody.appendChild(row);
                }
                table.appendChild(tbody);
            }

            attribute_to_table(asdaTable, asda_list);
            attribute_to_table(sainsTable, sains_list);
            attribute_to_table(tescoTable, tesco_list);

        })
        .catch(error => console.error(error));
}