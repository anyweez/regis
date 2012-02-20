
<script type="text/javascript">
   $(document).ready(function() {
//      $('#api_questions_list_structure').click(do_test1);
      do_test1();
   });
function do_test1(event) {
   if (event) {
      event.preventDefault();
   }
   var outputdiv = $('#api_questions_list_structure');  
   outputdiv.html("Running test ");
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
         
   var api_method = questions.list;
   var num_args = 0;
   var args_list = Array();
   var expected_response = {
          'kind' : 'questionFeed',
          'items' : null,
       };
   test_api(api_method, num_args, args_list, expected_response, callback);
}

function test_api(api_method, num_args, args_list, expected_json, callback) {
   var data_handler = function (data) {
         var errors = Array();
         for (var key in expected_json) {
            if (!(key in data)) {
               errors.push(key + ' not in response');
            } else if (expected_json[key] == null) {
               // null indicates that the real data can be any value
            } else if (expected_json[key] != data[key]) {
               errors.push(key + ' values do not match');
            } else {
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

</script>
<div id="api_questions_list_structure">
  <a href="#">{{test}}</a>
</div>

