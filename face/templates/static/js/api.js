//////////////////////
/// API  ///
//////////////////////


var questions = new function() {
   this.get = function(qid, callback) {
       $.getJSON('/api/questions/' + qid, callback);};
   this.list = function(callback) {
       $.getJSON('/api/questions/list');};
}

function load_hint() {
   $('#hintdisplay').css('display', 'block');
   elig_hints = $('#hintdisplay').children('li');
   for (i = 0; i < elig_hints.length; i++) {
      if ($(elig_hints[i]).html().length == 0) {
         $.getJSON('/ajax/hints/get/' + question_id + '/' + $(elig_hints[i]).attr('id'),
            function(data) {
               var hint_html = "<div class='votepane'><div class='hintvoter'><a onclick=\"hint_vote('" + data.hint_id + "', true)\">";
               hint_html += "<img title='Upvote this hint' src='/static/img/approve.png' /></a><a onclick='hint_vote(\"" + data.hint_id + "\", false)'>";
               hint_html += '<img title="Downvote this hint" src="/static/img/disapprove.png" /></a></div>';
               hint_html += '<div class="hintscore" id="score_' + data.hint_id + '">' + (data.upvotes - data.downvotes) + '</div></div>';
               hint_html += '<div style="vertical-align: top; display: inline-block; margin-top: 2px; width: 90%;">';
               hint_html += data.hint_body + '</div>';
               $(elig_hints[i]).html(hint_html);
            }
         );
         // We've fetched a hint so our work here is done.
         return;
     }
   }
   alert('Sorry, no more hints are available for this question.');
}

function hint_vote(hint_id, approve_flag) {
   url = approve_flag ? '/ajax/hints/vote/yes/' : '/ajax/hints/vote/no/';

   $.post(url + hint_id, { 'hinthash' : hint_id }, function(data) {
      if (data.msg == 'success') {
         $('#score_' + hint_id).html(data.upvotes - data.downvotes);
      }
      else {
         alert(data.msg);
      }
   });
}
