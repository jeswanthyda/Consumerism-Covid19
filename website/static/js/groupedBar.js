function plotGroupedBar(plot_params,plotID,yTick=true){
    
    var ctx = document.getElementById(plotID);
    
    var data = {
        labels: plot_params['labels'],
        datasets: [
            {
                label: "cluster_0",
                data: plot_params['cluster_0'],
                backgroundColor: "blue"
            },
            {
                label: "cluster_1",
                data: plot_params['cluster_1'],
                backgroundColor: "red"
            }
        ]
    };
    
    var myBarChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            barValueSpacing: 20,
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0,
                    }
                }],
                yAxes: [{
                    ticks: {
                        display: yTick
                    }
                }]
            }
        }
    });
}
