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
       $.post('/api/hints/' + hid + '/vote',
              { 'id' : hid,
                'rating' : approve },
              callback,
              'json');};
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
   hints.vote(hint_id, 'yes', alert_messages );
}

function hint_vote_down(hint_id) {
   hints.vote(hint_id, 'no', alert_messages);
}

function alert_messages(data) {
   if (data.kind == 'message') {
      alert(data.message);
   }
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


