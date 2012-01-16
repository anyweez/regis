<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="http://localhost:8000/static/css/main.css" />

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

  <title>Regis: Viewing question {{ question.title }}</title>
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
      {% if question.status != 'pending' and question.status != 'ready' %}         
      <h2 style="margin-bottom: 5px;">Question #{{question.tid.id}}: <span style="font-weight: normal">{{ question.tid.q_title }}</span></h2>
      <p style="color: #555; margin: 0px 0px 10px 3px; padding: 0;">released on {{ question.time_released }}</p>
      <p id="main_q">{{ question.text }}</p>
      {% include 'include/qbox.tpl' %}
      
      {% else %}
      <h2 style="margin-bottom: 5px;">Sorry!</h2>
      <p>You haven't unlocked this question yet.  Keep working and you'll get it in no time!</p>
      {% endif %}
      
      
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
