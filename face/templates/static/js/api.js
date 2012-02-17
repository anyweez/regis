//////////////////////
///      API       ///
//////////////////////


var questions = new function() {
   this.get = function(qid, callback) {
       $.getJSON('/api/questions/' + qid, callback);};
   this.list = function(callback) {
       $.getJSON('/api/questions/list', callback);};
}

function view_question_handler(data) {
  $('question_body').html(data.html);
}

function list_questions_handler(data) {
  for (var i = 0; i < data.items.length; i++) {
    $('question_body').append(data.items[i].html);
  }
}

