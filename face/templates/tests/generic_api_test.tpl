{% comment %}
Expected variables:

testname
wait_for_click
test
{% endcomment %}
<script type="text/javascript">
function test_{{testname}}(event) {
   var outputdiv = $('#{{testname}}');  
   outputdiv.html("Running test {{testname}}");
////////////////////////////////////
///    MODIFY VARIABLES BELOW    ///
////////////////////////////////////
   var api_method = {{jsinfo.api_method}};
   var num_args = {{jsinfo.num_args}};
   var args_list = {{jsinfo.args_list|safe}};
   var no_more_fields = {{jsinfo.no_more_fields}};
   var expected_response = {{jsinfo.expected_response|safe}};
////////////////////////////////////
///    MODIFY VARIABLES ABOVE    ///
////////////////////////////////////
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
      $('#{{testname}}').click(test_{{testname}});
   {% else %}
      test_{{testname}}();
   {% endif %}
   });
</script>

<span id="{{testname}}" class="api_test_span">
  <a href="#">{{testname}}</a>
</span>

