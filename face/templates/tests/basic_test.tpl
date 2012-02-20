{% comment %}
Expected variables:

wait_for_click
{% endcomment %}
<script type="text/javascript">
   $(document).ready(function() {
   {% if wait_for_click == "yes" %}
      $('#api_questions_list_structure').click(do_test1);
   {% else %}
      do_test1();
   {% endif %}
   });

function do_test1(event) {
   if (event) {
      event.preventDefault();
   }
   var outputdiv = $('#api_questions_list_structure');  
   outputdiv.html("Running test ");
         
   var api_method = questions.list;
   var num_args = 0;
   var args_list = Array();
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


</script>
<div id="api_questions_list_structure">
  <a href="#">{{test}}</a>
</div>

