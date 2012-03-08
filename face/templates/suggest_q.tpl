<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />

  <script type="text/javascript">
	function validate() {
		if ($("#question_suggestion").val().length == 0) {
			alert("Please enter a question before submitting");
			return false;
		}
	}
	
	$(document).ready(function() {
		$("#suggestbox").submit(validate);
	});	
  </script>
  {% include 'include/common_header.tpl' %}

  <title>Regis: Suggest a Question</title>
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
        <h2>Suggest a Question:</h2>
        {% include 'include/suggestbox.tpl' %}
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
