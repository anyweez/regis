<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/cupertino/jquery-ui-1.8.19.custom.css" />
  <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
  <script type="text/javascript" src="/static/js/underscore.js"></script>
  <script type="text/javascript" src="/static/js/jquery-1.7.2.min.js"></script>
  <script type="text/javascript" src="/static/js/jquery-ui-1.8.19.custom.min.js"></script>
  <script type="text/javascript" src="/static/js/jquery.layout.min-1.2.0.js"></script>
  <script type="text/javascript" src="/static/js/backbone.js"></script>
  <script type="text/javascript" src="/static/js/regis/regis.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      // New deck button TODO cartland: move into better place.
      $("#new-deck-box").submit(function() {
         $.ajax({
         	url: '/api/decks',
         	type: 'POST',
         	data: {
         		'name' : $("input[name='name']").val()
         	},
         	success: function(response) {
                    a_new_deck = regis.Deck({ 'name': response.name });
         	}
         });
         return false;
      });
    
      // Initialize Regis and get some decks.
      regis_init({'load_full' : true });
      
      user_deck = regis.Deck({ 'name': 'Users', 'endpoint': 'users', 'add_to_shelf': false });      
//      a_new_deck = regis.Deck({ 'name': 'New Deck' });

      $('#profile-btn').click(function() {
        regis.activateDeck(user_deck);
      });
      
      // Activate a deck after some time has passed.  This should be
      // converted to an event eventually.
      setTimeout(function() { regis.activateDeck(user_deck); }, 250);

      // Make the deck bench.
      var layout = $('body').layout({ 
        applyDefaultStyles: true, 
        resizable: true, 
//		initClosed: true,
		size: 170,
        onopen : function () { 
          $(".ui-layout-south").css("z-index", 1000);
          $(".ui-layout-resizer-south").css("z-index", 1000);
          return true;
        },
      });
//	  layout.sizePane("south", 180);
      $(".ui-layout-pane").css("background-color", "rgba(0,0,0, 0.6)");
      $(".ui-layout-pane").css("background-color", "rgba(255,255,255, 0.6)");
      $(".ui-layout-south").css("z-index", 1000);
      $(".ui-layout-resizer-south").css("z-index", 1000);
      
      $('#new-question-btn').click(function(event) {
         event.preventDefault();
         $( "#new-question-dialog" ).dialog( "open" );
      });
        $('#new-question-dialog-form').submit(function(event) {
           event.preventDefault();
           $("#new-question-dialog").dialog( "close" );
           $.ajax({
                 url: '/api/questions',
                 type: 'POST',
                 data: {
                    'question' : $(this).find('input[name="question"]').val(),
                    'correctanswer' : $(this).find('input[name="correctanswer"]').val(),
                 },
                 success: function(response) {
                    var clist = regis.getCardList();
                    var d = regis.getActiveDeck();
                    var card = response; 
                    card.view = new CardTypeView({model: card});
                    clist.add(card);
                    console.log(card);
                    d.add(card);
                 }
           });
        });

	$( "#new-question-dialog" ).dialog({
			autoOpen: false,
			height: 300,
			width: 550,
			modal: true,
			buttons: {
				"Create Question": function() {
					$( this ).dialog( "close" );
					$('#new-question-dialog-form').trigger('submit');
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}
			},
			close: function() {
			}
		});

    });
  </script>

  <title>Welcome to codepath!</title>
  {% include 'include/common_header.tpl' %}
</head>
<body>
  <div id='main-display'>
    <h1 id="codepath-title"><span class="cp_first">code</span><span class="cp_second">path</span></h1>
    <div id="navigation">
         <div id="new-question-btn"><img src="/static/img/profile.png" />new question</div>
         <div id="profile-btn"><img src="/static/img/profile.png" />profile</div>
         <div id="logout-btn"><a href="/account/logout"><img src="/static/img/profile.png" />logout</a></div>
    </div>
    <div id='card-stack'>
    </div>
  </div>
  <div id='deck-icons' class="ui-layout-south" style="z-index: 5;">
    <form id="new-deck-box" style="float: right;">
      <input type="text" value="Untitled" name="name">
      <input type="submit" value="New Deck" name="submit">
    </form>
  </div>
</body>
</html>
	


<div id="new-question-dialog" title="New question">
	<form id="new-question-dialog-form">
	<fieldset>
		<label for="question">Question</label>
		<input type="text" name="question" id="question" class="text ui-widget-content ui-corner-all" /><br />
		<label for="correctanswer">Correct Answer</label>
		<input type="text" name="correctanswer" id="correctanswer" class="text ui-widget-content ui-corner-all" />
	</fieldset>
	</form>
</div>

