<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  
  {% include 'include/common_header.tpl' %}
  
  <script type="text/javascript" src="/static/js/api.js">
  </script>
  <script type="text/javascript" src="/static/js/hints.js">
  </script>
 
  <script type="text/javascript">
    var question_id = {{ tid }};
    // Fetch information about hints as soon as the page is loaded.
    $(document).ready(function() {
       api.questions.get(question_id, questions_get_handler);
       api.hints.list(question_id, hints_list_handler);
       api.attempts.list(question_id, attempts_list_handler);
    });

    function questions_get_handler(data) {
      $('#question_body').html(data.html);
    }
    
    function hints_list_handler(data) {
      for (var i = 0; i < data.items.length; i++) {
        var hint = data.items[i];
        $('#hint' + hint.id).html('<a href="#">Hint ' + (i + 1) +'</a>');
        $('#hint' + hint.id).click(hint_click_handler);
      }
    }

    function hint_click_handler(event) {
      event.preventDefault();
      api.hints.get($(this).attr("id").slice(4), hint_get_handler);
    }
    
    function hint_get_handler(data) {
      $('#hint' + data.id).html(data.html);
    }
    
    function hint_vote_up(hint_id) {
       api.hints.vote(hint_id, 'yes', alert_messages );
    }
    
    function hint_vote_down(hint_id) {
       api.hints.vote(hint_id, 'no', alert_messages);
    }

    function attempts_list_handler(data) {
       var div = $('#attempts_body');
       var ul = $('<ul></ul>');
       for (var i = 0; i < data.items.length; i++) {
          ul.append($('<li></li>').html(data.items[i].html));
       }
       div.html(ul);
    }
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
    <div id="attempts_body">
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
