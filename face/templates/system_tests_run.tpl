<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  
  {% include 'include/common_header.tpl' %}
  
  <script type="text/javascript" src="/static/js/api.js">
  </script>
  <title>Regis: View question</title>
</head>
<body>
    
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">
    <div id="test_body">
      {% for testinfo in tests %}
      {% with testname=testinfo.0 test=testinfo.1 jsinfo=testinfo.2 %}
        <div class="testresult">
          <b>
            {{ testname }}
          </b>
          {% with "tests/"|add:test|add:".tpl" as test_template %}
          {% include test_template %}
          {% endwith %}
        </div>
      {% endwith %}
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
