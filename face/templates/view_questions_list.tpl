<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  {% include 'include/common_header.tpl' %}

  <script type="text/javascript" src="/static/js/api.js">
  </script>

  <script type="text/javascript">
    $(document).ready(function() {
       api.questions.list(list_questions_handler);
/*
       $(window).resize(function () {
          var h = Math.min($(window).height(), 500);
          $('#right_column').css('height', h + 'px');
          $('#right_column').css('position', 'fixed');
          $('#right_column').css('right', '0px');
       });
*/
    });

    function list_questions_handler(data) {
      for (var i = 0; i < data.items.length; i++) {
        $('#center_body').append(data.items[i].html);
      }
    }
  </script>
  <title>Regis: Available Questions</title>
  
  
  </style>
</head>
<body>
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="middle_container">
    <div id="left_body">
&nbsp;
    </div>
    <div id="center_body">
      <h2>Question List</h2>
      <p>The following questions are available in the system.  Additional questions will be released to you once
      you either solve a problem or work on it for 48 hours without solving it.</p>     
    </div>  
    {% include 'include/sidebar.tpl' %}
    <div style="clear: both; height: 0px;">&nbsp;</div>
  </div> <!--  end middle_container -->

  <!-- Container for the information that appears below the main content (i.e. licensing info). -->
  <div id="footer">
  </div>
</div> 
  </div>
</body>
</html>
