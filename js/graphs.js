const fillGraphs = async () => {
    // Fetchs all jsons
    const response = await fetch("js/datas/j_r_positivi_tamponi.json");
    const j_r_positivi_tamponi = await response.json(); 

    response = await fetch("js/datas/j_r_ricoverati_positivi.json");
    const j_r_ricoverati_positivi = await response.json(); 

    am4core.ready(function() {
        am4core.useTheme(am4themes_dataviz);
        am4core.useTheme(am4themes_animated);
        // Themes end
        
        // Create chart instance
        var c_positivi_tamponi = am4core.create("positivi_tamponi", am4charts.XYChart);
        c_positivi_tamponi.data = j_r_positivi_tamponi;
        
        // Create axes
        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 50;
        
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        
        // Create series
        var series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = "value";
        series.dataFields.dateX = "date";
        series.strokeWidth = 2;
        series.minBulletDistance = 10;
        series.tooltipText = "{valueY}";
        series.tooltip.pointerOrientation = "vertical";
        series.tooltip.background.cornerRadius = 20;
        series.tooltip.background.fillOpacity = 0.5;
        series.tooltip.label.padding(12,12,12,12)
        
        // Add scrollbar
        c_positivi_tamponi.scrollbarX = new am4charts.XYChartScrollbar();
        c_positivi_tamponi.scrollbarX.series.push(series);
        
        // Add cursor
        c_positivi_tamponi.cursor = new am4charts.XYCursor();
        c_positivi_tamponi.cursor.xAxis = dateAxis;
        c_positivi_tamponi.cursor.snapToSeries = series;

        var c_ricoverati_positivi = am4core.create("ricoverati_positivi", am4charts.XYChart);
        c_ricoverati_positivi.data = j_r_ricoverati_positivi;
        c_ricoverati_positivi.scrollbarX = new am4charts.XYChartScrollbar();
        c_ricoverati_positivi.scrollbarX.series.push(series)
        c_ricoverati_positivi.cursor = new am4charts.XYCursor();
        c_ricoverati_positivi.cursor.xAxis = dateAxis;
        c_ricoverati_positivi.cursor.snapToSeries = series;
    });
}

fillGraphs()