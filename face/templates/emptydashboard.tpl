{% comment %}
Requres

question_id
{% endcomment %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  
  {% include 'include/common_header.tpl' %}
  
  <!--- <script type="text/javascript" src="/static/js/api.js"></script> -->

  <title>Regis: View question</title>
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
        <h2>
          <b>Congrats!</b><br />
          You've finished all the questions that we have for you now.
        </h2>
        <p>We're constantly working on writing new questions...if you think you have an idea for one, feel free to email it to us!</p>
      </div>  
      {% include 'include/sidebar.tpl' %}
      <div style="clear: both; height: 0px;">&nbsp;</div>
    </div> <!--  end middle_container -->
  
    <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    </div>
  </div> 
</body>
</html>
