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

  {% if question %}
  <script type="text/javascript">
    var question_id = {{ question.template.id }};

    // Fetch information about hints as soon as the page is loaded.
    $(document).ready(function() {
      get_hints(question_id);
//      questions.get(question_id, view_question_handler);
    });
  </script>
  {% endif %}
  
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

  <title>Regis: Administration and Analytics Panel</title>
</head>
<body>    
  <!-- The heading, which contains the title and appears above everything else. -->
  <div id="display_body">   
    {% include 'include/heading.tpl' %}
    
  <!-- Container for the majority of the page's content. -->
  <div id="main_body">
    <div id="question_body"> 
      <h2 style="font-weight: normal">Administration and Analytics Panel</h2>
      <p>This panel can be used to manage the system's configuration and to analyze user behavior.</p>
      <div style="width: 45%; border: 1px solid black; display: inline-block; margin-right: 3%; padding-left: 10px; vertical-align: top;">
        <h3>Administration</h3>
        <p style="margin-bottom: 0; padding-bottom: 0;"><a href="/summary/chart_view/1">View users</a></p>
        <p style="margin: 4px 0 10px 0; font-size: small; font-style: italic;">Provides an overview of all users and settings to alter their accounts.</p>
        
        <p style="margin-bottom: 0; padding-bottom: 0;"><a href="#">View questions</a></p>
        <p style="margin: 4px 0 10px 0; font-size: small; font-style: italic;">Lists all questions and provides some configuration options.</p>
        
      </div>
      <div style="width: 45%; border: 1px solid black; display: inline-block; padding-left: 10px; vertical-align: top;">
        <h3>Analytics</h3>
        <p style="margin-bottom: 0; padding-bottom: 0;"><a href="/summary/chart_view/new_joins">New joins</a></p>
        <p style="margin: 4px 0 10px 0; font-size: small; font-style: italic;">The number of new members joining over time.</p>

        <p style="margin-bottom: 0; padding-bottom: 0;"><a href="/summary/chart_view/get/engagement">User engagement</a></p>
        <p style="margin: 4px 0 10px 0; font-size: small; font-style: italic;">Various measures of engagement among all users.</p>

        
      </div>
    </div>  
    {% include 'include/admin_sidebar.tpl' %}
  <div style="clear: both; height: 0px;">&nbsp;</div>
  </div> <!--  end main_body -->

  <!-- Container for the information that appears below the main content (i.e. licensing info). -->
    <div id="footer">
    </div>
</div> 
  </div>
</body>
</html>
