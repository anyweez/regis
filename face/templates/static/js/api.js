//////////////////////
///      API       ///
//////////////////////


var questions = new function() {
   this.get = function(qid, callback) {
       $.getJSON('/api/questions/' + qid, callback);};
   this.list = function(callback) {
       $.getJSON('/api/questions/list', callback);};
}

var hints = new function() {
   this.get = function(hid, callback) {
       $.getJSON('/api/hints/' + hid, callback);};
   this.list = function(qid, callback) {
       $.getJSON('/api/hints/list/' + qid, callback);};
   this.vote = function(hid, approve, callback) {
       $.getJSON('/api/hints/vote/' + hid + '/' + approve);};
}

function view_question_handler(data) {
  $('#question_body').html(data.html);
}

function list_questions_handler(data) {
  for (var i = 0; i < data.items.length; i++) {
    $('#question_body').append(data.items[i].html);
  }
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
  hints.get($(this).attr("id").slice(4), hint_get_handler);
}

function hint_get_handler(data) {
  $('#hint' + data.id).html(data.html);
}

function hint_vote_up(hint_id) {
   hints.vote(hint_id, 'yes', function(data) { alert('yes'); } );
}

function hint_vote_down(hint_id) {
   hints.vote(hint_id, 'no', function(data) { alert('now'); } );
}



// Send CSRF tokens when we make AJAX requests
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

//////////////////////
/// Hint functions ///
//////////////////////

function get_hints(qid) {
   $.getJSON('/ajax/hints/basic/' + qid,
     function(data) {
       // Update the hint status to state whether hints are available.
       if (data.length > 0) {
         if (data.length == 1) {
            $('#hintdrop').html('<a onclick="load_hint();" href="#">Want a hint</a>?  There is 1 available.');  
         }
         else {
            $('#hintdrop').html('<a onclick="load_hint();" href="#">Want a hint</a>?  There are ' + data.length + ' available.');
         }
         // Add the hint codes to the array.
         $('#hintdisplay').append('<ul>');
         for (i = 0; i < data.length; i++) {
           $('#hintdisplay').append('<li id="' + data[i] + '"></li>');
         }
         $('#hintdisplay').append('</ul>');
       }
       else {
         $('#hintdrop').html('No hints are currently available for this question.');
       }       
     }
   );
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
