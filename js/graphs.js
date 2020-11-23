(function ($) {

    "use strict";

    var fullHeight = function () {

        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function () {
            $('.js-fullheight').css('height', $(window).height());
        });

    };
    fullHeight();
})(jQuery);

document.getElementById("sidebarCollapse").onclick = () => {

    var sidebar = document.getElementById("sidebar");

    function updategraphs() {
        c_positivi_tamponi.svgContainer.measure();
        c_ricoverati_positivi.svgContainer.measure();
        c_terapia_ospedalizzati.svgContainer.measure();
        c_decessi_20_decessi_15_18.svgContainer.measure();
        c_decessi_covid_decessi_20.svgContainer.measure();
        c_dimessi_guariti_nuovi_positivi.svgContainer.measure();
        c_dimessi_guariti_attualmente_positivi.svgContainer.measure();
        c_deaths_positives.svgContainer.measure();
        c_nuovi_positivi_usciti.svgContainer.measure();
        c_intensive_variation.svgContainer.measure();
    }
    // Code for Chrome, Safari and Opera
    sidebar.addEventListener("webkitTransitionEnd", updategraphs);

    // Standard syntax
    sidebar.addEventListener("transitionend", updategraphs);

    sidebar.classList.toggle('active');
}

document.getElementById("sidebar").classList.toggle('active');

// Create chart instance
var c_positivi_tamponi = undefined
var c_ricoverati_positivi = undefined
var c_terapia_ospedalizzati = undefined
var c_decessi_20_decessi_15_18 = undefined
var c_decessi_covid_decessi_20 = undefined
var c_dimessi_guariti_nuovi_positivi = undefined
var c_dimessi_guariti_attualmente_positivi = undefined
var c_deaths_positives = undefined
var c_nuovi_positivi_usciti = undefined
var c_intensive_variation = undefined

const fillGraphs = async () => {
    // Fetchs all jsons
    fetch("js/datas/j_r_positivi_tamponi.json")
        .then(response => response.json())
        .then(data => plot_c_positivi_tamponi(data))

    fetch("js/datas/j_r_ricoverati_positivi.json")
        .then(response => response.json())
        .then(data => plot_c_ricoverati_positivi(data));

    fetch("js/datas/j_r_terapia_ospedalizzati.json")
        .then(response => response.json())
        .then(data => plot_c_terapia_ospedalizzati(data));

    fetch("js/datas/j_r_decessi_20_decessi_15_18.json")
        .then(response => response.json())
        .then(data => plot_c_decessi_20_decessi_15_18(data))

    fetch("js/datas/j_r_decessi_covid_decessi_20.json")
        .then(response => response.json())
        .then(data => plot_c_decessi_covid_decessi_20(data))

    fetch("js/datas/j_r_dimessi_guariti_nuovi_positivi.json")
        .then(response => response.json())
        .then(data => plot_c_dimessi_guariti_nuovi_positivi(data))

    fetch("js/datas/j_r_dimessi_guariti_attualmente_positivi.json")
        .then(response => response.json())
        .then(data => plot_c_dimessi_guariti_attualmente_positivi(data))

    fetch("js/datas/j_r_deaths_positives.json")
        .then(response => response.json())
        .then(data => plot_c_deaths_positives(data))

    fetch("js/datas/j_r_nuovi_positivi_usciti.json")
        .then(response => response.json())
        .then(data => plot_c_nuovi_positivi_usciti(data))

    fetch("js/datas/j_intensive_variation.json")
        .then(response => response.json())
        .then(data => plot_c_intensive_variation(data))

    am4core.ready(function () {
        am4core.useTheme(am4themes_dataviz);
        //am4core.useTheme(am4themes_animated);
        // Themes end
    });
}

function plot_c_positivi_tamponi(data) {
    c_positivi_tamponi = am4core.create("positivi_tamponi", am4charts.XYChart);

    // Create axes
    var dateAxis = c_positivi_tamponi.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_positivi_tamponi.yAxes.push(new am4charts.ValueAxis());

    /* Create series */
    var columnSeries = c_positivi_tamponi.series.push(new am4charts.ColumnSeries());
    columnSeries.name = "daily positives";
    columnSeries.dataFields.valueY = "positives";
    columnSeries.dataFields.dateX = "date";


    //columnSeries.columns.template.tooltipText = "[#fff font-size: 15px]{name} in {categoryX}:\n[/][#fff font-size: 20px]{valueY}[/] [#fff]{additional}[/]"
    //columnSeries.columns.template.propertyFields.fillOpacity = "fillOpacity";
    //columnSeries.columns.template.propertyFields.stroke = "stroke";
    //columnSeries.columns.template.propertyFields.strokeWidth = "strokeWidth";
    //columnSeries.columns.template.propertyFields.strokeDasharray = "columnDash";
    columnSeries.columns.template.strokeOpacity = 1;

    var rValueAxis = c_positivi_tamponi.yAxes.push(new am4charts.ValueAxis());
    rValueAxis.renderer.opposite = true;
    //rValueAxis.min = 0;
    //rValueAxis.max = 100;
    rValueAxis.strictMinMax = true;
    rValueAxis.renderer.grid.template.disabled = true;
    rValueAxis.numberFormatter = new am4core.NumberFormatter();
    rValueAxis.numberFormatter.numberFormat = "#'%'"
    rValueAxis.cursorTooltipEnabled = true;

    // Create series
    var series = c_positivi_tamponi.series.push(new am4charts.LineSeries());
    series.name = "ratio"
    series.dataFields.valueY = "r";
    series.dataFields.dateX = "date";
    series.yAxis = rValueAxis
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)


    // Add scrollbar
    c_positivi_tamponi.scrollbarX = new am4charts.XYChartScrollbar();
    c_positivi_tamponi.scrollbarX.series.push(columnSeries);

    // Add cursor
    c_positivi_tamponi.cursor = new am4charts.XYCursor();
    c_positivi_tamponi.cursor.xAxis = dateAxis;
    c_positivi_tamponi.cursor.snapToSeries = series;

    c_positivi_tamponi.legend = new am4charts.Legend();
    c_positivi_tamponi.svgContainer.autoResize = false;
    c_positivi_tamponi.data = data;
}

