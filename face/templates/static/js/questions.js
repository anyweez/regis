

function view_question_handler(data) {
   var question_html = '';
   if (data.kind == "question#pending" || data.kind == 'question#ready') {
       question_html = '<h2 style="margin-bottom: 5px;">Sorry!</h2>' +
       "<p>You haven't unlocked this question yet.  Keep working and you'll get it in no time!</p>";
   } else {
       question_html = '<h2 style="margin-bottom: 5px;">';
       question_html += 'Question #' + data.template + ': ';
       question_html += '<span style="font-weight: normal">';
       question_html += data.title + '</span></h2>';
       question_html += '<p style="color: #555; margin: 0px 0px 10px 3px; padding: 0;">released on ' + data.published + '</p>';
       question_html += '<p id="main_q">' + data.content + '</p>';
       question_html += '<div id="answerbox" style="height: 40px;">';
       question_html += '' +
'<form accept-charset="utf-8" method="post" action="/question/check">' +
'<div style="display:none">' +
'<input type="hidden" value="f4d76ce04b9550de5aee68dc690efb5c" name="csrfmiddlewaretoken">' +
'</div>' +
'<input type="text" style="font-size: 20px; margin: 0; border-radius: 5px 0px 0px 5px; height: 30px;" value="" name="answer">' +
'<input type="hidden" value="181" name="qid">' +
'<input type="hidden" value="/dash" name="on_correct">' +
'<input type="hidden" value="/dash" name="on_incorrect">' +
'<input type="submit" value="Guess" name="submit">' +
'</form>' +
'</div>';
       question_html += '<div id="hintzone" class="hintbox"><img src="/static/img/hint.png"><span id="hintdrop">No hints are currently available for this question.</span><div id="hintdisplay" style="display: none;"></div></div>';
   }
   $('#question_body').html(question_html);
}
