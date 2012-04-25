<script type="text/javascript">
    $(document).ready(function() {
      // Enable events for peer grading
      $('.peer-score').click(function(event) {
          var radiobutton = $(this).children();
          radiobutton.prop('checked', true);
          var p = $(this).parents('.peer-answer');
          $.ajax({
         	url: '/api/questions/' + p.attr('question_id') + '/attempts/' + p.attr('attempt_id') + '/evaluations',
         	type: 'POST',
         	data: {
                   'score' : radiobutton.val(),
                   'messages' : ''
         	},
         	success: function(response) {
         	}
          });
          $(p).fadeOut();
      });

      $('.peer-score').mouseover(function(event) {
         $(this).parent().find('.peer-instructions').html('Click to score.');
      });
      $('.peer-score').mouseout(function(event) {
         $(this).parent().find('.peer-instructions').html('');
      });

      // collapse all scraps
      $('.scrap-body').hide();
      $('.scrap-header').click(function(event) {
         var body = $(this).parent().find('.scrap-body');
         if (body.css('display') == 'none') {
            body.fadeIn();
         } else {
            body.fadeOut();
         }
      });
      
//      $('.hint-form > input').hide();
//      $('a.hint-button').click(function(event) {
//         event.preventDefault();
//         $(this).parent().find('input').show();
//      });
//      $('.hint-form').submit(function(event) {
//         event.preventDefaul();
//         var p = $(this).parents('.scrap');
//         $.ajax({
//               url: '/api/questions/' + p.attr('question_id') + '/hints',
//               type: 'POST',
//               data: {
//                  'text' : $(this).find('input[name="question-hint"]').val(),
//               },
//               success: function(response) {
//               }
//         });
//         $(p).fadeOut();
//      });
    });
</script>
<div class="scrap peer-grading" question_id="{{question.question_id}}">
  <div class="scrap-header">Grading</div>
  <div class="scrap-body">
    <form class="hint-form">
<!--    <input type="text" value="" name="question-hint">
      <a href="#" class="hint-button">Leave a hint</a> or grade answers from other students. -->
      Grade answers from other students.
    </form>
    <div class="given-answers">
      {% for answer in given_answers %}
        {% if answer.correct %}
          <div class="given-answer correct">
            Correct: 
            <div class="given-answer-text user-text">
              {{ answer.text }}
            </div>
            {% if answer.message %}
            Message: {{ answer.message }}
            {% endif %}
          </div>
        {% endif %}
      {% endfor %}
      {% for answer in given_answers %}
        {% if not answer.correct %}
          <div class="given-answer incorrect">
            Incorrect: 
            <div class="given-answer-text user-text">
              {{ answer.text }}
            </div>
            {% if answer.message %}
            Message: {{ answer.message }}
            {% endif %}
          </div>
        {% endif %}
      {% endfor %}
    </div>

    <div class="peer-answers">
      {% for attempt in peer_attempts %}
      <div class="peer-answer" attempt_id={{attempt.attempt_id}} question_id={{question.question_id}} {% if attempt.evaluation %} style="display:none;"{% endif %}>
        <form class="peer-answer-form">
          {% for score_option in score_options %}
          <div class="peer-score peer-line" title="{{score_option.1}}"><input type="radio" value="{{score_option.0}}" name="score"{% if attempt.evaluation.score == score_option.0 %}checked{% endif %}>{{score_option.0}}</div>
          {% endfor %}
          <div class="peer-instructions peer-line"></div>
        </form>
        <div class="peer-response-container">
          Peer response: 
          <div id='attempttext{{attempt.attempt_id}}' class="attempt-text user-text">
            {{attempt.text}}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>

