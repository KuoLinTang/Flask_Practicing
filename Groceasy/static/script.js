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
    showLoadingSpinner();  // display loading spinner
    var item_name = $('#item-name').val();  // Get item name from the input box

    $.ajax({
        url: '/scrap_items/',
        method: 'POST',
        data: { item_name: item_name },
        success: function (response, textStatus, xhr) {

            var status_code = xhr.status_code;

            console.log('get responses');
            hideLoadingSpinner();  // hide loading spinner
            console.log(status_code);

            if (status_code === 200) {
                displayData(response);
            } else {
                throw 'Undefined status code';
            }
        },
        error: function (error) {
            hideLoadingSpinner();
            console.log(error);
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