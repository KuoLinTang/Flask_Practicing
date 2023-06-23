// Create a function to go back to the last page
function goBack() {
    history.go(-1);
    $.ajax({
        url: '/initialise-variables/',
        method: 'POST',
        data: {}
    })
}

// Create a function that allows to update period of plots with button clicked
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
            success: function (data) {
                $('#line-chart').attr('src', 'data:image/png;base64,' + data.plot_data);
            }
        });
    }
});

// Create a function that allows to update period of plots with button clicked
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
            success: function (data) {
                $('#line-chart').attr('src', 'data:image/png;base64,' + data.plot_data);
                $()
            }
        });
    }
});


// Create a function to scroll back to the top
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    var backToTopBtn = document.getElementById("backToTopBtn");
    // when the page is scrolled over 40 px then the button will appear
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopBtn.style.display = "block";
    } else {
        backToTopBtn.style.display = "none";
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}