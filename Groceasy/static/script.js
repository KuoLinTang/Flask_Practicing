$(document).ready(function () {

    $('#submit-button').click(function (event) {
        event.preventDefault();
        updateTables();
    });

    $('#item-name').keypress(function (event) {
        if (event.which === 13) { // 按下的是Enter鍵
            event.preventDefault(); // 阻止表單的預設提交行為
            updateTables();
        }
    });
});

function updateTables() {
    var item_name = $('#item-name').val();  // Get item name from the input box

    $.ajax({
        url: '/scrap_items/',
        method: 'POST',
        data: { item_name: item_name },
        beforeSend: function () {
            hideInvalidItem();
            showLoadingSpinner(); // 请求发送前显示加载图标
        },
        success: function (response, textStatus, xhr) {

            console.log('get responses');
            console.log(textStatus);
            hideLoadingSpinner();  // hide loading spinner

            displayData(response);
        },
        error: function (xhr, textStatus, error) {
            hideLoadingSpinner();
            showInvalidItem();

            // 执行错误的逻辑
            console.log('Error:', textStatus, error);
        }
    });
}

function displayData(data) {
    var asdaTable = $('#asda_results');
    var sainsTable = $('#sains_results');
    var tescoTable = $('#tesco_results');
    console.log('get table');

    var asda_list = data.asda_result;
    var sains_list = data.sains_result;
    var tesco_list = data.tesco_result;
    console.log('get result');

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
        row.append($('<td>').text(data[i]['name']));
        row.append($('<td>').text(data[i]['price']));
        row.append($('<td>').text(data[i]['unit_price']));
        row.append($('<td>').text(data[i]['volume']));
        tbody.append(row);
    }
    table.append(tbody);
}


function showLoadingSpinner() {
    $('#loadingSpinner').show(); // 显示加载图标
}

function hideLoadingSpinner() {
    $('#loadingSpinner').hide(); // 隐藏加载图标
}

function showInvalidItem() {
    $('#invalidItem').show(); // 显示加载图标
}

function hideInvalidItem() {
    $('#invalidItem').hide(); // 隐藏加载图标
}