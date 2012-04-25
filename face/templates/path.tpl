<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
  <script type="text/javascript" src="/static/js/underscore.js"></script>
  <script type="text/javascript" src="/static/js/jquery-1.7.2.min.js"></script>
  <script type="text/javascript" src="/static/js/jquery-ui-1.8.19.custom.min.js"></script>
  <script type="text/javascript" src="/static/js/jquery.layout.min-1.2.0.js"></script>
  <script type="text/javascript" src="/static/js/backbone.js"></script>
  <script type="text/javascript" src="/static/js/regis/regis.js"></script>
  <script type="text/javascript" src="static/js/grading.js"></script>

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
                    alert('Deck ' + response.deck_id + ' ' + response.name);
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



    });
  </script>

  <title>Welcome to codepath!</title>
  {% include 'include/common_header.tpl' %}
</head>
<body>
  <div id='main-display'>
    <h1 id="codepath-title"><span class="cp_first">code</span><span class="cp_second">path</span></h1>
    <div id="navigation">
         <div id="profile-btn"><img src="/static/img/profile.png" />profile</div>
         <div id="logout-btn"><a href="/account/logout"><img src="/static/img/profile.png" />logout</a></div>
    </div>
    <div id='card-stack'>
    </div>
  </div>
  <div id='deck-icons' class="ui-layout-south">
    <form id="new-deck-box" style="float: right;">
      <input type="text" value="Untitled" name="name">
      <input type="submit" value="New Deck" name="submit">
    </form>
  </div>
</body>
</html>
