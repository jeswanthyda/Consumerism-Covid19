function plotLineChart(plot_params,plotID) {
    
    document.getElementById(plotID).innerHTML="";
    var ctx = document.getElementById(plotID);
    var industryLine = document.getElementById('industryLine')
    var industryIndex = parseInt(industryLine.options[industryLine.selectedIndex].value,10)
    console.log(industryIndex)
    var data = {
        labels: plot_params['labels'],
        datasets: [plot_params['datasets'][industryIndex]]
    }
    console.log(plot_params['datasets'][industryIndex])

    var options = {
        scales: {
            yAxes: [{
                ticks: {
                    min: -1.1,
                    max: 1.1
                },
            }]
        }
    }

    var myChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: options
    });
}

