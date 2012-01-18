<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="static/css/main.css" />

  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js">
  </script>
  <script type="text/javascript" src="static/js/hints.js">
  </script>
  
  <script type="text/javascript">
    var question_id = {{ question.tid.id }};
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

  <title>Regis: Dashboard for {{ user.username }}</title>
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
    {% if question.not_ready %}
      <h2 style="font-weight: normal"><b>Congrats!</b><br />You've finished all the questions that we have for you now.</h2>
      <p>We're constantly working on writing new questions...if you think you have an idea for one, feel free to email it to us!</p>
    {% else %}
      <h2 style="margin-bottom: 5px;">Challenge: <span style="font-weight: normal">{{ question.tid.q_title }} (#{{ question.tid.id }})</span></h2>
      <p style="font-size: small; margin-top: 0px; color: #666666;">A new question will be released in {{ ttl.hours }} hours and {{ ttl.minutes }} minutes.</p>
      {% if messages %}
        {% for m in messages %}
          {% if m.2 == True %}
          <p class="message">{{ m.0 }}</p>
          {% else %}
          <p class="message">{{ m.0 }}</p>
          {% endif %}
        {% endfor %}
      {% endif %}
      <p id="main_q">{{ question.decoded_text|safe }}</p>
      {% include 'include/qbox.tpl' %}
      <p id="hintzone">Want a hint?</p>
      <div id="hintdisplay"></div>
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
