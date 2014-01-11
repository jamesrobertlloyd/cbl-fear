google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

// this has to be a global function
function drawChart() {
   // grab the CSV
   $.get("data/ping.csv", function(csvString) {
      // transform the CSV string into a 2-dimensional array
      var arrayData = $.csv.toArrays(csvString, {onParseValue: $.csv.hooks.castToScalar});

      // this new DataTable object holds all the data
      var data = new google.visualization.arrayToDataTable(arrayData);

      // this view can select a subset of the data at a time
      var view = new google.visualization.DataView(data);
      view.setColumns([0,1]);

     // set chart options
     var options = {
        title: "Average ping time (s)",
        hAxis: {title: data.getColumnLabel(1), minValue: 0, maxValue: data.getColumnRange(1).max},
        vAxis: {title: data.getColumnLabel(0)},
        legend: 'none'
     };

     // create the chart object and draw it
     var chart = new google.visualization.BarChart(document.getElementById('chart-ping'));
     chart.draw(view, options);
  });
   $.get("data/cpus.csv", function(csvString) {
      // transform the CSV string into a 2-dimensional array
      var arrayData = $.csv.toArrays(csvString, {onParseValue: $.csv.hooks.castToScalar});

      // this new DataTable object holds all the data
      var data = new google.visualization.arrayToDataTable(arrayData);

      // this view can select a subset of the data at a time
      var view = new google.visualization.DataView(data);
      view.setColumns([0,1]);

     // set chart options
     var options = {
        title: "CPU usage (%)",
        hAxis: {title: data.getColumnLabel(1), minValue: 0, maxValue: 100},
        vAxis: {title: data.getColumnLabel(0)},
        legend: 'none'
     };

     // create the chart object and draw it
     var chart = new google.visualization.BarChart(document.getElementById('chart-cpu'));
     chart.draw(view, options);
  });
   $.get("data/bench.csv", function(csvString) {
      // transform the CSV string into a 2-dimensional array
      var arrayData = $.csv.toArrays(csvString, {onParseValue: $.csv.hooks.castToScalar});

      // this new DataTable object holds all the data
      var data = new google.visualization.arrayToDataTable(arrayData);
      /*data.SetColumnProperty(2, 'role', 'tooltip')*/

      // this view can select a subset of the data at a time
      /*var view = new google.visualization.DataView(data);
      view.setColumns([0,1]);
      view.setColumns([0,1,2,{calc:function (dataTable, rowNum){return dataTable.getValue(rowNum, 2)}, type:'string', role:'tooltip'}]);*/
      var view = new google.visualization.DataView(data);
      view.setColumns([0,1]);

     // set chart options
     var options = {
        title: "Time taken to complete a benchmark",
        hAxis: {title: 'Date'},
        vAxis: {title: 'Benchmark time'},
        legend: 'none'
     };

     // create the chart object and draw it
     var chart = new google.visualization.LineChart(document.getElementById('chart-bench'));
     chart.draw(view, options);
  });
}

$(document).ready(function() {
    $('#CSVTableDeadPing').CSVToTable('data/dead-ping.csv', { loadingImage: 'images/kitten-100-100.jpeg', startLine: 0 });
    $('#CSVTableDeadUsers').CSVToTable('data/dead-users.csv', { loadingImage: 'images/kitten-100-100.jpeg', startLine: 0 });
    /*$('#CSVTablePing').CSVToTable('data/ping.csv', { loadingImage: 'images/kitten-100-100.jpeg', startLine: 0 });*/
    $('#CSVTableDeadSsh').CSVToTable('data/dead-ssh.csv', { loadingImage: 'images/kitten-100-100.jpeg', startLine: 0 });
    /*$('#CSVTableCPU').CSVToTable('data/cpus.csv', { loadingImage: 'images/kitten-100-100.jpeg', startLine: 0 });*/
});