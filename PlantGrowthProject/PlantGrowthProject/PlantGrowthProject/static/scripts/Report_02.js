
function getData() {

    var deferredData = new jQuery.Deferred();

    $.ajax({
        type: "GET",
        url: "/ajax",
        dataType: "json",
        success: function (data) {
            deferredData.resolve(data);
        },
        complete: function (xhr, textStatus) {
            console.log("AJAX Request complete -> ", xhr, " -> ", textStatus);
        },
        error: function () {
            $("#myModal").modal();
            console.log("Error occur");
        }
    });

    return deferredData; // contains the passed data
};
// I used the Deferred structure below because I later added Deferred objects from other asynchronous functions to the `.when`

var dataDeferred = getData();
var DataLabels = [];
var DataArray = [];

function checkAjaxStatuses() {
    var pending = [];
    var successes = [];
    var errors = [];
    for (var i = 0; i < resp.propertiesList.length; i++) {
        if (resp.propertiesList[i].ajaxStatus === 'pending') {
            pending.push(resp.propertiesList[i]);
        }
        if (resp.propertiesList[i].ajaxStatus === 'success') {
            successes.push(resp.propertiesList[i]);
        }
        if (resp.propertiesList[i].ajaxStatus.indexOf('error') !== -1) {
            errors.push(resp.propertiesList[i]);
        }
    }

    console.log('ajax completed.');
    console.log(pending.length + ' pending.');
    console.log(successes.length + ' succeeded.');
    console.log(errors.length + ' failed.');
}

$.when(dataDeferred).done(function (data) {
    console.log("Okay");

    for (i = 0; i < data.nBlackPixelArrylst.length; i++) {
        var DataItem = (data.nBlackPixelArrylst[i] / data.nAllPixelArrylst[i])*data.FrameSize;
        DataArray.push(DataItem);
        var LabelItem = "Image " + i;
        DataLabels.push(LabelItem);
    }
    LoadChart();
});

function LoadChart() {
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: DataLabels,
            datasets: [{
                label: 'Growth area',
                data: DataArray,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}


