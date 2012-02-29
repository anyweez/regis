<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  {% include 'include/common_header.tpl' %}

  <title>Regis: about</title>
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
        <h2>About Regis</h2>
        <p>
         This can say whatever you want, but please provide a link back to 
         <a href="https://github.com/luke-segars/regis">Regis</a> somewhere. 
        </p>
      </div>  
{% comment %}      {% include 'include/sidebar.tpl' %} {% endcomment %}
      <div style="clear: both; height: 0px;">&nbsp;</div>
    </div> <!--  end middle_container -->
  
    <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    </div>
  </div> 
</body>
</html>
