//////////////////////
///      API       ///
//////////////////////


var questions = new function() {
   this.get = function(qid, callback) {
       $.getJSON('/api/questions/' + qid, callback);};
   this.list = function(callback) {
       $.getJSON('/api/questions/list', callback);};
}



