<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  
  {% include 'include/common_header.tpl' %}
  
  <script type="text/javascript" src="/static/js/hints.js">
  </script>
  
  <script type="text/javascript">
  var like_feedback = null;
  var challenge_feedback = null;

  // Submit this user's answer to the "did you like this question?" question
  function like_swap(btn) {
	if (like_feedback != null) {
		like_feedback.css("background-color", "#CAE3FC");
	}
    
    like_feedback = btn;
  	like_feedback.css("background-color", "#4BE846");
  	
  	$.getJSON('/ajax/feedback/like/{{ question.template.id }}/' + like_feedback.attr('value'),
            function(data) {});
  }
  
  function challenge_swap(btn) {
  	if (challenge_feedback != null) {
  		challenge_feedback.css("background-color", "#CAE3FC");
  	}
  	
  	challenge_feedback = btn;
  	challenge_feedback.css("background-color", "#4BE846");
  	
  	$.getJSON('/ajax/feedback/challenge/{{ question.template.id }}/' + challenge_feedback.attr('value'),
            function(data) {});
  }
  
  $(document).ready(function() {
    $(".feedback_btn").click(function(e) {
    	if ($(this).attr('type') == 'like') {
    		like_swap($(this));
    	}
    	if ($(this).attr('type') == 'challenge') {
    		challenge_swap($(this));
    	}
    });
  });
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

    #right_col {
      border-bottom: 3px solid black;
      border-radius: 0px 0px 0px 5px; 
    }
  </style>

  <title>Regis: {{ question.template.title }} [status]</title>
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

      {% comment %}
** If the question has been solved, give them a message telling them that 
** they were correct.  Give them a chance to leave a hint.
      {% endcomment %}      
      {% if question.status == 'solved' %}
      <h2 style="margin-bottom: 5px; font-weight: normal"><b>Correct!</b></h2>
      <p><b>{{ guess.value }}</b> was the correct answer to this puzzle.  Nice work!</p>
      <div id="feedback">
      	<h3>Reflection</h3>
      	<p>If you provide us with some feedback then we'll try to choose questions that may be more appropriate for you.</p>
      	<div style="margin-left: 10px; display: inline-block; width: 150px;">Did you like this question?</div>
      	<div type="like" value="1" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 160px;">
      		<img style="display: inline-block; width: 30px; height: 30px; margin: 0px 2px 0px 2px;" src="/static/img/buttons_ok_xl.png" />
      		<div style="text-align: left; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Yes!</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I enjoyed solving it.</p>
			</div>
      	</div>
      	<div type="like" value="0" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 160px;">
      		<img style="display: inline-block; width: 30px; height: 30px; margin: 0px 2px 0px 2px;" src="/static/img/buttons_cancel_xl.png" />
      		<div style="text-align: left; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">No!</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I'm not a fan.</p>
			</div>
		</div>
      	<div>&nbsp;</div>
      	<div style="margin-left: 10px; display: inline-block; width: 150px;">How challenging did you find it to be?</div>
      	<div type="challenge" value="1" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 140px; height: 75px;">
      		<div style="text-align: center; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Simple</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I knew how to solve it right away.</p>
			</div>
		</div>
		<div type="challenge" value="2" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 140px; height: 75px;">
      		<div style="text-align: center; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Pretty easy</p>
				<p style="margin: 2px; padding: 0; font-size: small;">It took me a minute but was fine once I thought about it.</p>
			</div>
		</div>
		<div type="challenge" value="3" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 140px; height: 75px;">
      		<div style="text-align: center; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Manageable</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I had to experiment around a bit to find the answer.</p>
			</div>
		</div>
		<div type="challenge" value="4" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 140px; height: 75px;">
      		<div style="text-align: center; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Challenging</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I had to fight but now feel like I understand the solution.</p>
			</div>
		</div>
		<div type="challenge" value="5" class="feedback_btn" style="padding: 3px; vertical-align: top; display: inline-block; cursor: pointer; background-color: #CAE3FC; border: 2px outset black; border-radius: 3px; width: 140px; height: 75px;">
      		<div style="text-align: center; display: inline-block;">
      			<p style="margin: 0; padding: 0; font-weight: bold">Impossible</p>
				<p style="margin: 2px; padding: 0; font-size: small;">I don't know how I got it right.</p>
			</div>
		</div>
      </div>
      <div class="hintbox" style="margin-top: 20px;">
        <p style="font-weight: bold; margin: 2px;">Before you go, would you like to leave a hint for others who
      try this question?</p>
      <p style="margin: 2px;">A good hint will not give away the answer, but will provide some guidance about the 
      algorithm you developed or thought process you went through to develop it.</p>
	  {% include 'include/hintsubmit.tpl' %}
      </div>  
      
      <h3>Next Steps</h3>
        {% if next_q %}
        <p>A new question has been unlocked for you: <a href="/question/view/{{next_q.template.id}}">{{ next_q.template.title }}</a></p>
        {% else %}
        <p>We're actually all out of questions.  Tell your TA to get on it!</p>
        {% endif %}
      
      {% endif %}
      
      {% comment %}
** If the question still hasn't been solved, the guess must have been incorrect.
** Report that back to them and give them the opportunity to see a hint if
** desired.
      {% endcomment %}
      {% if question.status == 'released' %}
      <h2 style="margin-bottom: 5px; font-weight: normal">Sorry, that's not correct.</h2>
      <p>You guessed <b>{{ guess.value }}</b> but unfortunately that's not the correct answer.</p>
      
        {% if answer %}
        {{ answer.message }}
        {% endif %}
      
      <p>Care to <a href="/question/view/{{question.template.id}}">try again</a>?</p>
      {% include 'include/hintbox.tpl' %}
      {% endif %}

      {% if question.status == 'ready' or question.status == 'pending' %}
      <h2 style="margin-bottom: 5px; font-weight: normal">{{ question.template.title}}: Question Unavailable</h2>
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
