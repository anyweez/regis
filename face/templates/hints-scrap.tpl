<script type="text/javascript">
   $(document).ready(function() {
    
      // collapse all scraps
      $('.hint-scrap-body').hide();
      $('.hint-scrap-header{{question.question_id}}').click(function(event) {
         var body = $(this).siblings('.hint-scrap-body');
         if (body.css('display') == 'none') {
            body.slideDown();
         } else {
            body.slideUp();
         }
      });

      
      $('a.new-hint-button{{question.question_id}}').click(function(event) {
         var question_id = this.question_id;
         event.preventDefault();
	 $( "#hint-dialog{{question.question_id}}" ).dialog( "open" );
      });
      $( "#hint-dialog{{question.question_id}}" ).dialog({
         autoOpen: false,
         height: 200,
         width: 350,
         modal: true,
         buttons: {
            "Leave hint": function() {
               $( this ).dialog( "close" );
               $('#hint-form{{question.question_id}}').trigger('submit');
            },
            Cancel: function() {
               $( this ).dialog( "close" );
            }
         },
         close: function() {
         }
      });

      $('#hint-form{{question.question_id}}').submit(function(event) {
         event.preventDefault();
         $("#hint-dialog{{question.question_id}}").dialog( "close" );
         $.ajax({
            url: '/api/questions/' + '{{question.question_id}}' + '/hints',
            type: 'POST',
            data: {
               'text' : $(this).find('input[name="hint"]').val(),
            },
            success: function(response) {
            }
         });
      });

      $('.get-hints-button{{question.question_id}}').click(function(event) {
         event.preventDefault();
         var p = $(this).parents('.scrap');
         $.ajax({
               url: '/api/questions/' + {{question.question_id}} + '/hints',
               type: 'GET',
               success: function(response) {
                  $('#hints{{question.question_id}}').html(response.html);
               }
         });
      });
   });
</script>
	

<div id="hint-dialog{{question.question_id}}" title="Leave hint">
	<form id="hint-form{{question.question_id}}">
	<fieldset>
		<label for="hint">Hint</label>
		<input type="text" name="hint" id="hint" class="text ui-widget-content ui-corner-all" />
	</fieldset>
	</form>
</div>


<div class="scrap hints" question_id="{{question.question_id}}">
  <div class="scrap-header hint-scrap-header{{question.question_id}}">Hints</div>
  <div class="hint-scrap-body">
    <a href="#" class="new-hint-button{{question.question_id}}">Leave a hint</a>
    <a href="#" class="get-hints-button{{question.question_id}}">Get hints</a>
    <div id="hints{{question.question_id}}">
      
    </div>
  </div>
</div>

