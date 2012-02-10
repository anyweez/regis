

function view_question_handler(data) {
   var question_html = '';
   if (data.kind == "question#pending" || data.kind == 'question#ready') {
       question_html = '<h2 style="margin-bottom: 5px;">Sorry!</h2>' +
       "<p>You haven't unlocked this question yet.  Keep working and you'll get it in no time!</p>";
   } else if (data.kind == "question") {
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
   } else {
       question_html = '<h2 style="margin-bottom: 5px;">Sorry!</h2>' +
       "<p>Question not found.</p>";
   }
   $('#question_body').html(question_html);
}

function list_questions_handler(data) {
	var html = '';
	if ('questionFeed' == data.kind) {
		for (var i = 0; i < data.items.length; i++) {

			var q = data.items[i];
			if ('pending' != q.status) {
				html += '<div class="qbox">';
				if ('ready' == q.status) {
					html += '<div class="q_decoration q_unavailable">' +
		    			'<p class="q_status">locked</p>';
				}
				if ('released' == q.status) {
					html += '<div class="q_decoration q_unanswered">' +
		    			'<p class="q_status">unsolved</p>';
				}	
				if ('solved' == q.status) {
					html += '<div class="q_decoration q_answered">' +
		    			'<p class="q_status">solved</p>';
				}	
		 		html += '<p>solved by 2 of 8</p>' +
		    			'<p>( 25% )</p>' +
		  			'</div>';
				if ('ready' == q.status) {
					html += '<h2 class="qbox_head">Question #' + q.template + ': ' + q.title + '</h2>';
					html += '<p class="qbox_preview" style="font-style: italic">This question isn\'t available yet.</p>';
				} else {
					html += '<h2 class="qbox_head">Question #' + q.template + ': <a href="' + q.url + '">' + q.title + '</a></h2>';
					if (q.content.length > 60) {
						html += '<p class="qbox_preview">' + q.content.substring(0,200) + '...</p>';
					} else {
						html += '<p class="qbox_preview">' + q.content + '</p>';
					}
				} 
				html += '</div>';
			}
		}
	} else {
		html = 'Sorry, could not find question data.';
	}
	$('#question_body').append(html);

}





