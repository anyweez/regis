{% comment %}
Expected variables:

wait_for_click
test
{% endcomment %}
<script type="text/javascript">
function test_{{test}}(event) {
////////////////////////////////////
///    MODIFY VARIABLES BELOW    ///
////////////////////////////////////
   var api_method = questions.get;
   var num_args = 1;
   var args_list = [1];
   var no_more_fields = false;
   var expected_response = {
          'kind' : 'question',
          'key' : 181,
          'id' : 1,
          'hints' : null,
          'errors' : null,
          'title' : "Numbers in Numbers",
          'url' : "http://localhost:8080/questions/1",
          'actor' : 2,
          'content' : null,
          'html' : null,
          'published' : null,
       };
////////////////////////////////////
///    MODIFY VARIABLES ABOVE    ///
////////////////////////////////////

   var outputdiv = $('#{{test}}');  
   outputdiv.html("Running test {{test}}");
   var callback = function (data) {
         if (data.success == true) {
            outputdiv.html("Success!");
         } else {
            outputdiv.html("Failed.");
         }
         for (var i = 0; i < data['errors'].length; i++) {
            outputdiv.append($('<li></li>').html(data['errors'][i]));
         }
      };
   test_api(api_method, num_args, args_list, expected_response, no_more_fields, callback);
   if (event) {
      event.preventDefault();
   }
}

   $(document).ready(function() {
   {% if wait_for_click == "yes" %}
      $('#{{test}}').click(test_{{test}});
   {% else %}
      test_{{test}}();
   {% endif %}
   });
</script>
<div id="{{test}}">
  <a href="#">{{test}}</a>
</div>

