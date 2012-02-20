{% comment %}
Expected variables:

wait_for_click
test
{% endcomment %}
<script type="text/javascript">
function test_{{test}}(event) {
   if (event) {
      event.preventDefault();
   }
   var outputdiv = $('#{{test}}');  
   outputdiv.html("Running test {{test}}");

   var api_method = questions.list;
   var num_args = 0;
   var args_list = [];
   var expected_response = {
          'kind' : 'questionFeed',
          'items' : null,
       };
   var no_more_fields = false;
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

