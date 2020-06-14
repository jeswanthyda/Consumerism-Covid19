function displayWorld(visualizationData) {
    
    google.charts.load('current', {'packages':['geochart'],'mapsApiKey': 'AIzaSyDSCQEH90fjMtJ5tlQF49YsRke1tf58TNA'});
    google.charts.setOnLoadCallback(drawRegionsMap);
    
    function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable(visualizationData);

        var options = {
            backgroundColor: '',
            colorAxis: {minValue: 0,  colors: ['#00ffd5', '#0066ff']}

        };

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

        chart.draw(data, options);
    }

}