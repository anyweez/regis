{% comment %}
Requires

question_id
{% endcomment %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  
  {% include 'include/common_header.tpl' %}
  
  <script type="text/javascript" src="/static/js/api.js">
  </script>
 
  <script type="text/javascript">
    var question_id = {{ questions_id }};

    // Fetch information about hints as soon as the page is loaded.
    $(document).ready(function() {
       api.questions.get(question_id, questions_get_handler);
       api.hints.list(question_id, hints_list_handler);
       api.attempts.list(question_id, attempts_list_handler);
       clear_messages();
    });

    function questions_get_handler(data) {
      $('#question').html(data.html);
      $('#attempt_form').submit(attempt_submit_handler);
      update_question_status(data.status);
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
      $(this).unbind('click');
    }
    
    function hint_get_handler(data) {
      $('#hint' + data.id).html(data.html);
      update_messages(data.messages);
    }
    
    function hint_vote_up(hint_id) {
       clear_messages();
       api.hints.vote(hint_id, 'yes', hint_get_handler );
    }
    
    function hint_vote_down(hint_id) {
       clear_messages();
       api.hints.vote(hint_id, 'no', hint_get_handler );
    }

    function attempts_list_handler(data) {
       var question_id = data.question;
       var div = $('#previous_attempts' + question_id);
       var ul = $('<ul></ul>');
       for (var i = data.items.length - 1; i >= 0; i--) {
          ul.append($('<li></li>').html(data.items[i].html));
       }
       div.html('Previous attempts');
       div.append(ul);
    }
    
    function update_question_status(question_status) {
       if (question_status == 'solved') {
          div = $('#question_status' + question_id);
          div.html('<h1>Solved!</h1>');
       } else {
          div = $('#question_status' + question_id);
          div.html('Ready to solve.');
       }
    }
    
    // This variable acts as a flag to tell the message updater
    // whether it should replace the list of messages, or 
    // add the new messages to the old list. The flag is set
    // by calling clear_messages().
    var mark_message_for_deletion = true;
    function update_messages(messages) {
       if (messages) {
          var ul = $('#messages > ul');
          if (mark_messages_for_deletion == true) {
             ul.html('');
             mark_messages_for_deletion = false;
          }
          for (var i = 0; i < messages.length; i++) {
             ul.append($('<li></li>').html(messages[i]));
          }
       }
    }
    
    function clear_messages() {
       mark_messages_for_deletion = true;
    }

    function attempt_submit_handler(event) {
       clear_messages();
       event.preventDefault();
       var values = $('#attempt_form :input');
       values.each(function() {
          if (this.name == 'answer') {
             answer = $(this).val();
             $(this).val('');
          } else if (this.name == 'qid') {
             qid = $(this).val();
          }
       });
       if (answer && qid) {
          api.attempts.insert(qid, answer, attempts_submit_response_handler);
       }
    }
    
    function attempts_submit_response_handler(data) {
       api.attempts.list(question_id, attempts_list_handler);
       update_messages(data.messages);
    }
  </script>
  

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
        <div id="question_status{{ questions_id }}">
        </div>
        <div id="messages">
          <ul></ul>
        </div>
        <div id="question">
        </div>
        <div id="previous_attempts{{ questions_id }}">
        </div>
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
