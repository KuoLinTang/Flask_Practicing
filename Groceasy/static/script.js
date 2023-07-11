$(document).ready(function () {
    $('.submit-item-name').click(function () {
        var item_name = $('#item-name').val();
        updateTables(item_name);
    });

    function updateTables(item_name) {
        $.ajax({
            url: '/scrap_items/',
            method: 'POST',
            data: { item_name: item_name },
            success: function (response) {
                console.log('get response');
                displayData(response);
            }
        });
    }
});

function displayData(data) {
    var asdaTable = $('#asda_results');
    var sainsTable = $('#sains_results');
    var tescoTable = $('#tesco_results');
    console.log('get table');

    var asda_list = data.asda_result;
    var sains_list = data.sains_result;
    var tesco_list = data.tesco_result;
    console.log('get result');
    console.log(asda_list);

    tableInsert(asda_list, asdaTable, 'ASDA');
    tableInsert(sains_list, sainsTable, 'Sainsbury');
    tableInsert(tesco_list, tescoTable, 'Tesco');
    console.log('update table');
}

function tableInsert(data, table, company) {
    table.empty();
    table.append($('<thead>').text(company));

    var tbody = $('<tbody>');
    // 使用迴圈將數據插入表格中
    for (var i = 0; i < data.length; i++) {
        var row = $('<tr>');
        row.append($('<td>').text(data['name']));
        row.append($('<td>').text(data['price']));
        row.append($('<td>').text(data['unit_price']));
        row.append($('<td>').text(data['volume']));
        tbody.append(row);
    }
    table.append(tbody);
}