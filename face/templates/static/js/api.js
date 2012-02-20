//////////////////////
///      API       ///
//////////////////////

/* 
** TO MAKE A NEW API: ** 

###      api.js      ###
Create a new API call for the object being modified.
Example: create api.attempts.insert

###      urls.py     ###
Create a rule for the URL that you use in api.js
Example: ('^api/attempts/insert/([0-9]+)$', views.api_attempts_insert),

###     views.py     ###
Write the Django handler for the API call.
This does the meet of the work.
Make sure it returns a JSON object.
Example: views.api_attempts_insert(request)

See views.system_tests_run for informaion about testing.
After testing, the API is ready.

###     templates    ###
Modify templates as needed to use your API methods.
*/
var api = new function() {

   this.questions = new function() {
      this.get = function(qid, callback) {
          $.getJSON('/api/questions/' + qid, callback);};
      this.list = function(callback) {
          $.getJSON('/api/questions/list', callback);};
   }
   
   this.hints = new function() {
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

   this.attempts = new function() {
      this.get = function(id, callback) {
          $.getJSON('/api/attempts/' + id, callback);};
      this.list = function(qid, callback) {
          $.getJSON('/api/attempts/list/' + qid, callback);};
      this.insert = function(qid, content, callback) {
          $.post('/api/attempts/insert/' + qid,
                 { 'question' : qid,
                   'content' : content },
                 callback,
                 'json');};
   }
}

function alert_messages(data) {
   if (data.kind == 'message') {
      alert(data.message);
   }
}

function test_api(api_method, num_args, args_list, expected_json, no_more_fields_allowed, callback) {
   if (!no_more_fields_allowed) {
      no_more_fields_allowed = false;
   }
   var data_handler = function (data) {
         var errors = Array();
         for (var key in expected_json) {
            if (!(key in data)) {
               errors.push(key + ' not in response');
            } else if (expected_json[key] == null) {
               // null indicates that the real data can be any value
            } else if (expected_json[key] != data[key]) {
               errors.push(key + ' values do not match');
            }
         }
         if (no_more_fields_allowed) {
            for (var key in data) {
               if (!(key in expected_json)) {
                  errors.push(key + ' not allowed in response');
               }
            }
         }
         var response = {};
         if (errors.length == 0) { 
            response.success = true;
         } else { 
            response.success = false;
         }
         response.errors = errors;
         callback(response);
      };
   if (num_args == 0) {
      api_method(data_handler);
   } else if (num_args == 1) {
      api_method(args_list[0], data_handler);
   } else if (num_args == 2) {
      api_method(args_list[0], args_list[1], data_handler);
   } else if (num_args == 3) {
      api_method(args_list[0], args_list[1], args_list[2], data_handler);
   } else if (num_args == 4) {
      api_method(args_list[0], args_list[1], args_list[2], args_list[3], data_handler);
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


