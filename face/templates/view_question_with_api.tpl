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
  <script type="text/javascript" src="/static/js/questions.js">
  </script>
 
  <script type="text/javascript">
    var question_id = {{ tid }};
    // Fetch information about hints as soon as the page is loaded.
    $(document).ready(function() {
       questions.get(question_id, view_question_handler);
    });
  </script>
  
  <style type="text/css">
    #logbox {
      background-color: white;
      width: 38em;
      padding: 1%;
      margin: 0 auto;

      border: 3px solid black;
      border-radius: 3px;
    }
  </style>

  <title>Regis: View question</title>
</head>
<body>
	{% if errors %}
	<div class="error">
      {% for e in errors %}
      <p>{{ e }}</p>
      {% endfor %}
    </div>
    {% endif %}
    
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">
    <div id="question_body">  
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
