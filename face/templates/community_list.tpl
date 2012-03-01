<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  {% include 'include/common_header.tpl' %}

  <script type="text/javascript" src="/static/js/hints.js">
  </script>
  <script type="text/javascript" src="/static/js/api.js">
  </script>

  <script type="text/javascript">
    $(document).ready(function() {
       api.community.questions.list(list_questions_handler);
    });
    function list_questions_handler(data) {
      for (var i = 0; i < data.items.length; i++) {
        $('#question_body').append(data.items[i].html);
      }
    }
  </script>
  <title>Regis: Community Questions</title>
  
  
  <style type="text/css">
    #right_col {
      border-bottom: 3px solid black;
      border-radius: 0px 0px 0px 5px; 
    }
  </style>
</head>
<body>
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">

    <div id="navigation">
      <ul>
        <li><a href="/community/add">submit a question</a></li>
      </ul>
    </div>

    <div id="question_body">     
      <h2>Community Question List</h2>   
    </div>  
    {% include 'include/sidebar.tpl' %}
  <div style="clear: both; height: 0px;">&nbsp;</div>
  </div> <!--  end main_body -->

  <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    </div>
</div> 
  </div>
</body>
</html>
