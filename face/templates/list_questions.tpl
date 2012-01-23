<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  <title>Regis: Available Questions</title>
</head>
<body>
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">
    <div id="question_body">     
      <h2>Question List</h2>
      <p>The following questions are available in the system.  Additional questions will be released to you once
      you either solve a problem or work on it for 24 hours without solving it.</p>     
      {% for q in questions %}
        {% if q.status != 'pending' %}
        <div class="qbox">
		  
		  {% if q.status == 'ready' %}
		  <div class="q_decoration q_unavailable">
		    <p class="q_status">locked</p>
		  {% endif %}
		  {% if q.status == 'released' %}
		  <div class="q_decoration q_unanswered">
		    <p class="q_status">unsolved</p>
		  {% endif %}
		  {% if q.status == 'solved' %}
		  <div class="q_decoration q_answered">
		    <p class="q_status">solved</p>
		  {% endif %} 
		  
		    <p>solved by 2 of 8</p>
		    <p>( 25% )</p>
		  </div>
          <div>
            {% if q.status == 'ready' %}
              <h2 class="qbox_head">Question #{{ q.tid.id }}: {{ q.tid.q_title }}</h2>
              <p class="qbox_preview" style="font-style: italic">This question isn't available yet.</p>
            {% else %}
              <h2 class="qbox_head">Question #{{ q.tid.id }}: <a href="{{q.tid.id}}/">{{ q.tid.q_title }}</a></h2>
              {% if q.text|length > 60 %}
                <p class="qbox_preview">{{ q.text|slice:":200" }}...</p>
              {% else %}
                <p class="qbox_preview">{{ q.text }}</p>
              {% endif %}
            {% endif %}
            

          </div>
        </div>
        {% endif %}
      {% endfor %}
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
