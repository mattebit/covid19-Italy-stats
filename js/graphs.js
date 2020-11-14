const fillGraphs = async () => {
    // Fetchs all jsons
    var response = await fetch("js/datas/j_r_positivi_tamponi.json");
    const j_r_positivi_tamponi = await response.json(); 

    response = await fetch("js/datas/j_r_ricoverati_positivi.json");
    const j_r_ricoverati_positivi = await response.json(); 

    am4core.ready(function() {
        am4core.useTheme(am4themes_dataviz);
        am4core.useTheme(am4themes_animated);
        // Themes end
        
        // Create chart instance
        var c_positivi_tamponi = am4core.create("positivi_tamponi", am4charts.XYChart);
        
        // Create axes
        var dateAxis = c_positivi_tamponi.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 50;
        
        var valueAxis = c_positivi_tamponi.yAxes.push(new am4charts.ValueAxis());
        
        /* Create series */
        var columnSeries = c_positivi_tamponi.series.push(new am4charts.ColumnSeries());
        columnSeries.name = "positives";
        columnSeries.dataFields.valueY = "positives";
        columnSeries.dataFields.dateX = "date";

        //columnSeries.columns.template.tooltipText = "[#fff font-size: 15px]{name} in {categoryX}:\n[/][#fff font-size: 20px]{valueY}[/] [#fff]{additional}[/]"
        //columnSeries.columns.template.propertyFields.fillOpacity = "fillOpacity";
        //columnSeries.columns.template.propertyFields.stroke = "stroke";
        //columnSeries.columns.template.propertyFields.strokeWidth = "strokeWidth";
        //columnSeries.columns.template.propertyFields.strokeDasharray = "columnDash";
        columnSeries.columns.template.strokeOpacity = 0;
        
        var rValueAxis = c_positivi_tamponi.yAxes.push(new am4charts.ValueAxis());
        rValueAxis.renderer.opposite = true;
        //rValueAxis.min = 0;
        //rValueAxis.max = 100;
        rValueAxis.strictMinMax = true;
        rValueAxis.renderer.grid.template.disabled = true;
        rValueAxis.numberFormatter = new am4core.NumberFormatter();
        rValueAxis.numberFormatter.numberFormat = "#'%'"
        rValueAxis.cursorTooltipEnabled = false;

        // Create series
        var series = c_positivi_tamponi.series.push(new am4charts.LineSeries());
        series.name = "r"
        series.dataFields.valueY = "r";
        series.dataFields.dateX = "date";
        series.yAxis = rValueAxis
        series.strokeWidth = 2;
        series.minBulletDistance = 10;
        series.tooltipText = "{valueY}";
        series.tooltip.pointerOrientation = "vertical";
        series.tooltip.background.cornerRadius = 20;
        series.tooltip.background.fillOpacity = 0.5;
        series.tooltip.label.padding(12,12,12,12)
        
        
        // Add scrollbar
        c_positivi_tamponi.scrollbarX = new am4charts.XYChartScrollbar();
        c_positivi_tamponi.scrollbarX.series.push(columnSeries);
        
        // Add cursor
        c_positivi_tamponi.cursor = new am4charts.XYCursor();
        c_positivi_tamponi.cursor.xAxis = dateAxis;
        c_positivi_tamponi.cursor.snapToSeries = series;

        c_positivi_tamponi.data = j_r_positivi_tamponi;

        var c_ricoverati_positivi = am4core.create("ricoverati_positivi", am4charts.XYChart);
        c_ricoverati_positivi.data = j_r_ricoverati_positivi;
        
        // Create axes
        var dateAxis = c_ricoverati_positivi.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 50;
        
        var valueAxis = c_ricoverati_positivi.yAxes.push(new am4charts.ValueAxis());
        
        // Create series
        var series = c_ricoverati_positivi.series.push(new am4charts.LineSeries());
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
        c_ricoverati_positivi.scrollbarX = new am4charts.XYChartScrollbar();
        c_ricoverati_positivi.scrollbarX.series.push(series);
        
        // Add cursor
        c_ricoverati_positivi.cursor = new am4charts.XYCursor();
        c_ricoverati_positivi.cursor.xAxis = dateAxis;
        c_ricoverati_positivi.cursor.snapToSeries = series;
    });
}

fillGraphs()