function plot_c_ricoverati_positivi(data) {
    c_ricoverati_positivi = am4core.create("ricoverati_positivi", am4charts.XYChart);
    c_ricoverati_positivi.data = data;

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
    series.numberFormatter.numberFormat = "#'%'"
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)

    // Add scrollbar
    c_ricoverati_positivi.scrollbarX = new am4charts.XYChartScrollbar();
    c_ricoverati_positivi.scrollbarX.series.push(series);

    // Add cursor
    c_ricoverati_positivi.cursor = new am4charts.XYCursor();
    c_ricoverati_positivi.cursor.xAxis = dateAxis;
    c_ricoverati_positivi.cursor.snapToSeries = series;
    c_ricoverati_positivi.svgContainer.autoResize = false;
}

function plot_c_terapia_ospedalizzati(data) {
    c_terapia_ospedalizzati = am4core.create("c_terapia_ospedalizzati", am4charts.XYChart);
    c_terapia_ospedalizzati.data = data;

    // Create axes
    var dateAxis = c_terapia_ospedalizzati.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_terapia_ospedalizzati.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_terapia_ospedalizzati.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_terapia_ospedalizzati.scrollbarX = new am4charts.XYChartScrollbar();
    c_terapia_ospedalizzati.scrollbarX.series.push(series);

    // Add cursor
    c_terapia_ospedalizzati.cursor = new am4charts.XYCursor();
    c_terapia_ospedalizzati.cursor.xAxis = dateAxis;
    c_terapia_ospedalizzati.cursor.snapToSeries = series;
    c_terapia_ospedalizzati.svgContainer.autoResize = false;
}

function plot_c_decessi_20_decessi_15_18(data) {
    c_decessi_20_decessi_15_18 = am4core.create("c_decessi_20_decessi_15_18", am4charts.XYChart);
    c_decessi_20_decessi_15_18.data = data;

    // Create axes
    var dateAxis = c_decessi_20_decessi_15_18.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_decessi_20_decessi_15_18.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_decessi_20_decessi_15_18.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_decessi_20_decessi_15_18.scrollbarX = new am4charts.XYChartScrollbar();
    c_decessi_20_decessi_15_18.scrollbarX.series.push(series);

    // Add cursor
    c_decessi_20_decessi_15_18.cursor = new am4charts.XYCursor();
    c_decessi_20_decessi_15_18.cursor.xAxis = dateAxis;
    c_decessi_20_decessi_15_18.cursor.snapToSeries = series;
    c_decessi_20_decessi_15_18.svgContainer.autoResize = false;
}

function plot_c_decessi_covid_decessi_20(data) {
    c_decessi_covid_decessi_20 = am4core.create("c_decessi_covid_decessi_20", am4charts.XYChart);
    c_decessi_covid_decessi_20.data = data;

    // Create axes
    var dateAxis = c_decessi_covid_decessi_20.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_decessi_covid_decessi_20.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_decessi_covid_decessi_20.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_decessi_covid_decessi_20.scrollbarX = new am4charts.XYChartScrollbar();
    c_decessi_covid_decessi_20.scrollbarX.series.push(series);

    // Add cursor
    c_decessi_covid_decessi_20.cursor = new am4charts.XYCursor();
    c_decessi_covid_decessi_20.cursor.xAxis = dateAxis;
    c_decessi_covid_decessi_20.cursor.snapToSeries = series;
    c_decessi_covid_decessi_20.svgContainer.autoResize = false;
}

