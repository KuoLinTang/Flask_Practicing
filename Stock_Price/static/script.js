// Create a function to go back to the last page
function goBack() {
    history.go(-1);
    $.ajax({
        url: '/initialise-variables/',
        method: 'POST',
        data: {}
    })
}

// Create a function that allows to update the period of plots when button clicked
$(document).ready(function () {
    $('.update-period-btn').click(function () {
        var timePeriod = $(this).data('period');
        updateChartPeriod(timePeriod);
    });

    function updateChartPeriod(period) {
        $.ajax({
            url: '/stock/update_plot_period/',
            method: 'POST',
            data: { period: period },
            success: function (response) {
                $('#line-chart').attr('src', 'data:image/png;base64,' + response.plot_data);
                $('#current-price').text('Current Price: ' + response.current_price + ' USD');
                $('#price-diff').text('Gain: ' + response.price_diff);
            }
        });
    }
});

// Create a function that allows to update the measure of plots when button clicked
$(document).ready(function () {
    $('.update-measure-btn').click(function () {
        var measure = $(this).data('measure');
        updateChartMeasure(measure);
    });

    function updateChartMeasure(measure) {
        $.ajax({
            url: '/stock/update_plot_measure/',
            method: 'POST',
            data: { measure: measure },
            success: function (response) {
                $('#line-chart').attr('src', 'data:image/png;base64,' + response.plot_data);
                $('#current-price').text('Current Price: ' + response.current_price + ' USD');
                $('#price-diff').text('Gain: ' + response.price_diff);
            }
        });
    }
});

// Create a function to update range of the table when button clicked
$(document).ready(function () {
    $('.table-page').click(function () {
        // get page action from button
        var action = $(this).data('go');
        updateTableRange(action);
    });

    function updateTableRange(action) {
        $.ajax({
            url: '/stock/update_table/',
            method: 'POST',
            data: { action: action },
            success: function (response) {
                $('#table-left').html(response.table_left);
                $('#table-right').html(response.table_right);
            }
        });
    }
});


// Create a function to scroll back to the top
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    var backToTopBtn = document.getElementById("backToTopBtn");
    // when the page is scrolled over 100 px then the button will appear
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        backToTopBtn.style.display = "block";
    } else {
        backToTopBtn.style.display = "none";
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}