function displayWorld(visualizationData) {
    
    var key = 'ADD Google Maps Java Script API KEY HERE'
    google.charts.load('current', {'packages':['geochart'],'mapsApiKey': key});
    google.charts.setOnLoadCallback(drawRegionsMap);
    
    function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable(visualizationData);

        var options = {
            backgroundColor: '',
            colorAxis: {  colors: ['#9ecae1', '3182bd']}

        };

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

        chart.draw(data, options);
    }

}
