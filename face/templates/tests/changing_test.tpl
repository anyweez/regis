{% comment %}
Expected variables:

wait_for_click
test
{% endcomment %}
<script type="text/javascript">
   $(document).ready(function() {
   {% if wait_for_click == "yes" %}
      $('#{{test}}').click(test_{{test}});
   {% else %}
      test_{{test}}();
   {% endif %}
   });

function test_{{test}}(event) {
   if (event) {
      event.preventDefault();
   }
   var outputdiv = $('#{{test}}');  
   outputdiv.html("Running test ");
         
   var api_method = questions.get;
   var num_args = 1;
   var args_list = [1];
   var expected_response = {
          'kind' : 'question',
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


</script>
<div id="{{test}}">
  <a href="#">{{test}}</a>
</div>

