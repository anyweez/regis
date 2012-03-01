
var charts = new function() {
  this.make = function(target, chart_handler) {
    $.json('/summary/chart_view/request/' + chart_handler,
      function(response) {
        alert(response);
      }
    );
      var chart;
      chart = new Highcharts.Chart({
        chart: {
          renderTo: target,
          type: properties.type,
          marginRight: 130,
          marginBottom: 25
        },
        title: {
          text: properties.title,
          x: -20 //center
        },
        yAxis: {
          title: {
            text: 'Users'
          },
          min: 0,
          max: Math.max.apply(Math, ydata) + (.1 * Math.max.apply(Math, ydata)),
          plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
          }]
        },
        tooltip: {
          formatter: function() {
            return '<b>'+ this.series.name +'</b>: ' + this.y;
          }
        },
        series: [{
          name: 'Users',
          data: ydata
        }]
      });
  }
}