function plot_c_dimessi_guariti_nuovi_positivi(data) {
    c_dimessi_guariti_nuovi_positivi = am4core.create("c_dimessi_guariti_nuovi_positivi", am4charts.XYChart);
    c_dimessi_guariti_nuovi_positivi.data = data;

    // Create axes
    var dateAxis = c_dimessi_guariti_nuovi_positivi.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_dimessi_guariti_nuovi_positivi.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_dimessi_guariti_nuovi_positivi.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_dimessi_guariti_nuovi_positivi.scrollbarX = new am4charts.XYChartScrollbar();
    c_dimessi_guariti_nuovi_positivi.scrollbarX.series.push(series);

    // Add cursor
    c_dimessi_guariti_nuovi_positivi.cursor = new am4charts.XYCursor();
    c_dimessi_guariti_nuovi_positivi.cursor.xAxis = dateAxis;
    c_dimessi_guariti_nuovi_positivi.cursor.snapToSeries = series;
    c_dimessi_guariti_nuovi_positivi.svgContainer.autoResize = false;
}

function plot_c_dimessi_guariti_attualmente_positivi(data) {
    c_dimessi_guariti_attualmente_positivi = am4core.create("c_dimessi_guariti_attualmente_positivi", am4charts.XYChart);
    c_dimessi_guariti_attualmente_positivi.data = data;

    // Create axes
    var dateAxis = c_dimessi_guariti_attualmente_positivi.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_dimessi_guariti_attualmente_positivi.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_dimessi_guariti_attualmente_positivi.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_dimessi_guariti_attualmente_positivi.scrollbarX = new am4charts.XYChartScrollbar();
    c_dimessi_guariti_attualmente_positivi.scrollbarX.series.push(series);

    // Add cursor
    c_dimessi_guariti_attualmente_positivi.cursor = new am4charts.XYCursor();
    c_dimessi_guariti_attualmente_positivi.cursor.xAxis = dateAxis;
    c_dimessi_guariti_attualmente_positivi.cursor.snapToSeries = series;
    c_dimessi_guariti_attualmente_positivi.svgContainer.autoResize = false;
}

function plot_c_deaths_positives(data) {
    c_deaths_positives = am4core.create("c_deaths_positives", am4charts.XYChart);
    c_deaths_positives.data = data;

    // Create axes
    var dateAxis = c_deaths_positives.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_deaths_positives.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_deaths_positives.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_deaths_positives.scrollbarX = new am4charts.XYChartScrollbar();
    c_deaths_positives.scrollbarX.series.push(series);

    // Add cursor
    c_deaths_positives.cursor = new am4charts.XYCursor();
    c_deaths_positives.cursor.xAxis = dateAxis;
    c_deaths_positives.cursor.snapToSeries = series;
    c_deaths_positives.svgContainer.autoResize = false;
}

function plot_c_nuovi_positivi_usciti(data) {
    c_nuovi_positivi_usciti = am4core.create("c_nuovi_positivi_usciti", am4charts.XYChart);
    c_nuovi_positivi_usciti.data = data;

    // Create axes
    var dateAxis = c_nuovi_positivi_usciti.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_nuovi_positivi_usciti.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_nuovi_positivi_usciti.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_nuovi_positivi_usciti.scrollbarX = new am4charts.XYChartScrollbar();
    c_nuovi_positivi_usciti.scrollbarX.series.push(series);

    // Add cursor
    c_nuovi_positivi_usciti.cursor = new am4charts.XYCursor();
    c_nuovi_positivi_usciti.cursor.xAxis = dateAxis;
    c_nuovi_positivi_usciti.cursor.snapToSeries = series;
    c_nuovi_positivi_usciti.svgContainer.autoResize = false;
}


function plot_c_intensive_variation(data) {
    c_intensive_variation = am4core.create("c_intensive_variation", am4charts.XYChart);
    c_intensive_variation.data = data;

    // Create axes
    var dateAxis = c_intensive_variation.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;

    var valueAxis = c_intensive_variation.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = c_intensive_variation.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 1;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.numberFormatter.numberFormat = "#'%'"

    // Add scrollbar
    c_intensive_variation.scrollbarX = new am4charts.XYChartScrollbar();
    c_intensive_variation.scrollbarX.series.push(series);

    // Add cursor
    c_intensive_variation.cursor = new am4charts.XYCursor();
    c_intensive_variation.cursor.xAxis = dateAxis;
    c_intensive_variation.cursor.snapToSeries = series;
    c_intensive_variation.svgContainer.autoResize = false;

    // Create a range to change stroke for values below 0
    var range = valueAxis.createSeriesRange(series);
    range.value = 0;
    range.endValue = -1000;
    range.contents.stroke = c_intensive_variation.colors.getIndex(4);
    range.contents.fill = range.contents.stroke;
    range.contents.strokeOpacity = 0.7;
    range.contents.fillOpacity = 0.1;

    series.tooltip.getFillFromObject = false;
    series.tooltip.adapter.add("x", (x, target) => {
        if (series.tooltip.tooltipDataItem.valueY < 0) {
            series.tooltip.background.fill = c_intensive_variation.colors.getIndex(4);
        }
        else {
            series.tooltip.background.fill = c_intensive_variation.colors.getIndex(0);
        }
        return x;
    })
}


fillGraphs()