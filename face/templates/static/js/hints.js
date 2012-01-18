
// Fetch information about hints as soon as the page is loaded.
$(document).ready(function() {
  get_hints(question_id);
});

function get_hints(qid) {
   $.getJSON('/ajax/hints/basic/' + qid,
     function(data) {
       // Update the hint status to state whether hints are available.
       if (data.length > 0) {
         if (data.length == 1) {
            $('#hintzone').html('<a onclick="load_hint();">Want a hint?  There is 1 available.</a>');  
         }
         else {
            $('#hintzone').html('<a onclick="load_hint();">Want a hint?  There are ' + data.length + ' available.</a>');
         }
         // Add the hint codes to the array.
         for (i = 0; i < data.length; i++) {
           $('#hintdisplay').append('<div id="' + data[i] + '"></div>');
         }
       }
       else {
         $('#hintzone').html('No hints are currently available for this question.');
       }       

     }
   );
}

function load_hint() {
   elig_hints = $('#hintdisplay').children('div');
   for (i = 0; i < elig_hints.length; i++) {
      if ($(elig_hints[i]).html().length == 0) {
         $.getJSON('/ajax/hints/get/' + question_id + '/' + $(elig_hints[i]).attr('id'),
            function(data) {
               var hint_html = '<p style="margin-left: 20px;">'+data.hint_body+'</p>';
               $(elig_hints[i]).html(hint_html);
            }
         );
         // We've fetched a hint so our work here is done.
         return;
     }
   }
   alert('Sorry, no more hints are available for this question.');
}
