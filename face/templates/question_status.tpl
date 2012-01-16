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

  <title>Regis: {{ question.tid.q_title }} [status]</title>
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
      
      {% if question.status == 'solved' %}
      <h2 style="margin-bottom: 5px; font-weight: normal"><b>Correct!</b></h2>
      <p><b>{{ guess.value }}</b> was the correct answer to this puzzle.  Nice work!</p>
      {% endif %}
      
      {% if question.status == 'released' %}
      <h2 style="margin-bottom: 5px; font-weight: normal">Sorry, that's not correct.</h2>
      <p>You guessed <b>{{ guess.value }}</b> but unfortunately that's not the correct answer.</p>
      
        {% if answer %}
        {{ answer.message }}
        {% endif %}
      
      <p>Care to <a href="http://localhost:8000/question/view/{{question.tid.id}}">try again</a>?</p>
      {% endif %}
      
      {% if question.status == 'ready' or question.status == 'pending' %}
      <h2 style="margin-bottom: 5px; font-weight: normal">{{ question.tid.q_title}}: Question Unavailable</h2>
      <p>This question isn't available to you yet, and it's amazing that you were able to make a guess at it.</p>
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
