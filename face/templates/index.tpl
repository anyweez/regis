<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/main.css" />
  <link href='http://fonts.googleapis.com/css?family=Pontano+Sans' rel='stylesheet' type='text/css'>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
  <script type="text/javascript" src="/static/js/underscore.js"></script>
  <script type="text/javascript" src="/static/js/backbone.js"></script>
  <script type="text/javascript" src="/static/js/regis/regis.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      regis_init();
      deck = regis.Deck('All', 'home');
      deck2 = regis.Deck('Study Cards', 'home2');
      
      setTimeout(function() { regis.activateDeck(deck); }, 500);
    });
    
//    deck2 = regis.Deck('Study Cards', 'home2');
//    setTimeout(function() { regis.activateDeck(deck2); }, 5000);
//    deck.show();
  </script>

  <title>Welcome to codepath!</title>
  {% include 'include/common_header.tpl' %}
</head>
<body>
  <div id='main-display'>
    <h1 id="codepath-title"><span class="cp_first">code</span><span class="cp_second">path</span></h1>
    <div id="navigation">
<!--         <div id="profile_btn"><img src="/static/img/profile.png" />profile</div> -->
    </div>
    <div id='card-stack'>
    </div>
    
    <div id='deck-icons'></div>
  </div>
</body>
</html>
