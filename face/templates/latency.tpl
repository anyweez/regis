<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
    <script type="text/javascript" src="/static/js/underscore.js"></script>
<!---
-->
    <script type="text/javascript" src="/static/js/jquery.js"></script>
    <script type="text/javascript" src="/static/questions/jquery-ui-1.8.18.custom.min.js"></script>
    <script type="text/javascript" src="/static/js/jquery.layout.min-1.2.0.js"></script>
    <script type="text/javascript" src="/static/js/backbone.js"></script>
    <script type="text/javascript" src="/static/js/regis/regis.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      $.ajaxSetup({ timeout : 10000 });
      var results = $('#results');
      var total_countdown = 10;
      var countdown = total_countdown;
      var latencies = new Array();
      var display_stats = function () {
        var sum = 0;
        for (var i = 0; i < latencies.length; i += 1) {
          sum += latencies[i][1];
        }
        var average = sum / latencies.length;
        var item = '<li>Trials: ' + latencies.length + ', Average: ' + average + "ms</li>";
        results.append(item);
      }
      var do_test = function() {
        var starttime = new Date().getTime();
        $.get('/test/thirdpartylatency?url={{ url }}', function () {
          stoptime = new Date().getTime();
          countdown -= 1;
          var callindex = total_countdown - countdown;
          var latency = stoptime - starttime;
          latencies.push([callindex, latency]);
          var item = '<li>Index: ' + callindex + ', Time: ' + latency + "ms</li>";
          results.append(item);
          if (countdown > 0) {
             do_test();
          } else {
             display_stats();
          }
        });
      };
      do_test();
    });
  </script>
</head>
<body>
<ul id="results">

</ul>
</body>
</html>
